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
  - name: dpPipelineLastRunStateCheck
    type: check
    status: pass
    severity: critical
    threshold:
      validValues: ["success"]
    measure:
      value: success
  - name: dpPipelineLastRanAt
    type: metric
    measure:
      value: '2026-03-21 15:09:37.015000+00:00'
  - name: dpPipelineRunDuration
    type: metric
    measure:
      value: 2642
      unit: seconds
  - name: dpPipelineRecordsProcessed
    type: metric
    measure:
      value: 7852
  - name: dpPipelineMeanTimeBetweenFailuresCheck
    type: check
    status: fail
    severity: warning
    threshold:
      mustBeGreaterThan: 5
    measure:
      value: 2
      unit: days
  - name: dpPipelineMeanTimeToRecoveryCheck
    type: check
    status: pass
    severity: warning
    threshold:
      mustBeLessThan: 120
    measure:
      value: 60
      unit: minutes
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
  - name: dpConsumerQueryCount
    type: metric
    measure:
      value: 1476
  - name: dpOutputPortDistinctConsumers
    type: metric
    measure:
      value: 6
  - name: dpOutputPortsResponseTimeCheck
    type: check
    status: pass
    severity: warning
    threshold:
      mustBeGreaterThan: 50
    measure:
      value: 100
      unit: percent
```

## Data Latency metrics

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
  - name: dpDataLatencyMaximum
    type: metric
    measure:
      value: 26
      unit: minutes
  - name: dpDataLatencyCheck
    type: check
    status: pass
    severity: warning
    threshold:
      mustBeLessThan: 60
    measure:
      value: 26
      unit: minutes
```


## Data Quality metrics

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
  - name: dpDataQualityRulesPassCheck
    type: check
    status: pass
    severity: warning
    threshold:
      mustBe: 100
    measure:
      value: 100
      unit: percent
  - name: dcDataQualityRuleCount
    type: metric
    measure:
      value: 10
  - name: dpDataQualityRuleFailCount
    type: metric
    measure:
      value: 0

  # Data Contract level metrics
  - name: dcDataQualityRulesPassCheck
    target:
      resourceType: DataContract
      resourceIdentifier: 123e4567-e89b-12d3-a456-426614174000
    type: check
    status: pass
    severity: warning
    threshold:
      mustBe: 0
    measure:
      unit: percent
      value: 0
  - name: dcDataQualityRuleCount
    target:
      resourceType: DataContract
      resourceIdentifier: 123e4567-e89b-12d3-a456-426614174000
    type: metric
    measure:
      value: 100
  - name: dcDataQualityRuleFailCount
    target:
      resourceType: DataContract
      resourceIdentifier: 123e4567-e89b-12d3-a456-426614174000
    type: metric
    measure:
      value: 0
```