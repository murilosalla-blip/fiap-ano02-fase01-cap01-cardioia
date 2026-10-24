#include <assert.h>
#include <stdio.h>
#include "../firmware/cardioia_edge/edge_core.h"

cardioia::Sample sample(uint32_t sequence) {
  cardioia::Sample result{};
  result.sequence = sequence;
  return result;
}

int main() {
  cardioia::OfflineQueue<3> queue;
  assert(queue.front() == nullptr);
  assert(!queue.acknowledge(1));
  // Offline: armazenar sem confirmar mantém tudo na fila.
  assert(queue.push(sample(1)));
  assert(queue.push(sample(2)));
  assert(queue.push(sample(3)));
  assert(queue.size() == 3);
  assert(!queue.push(sample(4)));
  assert(queue.dropped() == 1);
  assert(queue.front()->sequence == 1);
  // Falha de transporte e ACK incorreto não removem pendência.
  assert(!queue.acknowledge(2));
  assert(queue.size() == 3);
  assert(queue.acknowledge(1));
  assert(!queue.acknowledge(1));
  assert(queue.push(sample(5)));
  const uint32_t recovered[] = {2u, 3u, 5u};
  for (uint32_t sequence : recovered) {
    assert(queue.front()->sequence == sequence);
    assert(queue.acknowledge(sequence));
  }
  assert(queue.front() == nullptr);
  // Múltiplas voltas do buffer, sem mudar a ordem.
  for (uint32_t sequence = 6; sequence < 10006; ++sequence) {
    assert(queue.push(sample(sequence)));
    assert(queue.front()->sequence == sequence);
    assert(queue.acknowledge(sequence));
  }
  assert(queue.dropped() == 1);
  assert(cardioia::bpm(6, 5000) == 72.0f);
  assert(cardioia::bpm(0, 5000) == 0.0f);
  assert(cardioia::bpm(6, 0) == 0.0f);

  cardioia::PulseButton button;
  assert(!button.update(true, 100));
  assert(!button.update(false, 101));
  assert(!button.update(true, 102));
  assert(!button.update(true, 126));
  assert(button.update(true, 127));
  assert(!button.update(true, 500));  // Segurar não repete.
  assert(!button.update(false, 501));
  assert(!button.update(true, 502));  // Repique ao soltar.
  assert(!button.update(false, 503));
  assert(!button.update(false, 528));
  assert(!button.update(true, 600));
  assert(button.update(true, 625));
  // Debounce permanece correto após rollover de millis().
  cardioia::PulseButton rollover;
  assert(!rollover.update(true, UINT32_MAX - 10));
  assert(!rollover.update(true, 13));
  assert(rollover.update(true, 14));

  printf("PASS: FIFO, offline, overflow, ACK incorreto/repetido, wrap, BPM e debounce\n");
  printf("sizeof_sample=%zu; sizeof_queue_2000=%zu\n", sizeof(cardioia::Sample),
      sizeof(cardioia::OfflineQueue<2000>));
}
