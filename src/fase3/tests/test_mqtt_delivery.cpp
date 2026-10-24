#include <assert.h>
#include <stdio.h>
#include "../firmware/cardioia_mqtt/mqtt_delivery.h"

int main() {
  cardioia::DeliveryTracker tracker;
  assert(tracker.due(1, 100));
  assert(!tracker.accepts(1, 1));  // Não aceito ACK de leitura ainda não enviada.
  assert(tracker.nextAttempt(1) == 1);
  tracker.queued(1, 100);
  assert(!tracker.due(1, 3099));
  assert(tracker.due(1, 3100));
  assert(!tracker.accepts(1, 2));
  assert(!tracker.accepts(2, 1));
  assert(tracker.accepts(1, 1));
  assert(tracker.nextAttempt(1) == 2);
  tracker.queued(1, 3100);
  assert(tracker.nextAttempt(1) == 3);
  tracker.confirmed();
  assert(!tracker.accepts(1, 1));  // ACK repetido não libera outra leitura.
  assert(tracker.due(2, 3101));
  assert(tracker.nextAttempt(2) == 1);
  tracker.queued(2, 3101);
  assert(!tracker.accepts(2, 1));
  assert(tracker.accepts(2, 2));
  puts("PASS: confirmacao, timeout, reenvio e ACK incorreto/repetido");
}
