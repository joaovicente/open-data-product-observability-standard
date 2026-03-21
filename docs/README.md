# Data Product Observability Standard

## Executive Summary

The goal of this standard is to provide a common format for data product observability metrics, fulfilling its observabilty endpoints:

* `{dp}/observe/health` 
* `{dp}/observe/metrics`

The aim is to provide data product level granular metrics, at the following levels:

* data product overall health (e.g. healthy, degraded, critical)
* data product overall metrics (e.g. pipeline health, consumption, etc.)
* data product data contract metrics (e.g. quality, schema conformance, etc.)
* data product output port usage metrics (e.g. number of queries, active user statistics, query response time statistics, etc.)

This standard enables visualisation tools to monitor data product health and drill down into associated metrics and checks.

## Schema Details

**Schema Version:** `0.1.0`
**Schema File:** [`../schema/odps-observability-json-schema-v0.1.0.json`](https://github.com/joaovicente/open-data-product-observability-standard/blob/release/v0.1.0/schema/odps-observability-json-schema-v0.1.0.json)

## Fundamentals

### Example

```yaml
schemaVersion: 0.1.0
kind: DataProductObservability
id: fbe8d147-28db-4f1d-bedf-a3fe9f458427
observedAt: '2026-03-13T09:00:00Z'
period: P1D
health: healthy
```

### Field Descriptions

| Key | UX label | Required | Description | Example |
|---|---|---|---|---|
| `schemaVersion` | Schema Version | Yes | Semantic version of this schema. Consumers should use this for compatibility checks. | `0.1.0` |
| `kind` | Kind | No | The kind of file this is. Valid value is `DataProductObservability`. | `DataProductObservability` |
| `id` | ID | Yes | UUID of the data product as declared in the ODPS | `fbe8d147-28db-4f1d-bedf-a3fe9f458427` |
| `observedAt` | Observed At | Yes | ISO 8601 UTC timestamp at which these metrics were collected. | `2026-03-21T09:00:00Z` |
| `period` | Period | Yes | ISO 8601 duration representing the observation window for rate-based metrics (e.g. query volume, pipeline runs). | `P1D` |
| `health` | Status | Yes | Composite any-case health status derived across all dimensions and output ports. Possible values: `critical`, `degraded`, `healthy`. | `healthy` |
| `source` | Source | No | Object. Source of the metrics. |  |
| `results` | Results | No | Array of objects each with a metric or a check |  |

## Source

### Example

```yaml
source:
  process: customDataProductObserver
```

### Field Descriptions

| Key | UX label | Required | Description | Example |
|---|---|---|---|---|
| `process` | Process | Yes | The process that generated the metrics. | `customDataProductObserver` |


## Results

### Example at product level only

```yaml
results:
  - name: pipelineLastRanAt
    type: metric
    measure:
      value: '2026-03-13T08:45:00Z'
  - name: pipelineDuration
    type: metric
    measure:
      unit: minutes
      value: 1200
  - name: pipelineDurationCheck
    type: check
    status: fail
    severity: warning
    threshold:
      mustBeLessThan: 1000
    measure:
      unit: minutes
      value: 1200
  - name: pipelineLastRunState
    type: metric
    measure:
      value: success
    message: "Spark executor OOM"
  - name: pipelineLastRunStateCheck
    type: check
    status: fail
    threshold:
      validValues: ["success", "skipped"]
    measure:
      value: failed
    message: "Spark executor OOM"
  - name: pipelineRecordsProcessed
    type: metric
    measure:
      value: 100000
  - name: pipelineMeanTimeBetweenFailuresCheck
    type: check
    severity: warning
    status: pass
    threshold:
      mustBeGreaterThan: 5
    measure:
      value: 10
      unit: days
  - name: pipelineMeanTimeToRecoveryCheck
    type: check
    severity: warning
    status: pass
    threshold:
      mustBeLessThan: 2
    measure:
      value: 1
      unit: hours
```

### Example at product and contract level

```yaml
results:
  # Data Product level metrics
  - name: productDataLatencyBeyondSlaCheck
    type: check
    status: pass
    severity: warning
    threshold:
      mustBe: 0 # > 50% of data contracts should be within SLA
    measure:
      unit: percent
      value: 0
  - name: productDataLatencyMaximumAcrossAllContracts
    type: metric
    measure:
      unit: hours
      value: 12
  # Data Contract level metrics
  - name: contractDataLatencySlaCheck
    target:
      resourceType: DataContract
      resourceIdentifier: 123e4567-e89b-12d3-a456-426614174000 # DataContract ID
    type: check
    severity: warning
    status: fail
    threshold:
      mustBeLessThan: 6 # data latency must be less than 6 hours
    measure:
      unit: hours
      value: 12
  - name: contractDataLatencySlaCheck
    target:
      resourceType: DataContract
      resourceIdentifier: 123e4567-e89b-12d3-a456-426614174001 # DataContract ID
    type: check
    severity: warning
    status: pass
    threshold:
      mustBeLessThan: 6 # data latency must be less than 6 hours
    measure:
      unit: hours
      value: 3
```

### Field Descriptions

| Key | UX label | Required | Description | Example |
|---|---|---|---|---|
| `name` | Name | Yes | The name of the metric. | `pipelineLastRanAt` |
| `type` | Type | Yes | The type of the metric. Valid values: `metric`, `check`. When type is `check`, `status` must be provided and `threshold` should also be provided. | `metric` |
| `target` | Target | No | Object. The target of the metric. |  |
| `target.resourceType` | Resource Type | No | The type of the resource. Valid values: `DataProduct`, `DataContract`, `DataContract/schema`, `DataContract/schema/object` | `DataProduct` (implicit unless specified) |
| `target.resourceIdentifier` | Resource Identifier | No | The identifier of the resource. | `DataContract/fbe8d147-28db-4f1d-bedf-a3fe9f458427` (odcs)<br> `fbe8d147-28db-4f1d-bedf-a3fe9f458427/table1` (odcs schema)<br> `fbe8d147-28db-4f1d-bedf-a3fe9f458427/table1/column1` (odcs object)| 
| `measure` | Measure | Yes | Object. The measure of the metric. |  |
| `measure.value` | Value | Yes | The value of the metric. | `2026-03-13T08:45:00Z`, `42`, `success` |
| `measure.unit` | Unit | No | The unit of the metric. | `minutes`, `hours`, `days`, `seconds`, `percent`, `rows` |
| `status` | Status | No | When type is `check`, this is the status of the `check`. Valid values: `pass`, `fail` | `pass` |
| `measure.threshold` | Threshold | No | An object describing the `pass` criteria, valid operators: `mustBe`, `mustNotBe` `mustBeGreaterThan`, `mustBeGreaterOrEqualThan`, `mustBeLessThan`, `mustBeLessOrEqualThan`, `mustBeBetween`, `mustNotBeBetween`,   `validValues`.  | `"mustBe": 100`, `"mustBeBetween": [100, 200]`, `"validValues": ["success", "skipped"]`|
| `severity` | Severity | No | Determines how severe a failed check should be treated as. Valid values: `critical`, `error`, `warning` | `warning` |
| `message` | Message | No | Human-readable message associated with the metric or check. | `Spark executor OOM` |

