#ifndef CARDIOIA_MQTT_DELIVERY_H
#define CARDIOIA_MQTT_DELIVERY_H
#include <stdint.h>

namespace cardioia {
// Só retiro a cabeça após confirmação de uma tentativa dessa mesma sequência.
// A validação de dispositivo e sessão ocorre antes, no callback MQTT.
class DeliveryTracker {
 public:
  bool due(uint32_t head, uint64_t now) const {
    return !waiting_ || sequence_ != head || now - lastAttempt_ >= 3000;
  }
  uint32_t nextAttempt(uint32_t head) const {
    return waiting_ && sequence_ == head ? attempts_ + 1 : 1;
  }
  void queued(uint32_t sequence, uint64_t now) {
    attempts_ = nextAttempt(sequence);
    sequence_ = sequence;
    waiting_ = true;
    lastAttempt_ = now;
  }
  bool accepts(uint32_t head, uint32_t received) const {
    return waiting_ && sequence_ == head && received == head;
  }
  void confirmed() { waiting_ = false; attempts_ = 0; }
 private:
  bool waiting_ = false;
  uint32_t sequence_ = 0;
  uint32_t attempts_ = 0;
  uint64_t lastAttempt_ = 0;
};
}
#endif
