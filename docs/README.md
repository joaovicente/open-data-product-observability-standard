# Data Product Observability Standard

## Executive Summary

Observability specification compatible with [Bitol ODPS data product specification](https://bitol-io.github.io/open-data-product-standard)

## Schema Details

**Schema Version:** `0.0.1`
**Schema File:** [`../schema/odps-observability-json-schema-v0.0.1.json`](../schema/odps-observability-json-schema-v0.0.1.json)

## Fundamentals

### Example

```yaml
schemaVersion: 1.0.0
productId: fbe8d147-28db-4f1d-bedf-a3fe9f458427
asOf: '2026-03-14T09:00:00Z'
period: PT1D
status: critical
```

### Field Descriptions

| Key | UX label | Required | Description | Example |
|---|---|---|---|---|
| `schemaVersion` | Schema Version | Yes | Semantic version of this schema. Consumers should use this for compatibility checks. | `0.0.1` |
| `kind` | Kind | No | The kind of file this is. Valid value is `DataProductObservability`. | `DataProductObservability` |
| `productId` | Product Id | Yes | UUID of the data product as declared in the ODPS | `fbe8d147-28db-4f1d-bedf-a3fe9f458427` |
| `asOf` | As Of | Yes | ISO 8601 UTC timestamp at which these metrics were collected. |  |
| `period` | Period | Yes | ISO 8601 duration representing the observation window for rate-based metrics (e.g. query volume, pipeline runs). | `PT1D` |
| `status` | Status | Yes | Composite any-case health status derived across all dimensions and output ports. Maps directly to the node shading colour in the mesh visualisation. | `healthy` |

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
    errorMessage: 'Source system unavailable: connection timeout after 30s'
    meanTimeBetweenFailuresDays: 12.5
    meanTimeToRecoveryMinutes: 45.0
```

### Field Descriptions

| Key | UX label | Required | Description | Example |
|---|---|---|---|---|
| `physical` | Physical | No | Object. Physical-space metrics (Petrella ch.3): compute, pipeline runtime, and storage — the infrastructure layer beneath the data. |  |
| `physical.pipeline` | Pipeline | No | Object. Most recent pipeline execution for this data product. |  |
| `physical.pipeline.lastRunAt` | Last Run At | No | UTC timestamp when the last pipeline run started. |  |
| `physical.pipeline.durationSeconds` | Duration Seconds | No | Wall-clock duration of the last run in seconds. Null if the run failed before completion. |  |
| `physical.pipeline.status` | Status | Yes | Terminal or current status of the last pipeline execution. | `success` |
| `physical.pipeline.errorMessage` | Error Message | No | Human-readable error message if status=failed. |  |
| `physical.pipeline.recordsProcessed` | Records Processed | No | Number of records processed end-to-end by the pipeline in the last run — i.e. records that completed the full source-to-output transformation. Distinct from dynamic.volume.rowCount, which reflects the resulting stored state of the output port. Null if the run failed before completion or if the pipeline does not emit this metric. Aligns with Petrella's physical-space instrumentation of pipeline throughput. |  |
| `physical.pipeline.computeCreditsUsed` | Compute Credits Used | No | Platform-specific compute units consumed (e.g. Databricks DBUs). Null if not applicable or unavailable. |  |
| `physical.pipeline.meanTimeBetweenFailuresDays` | Mean Time Between Failures Days | No | MTBF is the average time between repairable failures of a pipeline. Computed from physical.pipeline events: time between status=failed and next status=success. |  |
| `physical.pipeline.meanTimeToRecoveryMinutes` | Mean Time To Recovery Minutes | No | MTTR Mean time to recovery is the average time it takes to recover from an incident. Computed from physical.pipeline events: time between status=failed and next status=success. |  |
