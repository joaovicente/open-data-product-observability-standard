# Examples

## Health

Returning health status for the data product<br>
`GET /data-products/{data-product-id}/observe/health`

```yaml
schemaVersion: 0.1.0
kind: DataProductObservability
id: fbe8d147-28db-4f1d-bedf-a3fe9f458427
observedAt: '2026-03-13T09:00:00Z'
period: P1D
health: healthy
```

## Product pipeline metrics

`GET /data-products/{data-product-id}/observe/metrics`

```yaml
schemaVersion: 0.1.0
kind: DataProductObservability
id: fbe8d147-28db-4f1d-bedf-a3fe9f458427
observedAt: '2026-03-13T09:00:00Z'
period: P1D
health: healthy
source:
  process: customDataProductObserver
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
    severity: critical
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
      mustBeMoreThan: 5
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

## Product and output port consumption metrics

`GET /data-products/{data-product-id}/observe/metrics`

```yaml
schemaVersion: 0.1.0
kind: DataProductObservability
id: fbe8d147-28db-4f1d-bedf-a3fe9f458427
observedAt: '2026-03-13T09:00:00Z'
period: P1D
health: healthy
source:
  process: customDataProductObserver
results:
  # Data Product level metrics
  - name: productOutputPortsResponseTimeCheck
    type: check
    status: pass
    severity: warning
    threshold:
      mustBeGreatedThan: 50 # > 50% of data contracts should be within SLA
    measure:
      unit: percent
      value: 100
  - name: productConsumerQueryCount
    type: metric
    measure:
      value: 2509
  # Data Contract level metrics
  - name: outputPortResponseTimeMeanCheck
    target:
      resourceType: DataContract
      resourceIdentifier: 123e4567-e89b-12d3-a456-426614174000 # DataContract ID
    type: check
    status: fail
    severity: warning
    threshold:
      mustBeLessThan: 10000 # Query (mean) response time must be below 10 seconds
    measure:
      unit: seconds
      value: 12000
  - name: outputPortDistinctConsumers
    target:
      resourceType: DataContract
      resourceIdentifier: 123e4567-e89b-12d3-a456-426614174000 # DataContract ID
    type: metric
    measure:
      value: 10
  - name: outputPortQueryCount
    target:
      resourceType: DataContract
      resourceIdentifier: 123e4567-e89b-12d3-a456-426614174000 # DataContract ID
    type: metric
    measure:
      value: 2590
```

## Data Contract latency metrics

`GET /data-products/{data-product-id}/observe/metrics`

```yaml
schemaVersion: 0.1.0
kind: DataProductObservability
id: fbe8d147-28db-4f1d-bedf-a3fe9f458427
observedAt: '2026-03-13T09:00:00Z'
period: P1D
health: healthy
source:
  process: customDataProductObserver
results:
  # Data Product level metrics
  - name: productDataLatencyBeyondSlaCheck
    type: check
    status: pass
    severity: warning
    threshold:
      mustBe: 0 # no table latency should be outside SLA
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


## Data Contract quality

`GET /data-products/{data-product-id}/observe/metrics`

```yaml
schemaVersion: 0.1.0
kind: DataProductObservability
id: fbe8d147-28db-4f1d-bedf-a3fe9f458427
observedAt: '2026-03-13T09:00:00Z'
period: P1D
health: healthy
source:
  process: customDataProductObserver
results:
  # Data Product level metrics
  - name: productDataQualityRulesFailCheck
    type: check
    status: pass
    severity: warning
    threshold:
      mustBe: 0 # no data quality rules should fail
    measure:
      unit: percent
      value: 0
  # Rules aggregated at contract level (odcs schema and object counts rolled up)
  - name: contractDataQualityRuleCount
    target:
      resourceType: DataContract
      resourceIdentifier: 123e4567-e89b-12d3-a456-426614174000
    type: metric
    measure:
      value: 100
  - name: contractDataQualityRuleFailCount
    target:
      resourceType: DataContract
      resourceIdentifier: 123e4567-e89b-12d3-a456-426614174000
    type: metric
    measure:
      value: 0
  - name: contractDataQualityRulesFailCheck
    target:
      resourceType: DataContract
      resourceIdentifier: 123e4567-e89b-12d3-a456-426614174000
    type: check
    status: pass
    severity: warning
    threshold:
      mustBe: 0 # no data quality rules should fail
    measure:
      unit: percent
      value: 0
```