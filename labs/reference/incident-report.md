# Incident rehearsal — unknown contact delivery

**Environment:** deterministic, in-memory teaching ledger. This incident was simulated.

## Trigger and observation

Reserve four units for `contact-001`. Simulate a timeout with unknown remote delivery.
Retry the same decision ID. The ledger returns its existing state and retains the original
reservation. It must not debit four more units or issue a second decision for that customer.
Reserve `contact-002`, then reconcile a confirmed nondelivery; release only that reservation.

## Result

Initial budget: eight. One unknown reservation: four. One confirmed nondelivery refunded: four.
Final available budget: four. No duplicate decision was created. The executable assertions
are in `test_ground_truth_lab.py`; the generated execution records are in `evaluation.json`.

## Recovery boundary

This ledger makes local reservation transactions atomic. It does not call a real delivery
provider and does not promise exactly-once external effects. A real service needs a durable
outbox, provider idempotency keys, acknowledgement reconciliation, access controls, backup
and restoration tests. Keep unknown deliveries reserved until their status is established.

## Follow-up

Before a pilot, test crash-before-dispatch and crash-after-effect-before-acknowledgement
against the real provider's idempotency and status contract. Record detection and recovery
durations from the real drill; this fixture supplies no measured production timings.
