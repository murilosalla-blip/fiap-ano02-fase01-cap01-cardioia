// CardioIA Fase 3 — MQTT com confirmação após persistência no consumidor.
// Mantenho a coleta no loop principal e as operações de rede em outra tarefa.
#include <Arduino.h>
#include <DHTesp.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <esp_system.h>
#include <esp_timer.h>
#include <atomic>
#include <math.h>
#include <new>
#include "edge_core.h"
#include "mqtt_delivery.h"

constexpr int DHT_PIN = 15;
constexpr int PULSE_PIN = 26;
constexpr int CONNECTION_PIN = 27;
constexpr uint32_t SAMPLE_INTERVAL_MS = 5000;
constexpr size_t QUEUE_CAPACITY = 2000;
// O broker usa tempo real; o relógio do Wokwi pode avançar lentamente.
// Mantenho a validade dos dados separada deste prazo de transporte MQTT.
constexpr uint16_t MQTT_KEEPALIVE_SECONDS = 300;
constexpr uint16_t MQTT_SOCKET_TIMEOUT_SECONDS = 5;
constexpr char DEVICE_ID[] = "cardioia-esp32-01";
constexpr char MQTT_HOST[] = "broker.hivemq.com";
constexpr char TOPIC_ROOT[] = "cardioia/aura/fase3/478054573982428161/v1";

struct SendRequest { char body[1024]; };
struct ReceivedAck { uint32_t sequence; };
QueueHandle_t outgoing;
QueueHandle_t incomingAcks;
std::atomic<bool> networkAllowed{false};
std::atomic<bool> networkReady{false};
std::atomic<bool> brokerFault{false};
DHTesp dht;
WiFiClient tcpClient;
PubSubClient mqtt(tcpClient);
cardioia::OfflineQueue<QUEUE_CAPACITY>* pending = nullptr;
cardioia::PulseButton pulseButton;
cardioia::DeliveryTracker delivery;
char sessionId[24];
char telemetryTopic[180];
char ackTopic[180];
char statusTopic[180];
uint64_t lastCollection = 0;
uint64_t lastScheduled = 0;
uint32_t nextSequence = 1;
uint32_t pulseCount = 0;
char serialCommand[32];
size_t serialCommandLength = 0;

uint64_t uptimeMs() {
  return static_cast<uint64_t>(esp_timer_get_time()) / 1000;
}

void receiveAck(char* topic, byte* payload, unsigned int length) {
  if (strcmp(topic, ackTopic) != 0 || length > 384) return;
  StaticJsonDocument<384> doc;
  if (deserializeJson(doc, payload, length)) return;
  if (!doc["schema_version"].is<unsigned int>() || doc["schema_version"].as<unsigned int>() != 1
      || !doc["sequence"].is<uint32_t>() || !doc["device_id"].is<const char*>()
      || !doc["session_id"].is<const char*>() || !doc["status"].is<const char*>()) return;
  if (strcmp(doc["device_id"], DEVICE_ID) || strcmp(doc["session_id"], sessionId)
      || strcmp(doc["status"], "stored")) {
    Serial.println("# ack_ignorado: dispositivo, sessao ou status incorreto");
    return;
  }
  ReceivedAck ack{doc["sequence"].as<uint32_t>()};
  // Se o canal estiver cheio, preservo a pendência; o reenvio pedirá outro ACK.
  xQueueSend(incomingAcks, &ack, 0);
}

void publishStatus(const char* state) {
  char message[180];
  snprintf(message, sizeof(message),
      "{\"device_id\":\"%s\",\"session_id\":\"%s\",\"state\":\"%s\",\"simulated\":true}",
      DEVICE_ID, sessionId, state);
  mqtt.publish(statusTopic, message, true);
}

void networkTask(void*) {
  WiFi.mode(WIFI_STA);
  mqtt.setServer(MQTT_HOST, 1883);
  mqtt.setCallback(receiveAck);
  mqtt.setBufferSize(1536);
  mqtt.setSocketTimeout(MQTT_SOCKET_TIMEOUT_SECONDS);
  mqtt.setKeepAlive(MQTT_KEEPALIVE_SECONDS);
  // No WiFiClient do ESP32 2.0.17, setTimeout recebe segundos.
  tcpClient.setTimeout(3);
  bool wifiStarted = false;
  bool previousFault = false;
  bool firstConnectionAttempt = true;
  uint8_t consecutiveFailures = 0;
  uint64_t lastWifiAttempt = 0;
  uint64_t lastBrokerAttempt = 0;
  SendRequest request;
  for (;;) {
    uint64_t now = uptimeMs();
    if (!networkAllowed.load()) {
      networkReady.store(false);
      if (mqtt.connected()) { publishStatus("offline_simulated"); mqtt.disconnect(); }
      if (wifiStarted) WiFi.disconnect(false);
      tcpClient.stop();
      wifiStarted = false;
      firstConnectionAttempt = true;
      consecutiveFailures = 0;
      xQueueReset(outgoing);
      vTaskDelay(pdMS_TO_TICKS(25));
      continue;
    }
    bool fault = brokerFault.load();
    if (fault != previousFault) {
      networkReady.store(false);
      if (mqtt.connected()) { publishStatus("broker_fault_test"); mqtt.disconnect(); }
      tcpClient.stop();
      mqtt.setServer(MQTT_HOST, fault ? 1 : 1883);
      previousFault = fault;
      firstConnectionAttempt = true;
      consecutiveFailures = 0;
      xQueueReset(outgoing);
    }
    if (WiFi.status() != WL_CONNECTED) {
      networkReady.store(false);
      if (!wifiStarted || now - lastWifiAttempt >= 10000) {
        WiFi.begin("Wokwi-GUEST", "", 6);
        wifiStarted = true;
        lastWifiAttempt = now;
        Serial.println("# wifi_conectando");
      }
      vTaskDelay(pdMS_TO_TICKS(25));
      continue;
    }
    if (!mqtt.connected()) {
      networkReady.store(false);
      if (firstConnectionAttempt || now - lastBrokerAttempt >= 5000) {
        firstConnectionAttempt = false;
        lastBrokerAttempt = now;
        char clientId[32];
        snprintf(clientId, sizeof(clientId), "aura-%s", sessionId);
        char will[180];
        snprintf(will, sizeof(will),
            "{\"device_id\":\"%s\",\"session_id\":\"%s\",\"state\":\"offline_unexpected\",\"simulated\":true}",
            DEVICE_ID, sessionId);
        // Este connect pode bloquear a tarefa de rede. A coleta continua
        // independentemente no outro núcleo; não espero conexão no loop().
        tcpClient.stop();
        bool connected = mqtt.connect(clientId, statusTopic, 1, true, will);
        if (connected && mqtt.subscribe(ackTopic, 1)) {
          xQueueReset(outgoing);
          publishStatus("online");
          networkReady.store(true);
          consecutiveFailures = 0;
          Serial.println("# mqtt_conectado: aguardando confirmacao do consumidor");
        } else {
          if (mqtt.connected()) mqtt.disconnect();
          tcpClient.stop();
          Serial.printf("# mqtt_falha estado=%d porta=%u\n", mqtt.state(), fault ? 1 : 1883);
          if (++consecutiveFailures >= 3) {
            // Recupero também uma pilha/rede presa após repetidas falhas TCP.
            // O loop principal continua coletando durante essa recuperação.
            Serial.println("# mqtt_recuperacao: reiniciando WiFi apos tres falhas");
            WiFi.disconnect(false);
            wifiStarted = false;
            consecutiveFailures = 0;
          }
        }
      }
      vTaskDelay(pdMS_TO_TICKS(25));
      continue;
    }
    mqtt.loop();
    networkReady.store(mqtt.connected());
    if (mqtt.connected() && xQueueReceive(outgoing, &request, 0) == pdTRUE) {
      bool sent = mqtt.publish(telemetryTopic, request.body, false);
      Serial.printf("# mqtt_publicacao=%s\n", sent ? "tentada" : "falhou");
      // publish()==true não retira nenhuma leitura da fila.
    }
    vTaskDelay(pdMS_TO_TICKS(10));
  }
}

void collectSample(uint64_t now) {
  TempAndHumidity reading = dht.getTempAndHumidity();
  bool valid = dht.getStatus() == 0 && isfinite(reading.temperature)
      && isfinite(reading.humidity) && reading.temperature >= -40
      && reading.temperature <= 80 && reading.humidity >= 0 && reading.humidity <= 100;
  cardioia::Sample sample{};
  sample.collectedUptimeMs = now;
  sample.sequence = nextSequence++;
  sample.windowMs = static_cast<uint32_t>(now - lastCollection);
  sample.pulseCount = pulseCount;
  sample.heartRateBpm = cardioia::bpm(pulseCount, sample.windowMs);
  sample.temperatureC = reading.temperature;
  sample.humidityPct = reading.humidity;
  sample.dhtValid = valid;
  pulseCount = 0;
  lastCollection = now;
  bool stored = pending->push(sample);
  Serial.printf("# coleta seq=%lu fila=%u perdas=%lu resultado=%s\n",
      static_cast<unsigned long>(sample.sequence), static_cast<unsigned>(pending->size()),
      static_cast<unsigned long>(pending->dropped()), stored ? "armazenada" : "fila_cheia");
}

void scheduleSample(uint64_t now) {
  const auto* sample = pending->front();
  if (!sample || !networkAllowed.load() || !networkReady.load()
      || now - lastScheduled < 150 || !delivery.due(sample->sequence, now)) return;
  StaticJsonDocument<1536> doc;
  doc["schema_version"] = 1;
  doc["device_id"] = DEVICE_ID;
  doc["session_id"] = sessionId;
  doc["sequence"] = sample->sequence;
  doc["collected_uptime_ms"] = sample->collectedUptimeMs;
  doc["window_ms"] = sample->windowMs;
  if (sample->dhtValid) {
    doc["temperature_c"] = sample->temperatureC;
    doc["humidity_pct"] = sample->humidityPct;
  } else { doc["temperature_c"] = nullptr; doc["humidity_pct"] = nullptr; }
  doc["pulse_count"] = sample->pulseCount;
  doc["heart_rate_bpm"] = roundf(sample->heartRateBpm * 100) / 100;
  doc["dht_valid"] = sample->dhtValid;
  doc["dropped_total"] = pending->dropped();
  doc["backlog_samples"] = pending->size();
  doc["simulated"] = true;
  doc["transport"] = "mqtt";
  doc["sent_uptime_ms"] = now;
  doc["age_ms"] = now - sample->collectedUptimeMs;
  doc["attempt"] = delivery.nextAttempt(sample->sequence);
  doc["replay"] = now - sample->collectedUptimeMs > 10000;
  SendRequest request;
  if (doc.overflowed() || measureJson(doc) >= sizeof(request.body)) {
    Serial.println("# erro_serializacao: pendencia preservada");
    return;
  }
  serializeJson(doc, request.body, sizeof(request.body));
  if (xQueueOverwrite(outgoing, &request) == pdPASS) {
    delivery.queued(sample->sequence, now);
    lastScheduled = now;
    Serial.println(request.body);
  }
}

void processSerialCommand() {
  while (Serial.available()) {
    char value = Serial.read();
    if (value == '\n' || value == '\r') {
      serialCommand[serialCommandLength] = '\0';
      if (!strcmp(serialCommand, "broker_off")) {
        brokerFault.store(true);
        Serial.println("# teste_broker: endpoint TCP indisponivel, WiFi permanece ativo");
      } else if (!strcmp(serialCommand, "broker_on")) {
        brokerFault.store(false);
        Serial.println("# teste_broker: endpoint normal restaurado");
      }
      serialCommandLength = 0;
    } else if (serialCommandLength < sizeof(serialCommand) - 1) {
      serialCommand[serialCommandLength++] = value;
    } else { serialCommandLength = 0; }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(PULSE_PIN, INPUT_PULLUP);
  pinMode(CONNECTION_PIN, INPUT_PULLUP);
  pulseButton = cardioia::PulseButton(digitalRead(PULSE_PIN) == LOW);
  dht.setup(DHT_PIN, DHTesp::DHT22);
  snprintf(sessionId, sizeof(sessionId), "%08lx%08lx",
      static_cast<unsigned long>(esp_random()), static_cast<unsigned long>(esp_random()));
  snprintf(telemetryTopic, sizeof(telemetryTopic), "%s/devices/%s/telemetry", TOPIC_ROOT, DEVICE_ID);
  snprintf(ackTopic, sizeof(ackTopic), "%s/devices/%s/ack", TOPIC_ROOT, DEVICE_ID);
  snprintf(statusTopic, sizeof(statusTopic), "%s/devices/%s/status", TOPIC_ROOT, DEVICE_ID);
  // Aloco a fila fixa uma única vez no heap para preservar a DRAM estática do Wi-Fi.
  pending = new (std::nothrow) cardioia::OfflineQueue<QUEUE_CAPACITY>();
  if (!pending) { Serial.println("# erro_fatal: fila sem memoria"); abort(); }
  outgoing = xQueueCreate(1, sizeof(SendRequest));
  incomingAcks = xQueueCreate(8, sizeof(ReceivedAck));
  if (!outgoing || !incomingAcks) { Serial.println("# erro_fatal: canais de rede sem memoria"); abort(); }
  lastCollection = uptimeMs();
  Serial.printf("# CardioIA MQTT sessao=%s capacidade=%u\n", sessionId, static_cast<unsigned>(QUEUE_CAPACITY));
  Serial.printf("# bytes_fila=%u heap_livre=%u\n", static_cast<unsigned>(sizeof(*pending)), ESP.getFreeHeap());
  Serial.println("# Chave direita=online; Serial: broker_off / broker_on");
  Serial.printf("# mqtt_tempos keepalive_s=%u socket_timeout_s=%u\n",
      MQTT_KEEPALIVE_SECONDS, MQTT_SOCKET_TIMEOUT_SECONDS);
  if (xTaskCreatePinnedToCore(networkTask, "cardioia-mqtt", 8192, nullptr, 1, nullptr, 0) != pdPASS) {
    Serial.println("# erro_fatal: tarefa MQTT indisponivel"); abort();
  }
}

void loop() {
  uint64_t now = uptimeMs();
  if (pulseButton.update(digitalRead(PULSE_PIN) == LOW, static_cast<uint32_t>(now))) ++pulseCount;
  bool allowed = digitalRead(CONNECTION_PIN) == HIGH;
  if (allowed != networkAllowed.load()) {
    networkAllowed.store(allowed);
    Serial.printf("# conexao_simulada=%s\n", allowed ? "online" : "offline");
  }
  processSerialCommand();
  ReceivedAck ack;
  while (xQueueReceive(incomingAcks, &ack, 0) == pdTRUE) {
    const auto* head = pending->front();
    if (head && delivery.accepts(head->sequence, ack.sequence) && pending->acknowledge(ack.sequence)) {
      delivery.confirmed();
      Serial.printf("# ack_confirmado seq=%lu fila=%u\n", static_cast<unsigned long>(ack.sequence),
          static_cast<unsigned>(pending->size()));
    } else { Serial.println("# ack_ignorado: sequencia fora da pendencia atual"); }
  }
  if (now - lastCollection >= SAMPLE_INTERVAL_MS) collectSample(now);
  scheduleSample(now);
  delay(1);
}
