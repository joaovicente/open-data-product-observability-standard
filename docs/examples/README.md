# Examples

## Pipeline success

```yaml
schemaVersion: 0.0.1
kind: DataProductObservability
productId: fbe8d147-28db-4f1d-bedf-a3fe9f458427
asOf: '2026-03-14T09:00:00Z'
period: P1D
status: healthy
physical:
  pipeline:
    lastRunAt: '2026-03-13T08:45:00Z'
    durationSeconds: 1200
    status: success
    recordsProcessed: 1000000
    meanTimeBetweenFailuresDays: 12
    meanTimeToRecoveryMinutes: 45
```

## Pipeline failure

```yaml
schemaVersion: 0.0.1
kind: DataProductObservability
productId: fbe8d147-28db-4f1d-bedf-a3fe9f458427
asOf: '2026-03-14T09:00:00Z'
period: P1D
status: critical
physical:
  pipeline:
    lastRunAt: '2026-03-13T08:45:00Z'
    durationSeconds: 1200
    status: failed
    failureReason: 'Spark executor OOM'
    meanTimeBetweenFailuresDays: 12
    meanTimeToRecoveryMinutes: 45
```