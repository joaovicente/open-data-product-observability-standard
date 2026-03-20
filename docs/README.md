# Data Product Observability Standard

## Executive Summary

Observability specification compatible with [Bitol ODPS data product specification](https://bitol-io.github.io/open-data-product-standard)

## Schema Details

**Schema Version:** `0.0.1`
**Schema File:** [`odps-observability-json-schema-v0.0.1.json`](../schema/odps-observability-json-schema-v0.0.1.json)

## Fundamentals

### Example

```yaml
schemaVersion: 0.0.1
kind: DataProductObservability
productId: fbe8d147-28db-4f1d-bedf-a3fe9f458427
asOf: '2026-03-14T09:00:00Z'
period: P1D
status: healthy
```

### Field Descriptions

| Key | UX label | Required | Description | Example |
|---|---|---|---|---|
| `schemaVersion` | Schema Version | Yes | Semantic version of this schema. Consumers should use this for compatibility checks. | `0.0.1` |
| `kind` | Kind | Yes | The kind of file this is. Valid value is `DataProductObservability`. | `DataProductObservability` |
| `productId` | Product Id | Yes | UUID of the data product as declared in the ODPS | `fbe8d147-28db-4f1d-bedf-a3fe9f458427` |
| `asOf` | As Of | Yes | [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) UTC timestamp at which these metrics were collected. | `2026-03-14T09:00:00Z` |
| `period` | Period | Yes | [ISO 8601 duration](https://en.wikipedia.org/wiki/ISO_8601#Durations) representing the observation window for rate-based metrics | `P1D` (1 day) `P7D` (7 days) `P1M` (1 month) |
| `status` | Status | Yes | Composite any-case health status derived across all observability dimensions. Valid values: `healthy`, `degraded`, `critical`, `unknown` | `healthy` |

## Physical Metrics

### Examples

Success

```yaml
physical:
  pipeline:
    lastRunAt: '2026-03-13T08:45:00Z'
    durationSeconds: 1200
    status: success
    recordsProcessed: 1000000
    meanTimeBetweenFailuresDays: 12
    meanTimeToRecoveryMinutes: 45
```

Failure

```yaml
physical:
  pipeline:
    lastRunAt: '2026-03-13T08:45:00Z'
    durationSeconds: 1200
    status: failed
    errorMessage: 'Spark executor OOM'
    meanTimeBetweenFailuresDays: 12.5
    meanTimeToRecoveryMinutes: 45.0
```

### Field Descriptions

| Key | UX label | Required | Description | Example |
|---|---|---|---|---|
| `physical` | Physical | No | Object. Physical-space the infrastructure layer beneath the data. |  |
| `physical.pipeline` | Pipeline | No | Object. Most recent pipeline execution for this data product. |  |
| `physical.pipeline.lastRunAt` | Last Run | No | UTC timestamp when the last pipeline run started. | `2026-03-13T08:45:00Z` |
| `physical.pipeline.durationSeconds` | Duration | No | Wall-clock duration of the last run in seconds. Null if the run failed before completion. | `1200` |
| `physical.pipeline.status` | Status | Yes | Terminal or current status of the last pipeline execution. | `success` |
| `physical.pipeline.failureReason` | Failure reason | No | Human-readable error message if status=failed. | `Spark executor OOM` |
| `physical.pipeline.recordsProcessed` | Records Processed | No | Number of records processed end-to-end by the pipeline in the last run. i.e. records that completed the full source-to-output transformation. Null if the run failed before completion or if the pipeline does not emit this metric. | `1000000` |
| `physical.pipeline.meanTimeBetweenFailuresDays` | MTBF (Mean Time Between Failures) | No | MTBF is the average time between repairable failures of a pipeline. Computed from physical.pipeline events: time between status=failed and next status=success. | `12` |
| `physical.pipeline.meanTimeToRecoveryMinutes` | MRRT (Mean Time To Recovery) | No | MTTR Mean time to recovery is the average time it takes to recover from an incident. Computed from physical.pipeline events: time between status=failed and next status=success. | `45` |
