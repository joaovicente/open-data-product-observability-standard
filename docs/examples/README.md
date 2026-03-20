# Examples

## Pipeline success

```yaml
schemaVersion: 1.0.0
productId: fbe8d147-28db-4f1d-bedf-a3fe9f458427
asOf: '2026-03-14T09:00:00Z'
period: PT1D
status: healthy
physical:
  pipeline:
    lastRunAt: '2026-03-13T08:45:00Z'
    durationSeconds: 1200
    status: success
    recordsProcessed: 1000000
    meanTimeBetweenFailuresDays: 12.5
    meanTimeToRecoveryMinutes: 45.0
```

## Pipeline failure

```yaml
schemaVersion: 1.0.0
productId: fbe8d147-28db-4f1d-bedf-a3fe9f458427
asOf: '2026-03-14T09:00:00Z'
period: PT1D
status: critical
physical:
  pipeline:
    lastRunAt: '2026-03-13T08:45:00Z'
    durationSeconds: 1200
    status: failed
    errorMessage: 'Source system unavailable: connection timeout after 30s'
    meanTimeBetweenFailuresDays: 12.5
    meanTimeToRecoveryMinutes: 45.0
```