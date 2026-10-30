# Incident rehearsal — unknown contact delivery

**Environment:** deterministic, in-memory teaching ledger. This incident was simulated.

## Trigger and observation

Reserve four units for `contact-001`. Simulate a timeout with unknown remote delivery.
Retry the same decision ID. The ledger returns its existing state and keeps the original
reservation. It must not take four more units or issue a second decision for that customer.
Reserve `contact-002`, then reconcile a confirmed non-delivery. Release only that reservation.

## Result

Initial budget: eight. One unknown reservation: four. One confirmed non-delivery refunded: four.
Final available budget: four. No duplicate decision was created. The tests for this
are in `test_ground_truth_lab.py`, and the generated execution records are in `evaluation.json`.

## Recovery boundary

This ledger makes local reservation transactions atomic. It does not call a real delivery
provider, so it cannot promise exactly-once external effects. A real service needs a durable
outbox, provider idempotency keys, acknowledgement reconciliation, access controls, backup
and restoration tests. Keep unknown deliveries reserved until you know their status.

## Follow-up

Before a pilot, test two crashes against the real provider's idempotency and status contract:
one before dispatch, one after the effect but before acknowledgement. Record detection
and recovery times from the real drill. This fixture has no measured production timings.
