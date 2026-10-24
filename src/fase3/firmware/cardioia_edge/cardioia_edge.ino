// CardioIA Fase 3 — Entrega 1: sensores e fila offline com saída Serial.
// Esta versão NÃO conecta à nuvem. A chave controla conectividade simulada.
#include <Arduino.h>
#include <DHTesp.h>
#include <esp_system.h>
#include <esp_timer.h>
#include <math.h>
#include "edge_core.h"

constexpr int DHT_PIN = 15;
constexpr int PULSE_PIN = 26;
constexpr int CONNECTION_PIN = 27;
constexpr uint32_t SAMPLE_INTERVAL_MS = 5000;
constexpr uint32_t SEND_INTERVAL_MS = 100;
#ifndef CARDIOIA_QUEUE_CAPACITY
#define CARDIOIA_QUEUE_CAPACITY 2000
#endif

DHTesp dht;
cardioia::OfflineQueue<CARDIOIA_QUEUE_CAPACITY> pending;
cardioia::PulseButton pulseButton;
uint64_t lastCollection = 0;
uint64_t lastSend = 0;
uint32_t pulseCount = 0;
uint32_t nextSequence = 1;
char sessionId[24];
bool wasConnected = false;

uint64_t uptimeMs() {
  return static_cast<uint64_t>(esp_timer_get_time()) / 1000;
}

void collectSample(uint64_t now) {
  TempAndHumidity reading = dht.getTempAndHumidity();
  bool valid = dht.getStatus() == 0 && isfinite(reading.temperature)
      && isfinite(reading.humidity) && reading.temperature >= -40
      && reading.temperature <= 80 && reading.humidity >= 0
      && reading.humidity <= 100;
  uint32_t window = static_cast<uint32_t>(now - lastCollection);
  cardioia::Sample sample{};
  sample.collectedUptimeMs = now;
  sample.sequence = nextSequence++;
  sample.windowMs = window;
  sample.pulseCount = pulseCount;
  sample.heartRateBpm = cardioia::bpm(pulseCount, window);
  sample.temperatureC = reading.temperature;
  sample.humidityPct = reading.humidity;
  sample.dhtValid = valid;
  pulseCount = 0;
  lastCollection = now;
  bool stored = pending.push(sample);
  Serial.printf("# coleta seq=%lu fila=%u perdas=%lu resultado=%s\n",
      static_cast<unsigned long>(sample.sequence), static_cast<unsigned>(pending.size()),
      static_cast<unsigned long>(pending.dropped()), stored ? "armazenada" : "fila_cheia");
}

void sendSerialDemo() {
  const cardioia::Sample* sample = pending.front();
  if (!sample) return;
  char temperature[24] = "null";
  char humidity[24] = "null";
  if (sample->dhtValid) {
    snprintf(temperature, sizeof(temperature), "%.2f", sample->temperatureC);
    snprintf(humidity, sizeof(humidity), "%.2f", sample->humidityPct);
  }
  char message[768];
  int length = snprintf(message, sizeof(message),
      "{\"schema_version\":1,\"device_id\":\"cardioia-esp32-01\","
      "\"session_id\":\"%s\",\"sequence\":%lu,\"collected_uptime_ms\":%llu,"
      "\"window_ms\":%lu,\"temperature_c\":%s,\"humidity_pct\":%s,"
      "\"pulse_count\":%lu,\"heart_rate_bpm\":%.2f,\"dht_valid\":%s,"
      "\"dropped_total\":%lu,\"backlog_samples\":%u,\"simulated\":true,"
      "\"transport\":\"serial_demo\"}", sessionId,
      static_cast<unsigned long>(sample->sequence),
      static_cast<unsigned long long>(sample->collectedUptimeMs),
      static_cast<unsigned long>(sample->windowMs), temperature, humidity,
      static_cast<unsigned long>(sample->pulseCount), sample->heartRateBpm,
      sample->dhtValid ? "true" : "false", static_cast<unsigned long>(pending.dropped()),
      static_cast<unsigned>(pending.size()));
  if (length < 0 || static_cast<size_t>(length) >= sizeof(message)) {
    Serial.println("# erro: mensagem excedeu o buffer; pendencia preservada");
    return;
  }
  // Confirma somente escrita no Serial local. Não equivale a ACK MQTT ou
  // persistência em nuvem. A Entrega 2 substituirá este transporte.
  if (Serial.write(reinterpret_cast<const uint8_t*>(message), length)
      == static_cast<size_t>(length)) {
    Serial.println();
    Serial.flush();
    pending.acknowledge(sample->sequence);
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
  lastCollection = uptimeMs();
  Serial.println("# CardioIA Edge: saida SERIAL LOCAL, sem MQTT nesta entrega");
  Serial.println("# Botao B = pulso; chave esquerda = offline; direita = online");
  Serial.printf("# sessao=%s capacidade=%u tamanho_amostra=%u bytes_fila=%u\n",
      sessionId, static_cast<unsigned>(CARDIOIA_QUEUE_CAPACITY),
      static_cast<unsigned>(sizeof(cardioia::Sample)), static_cast<unsigned>(sizeof(pending)));
}

void loop() {
  uint64_t now = uptimeMs();
  if (pulseButton.update(digitalRead(PULSE_PIN) == LOW, static_cast<uint32_t>(now))) {
    ++pulseCount;
  }
  // A variável booleana atende à simulação exigida na Parte 1.
  bool connected = digitalRead(CONNECTION_PIN) == HIGH;
  if (connected != wasConnected) {
    Serial.printf("# conexao_simulada=%s\n", connected ? "online" : "offline");
    wasConnected = connected;
  }
  if (now - lastCollection >= SAMPLE_INTERVAL_MS) collectSample(now);
  if (connected && now - lastSend >= SEND_INTERVAL_MS) {
    lastSend = now;
    sendSerialDemo();
  }
  // Sem espera pela conexão. Pequena pausa libera o processador.
  delay(1);
}
