#ifndef CARDIOIA_EDGE_CORE_H
#define CARDIOIA_EDGE_CORE_H

#include <stddef.h>
#include <stdint.h>

namespace cardioia {

struct Sample {
  uint64_t collectedUptimeMs;
  uint32_t sequence;
  uint32_t windowMs;
  uint32_t pulseCount;
  float temperatureC;
  float humidityPct;
  float heartRateBpm;
  bool dhtValid;
};

// Fila circular sem alocação dinâmica. Preserva pendências antigas e rejeita
// novas leituras ao lotar. O contador permite evidenciar as perdas.
template <size_t Capacity>
class OfflineQueue {
 public:
  static_assert(Capacity > 0, "A fila precisa de capacidade positiva");

  bool push(const Sample& sample) {
    if (count_ == Capacity) {
      ++dropped_;
      return false;
    }
    samples_[(head_ + count_) % Capacity] = sample;
    ++count_;
    return true;
  }

  const Sample* front() const {
    return count_ ? &samples_[head_] : nullptr;
  }

  // A camada de transporte decide quando houve confirmação. Uma confirmação
  // atrasada ou fora de ordem nunca remove outra leitura.
  bool acknowledge(uint32_t sequence) {
    if (!count_ || samples_[head_].sequence != sequence) return false;
    head_ = (head_ + 1) % Capacity;
    --count_;
    return true;
  }

  size_t size() const { return count_; }
  uint32_t dropped() const { return dropped_; }

 private:
  Sample samples_[Capacity]{};
  size_t head_ = 0;
  size_t count_ = 0;
  uint32_t dropped_ = 0;
};

// Debounce por estado estável: evita contar repiques tanto na pressão quanto
// na soltura. Cada pressão completa conta uma vez; segurar não gera pulsos.
class PulseButton {
 public:
  explicit PulseButton(bool initiallyPressed = false)
      : raw_(initiallyPressed), stable_(initiallyPressed) {}

  bool update(bool pressed, uint32_t nowMs) {
    if (pressed != raw_) {
      raw_ = pressed;
      changedAt_ = nowMs;
    }
    if (raw_ != stable_ && uint32_t(nowMs - changedAt_) >= 25) {
      stable_ = raw_;
      return stable_;
    }
    return false;
  }

 private:
  bool raw_;
  bool stable_;
  uint32_t changedAt_ = 0;
};

inline float bpm(uint32_t pulses, uint32_t windowMs) {
  return windowMs ? (60000.0f * pulses / windowMs) : 0.0f;
}

}  // namespace cardioia
#endif
