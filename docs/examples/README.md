# Examples

## Example 1

```yaml
schemaVersion: 1.0.0
productId: fbe8d147-28db-4f1d-bedf-a3fe9f458427
asOf: '2026-03-14T09:00:00Z'
period: PT1D
status: critical
physical:
  pipeline:
    lastRunAt: '2026-03-13T08:45:00Z'
    durationSeconds: null
    status: failed
    recordsProcessed: null
    computeCreditsUsed: null
    meanTimeBetweenFailuresDays: 12.5
    meanTimeToRecoveryMinutes: 45.0
    errorMessage: 'Source system unavailable: connection timeout after 30s'
static:
  schema:
    version: 2.3.0
    lastValidatedAt: '2026-03-13T08:00:00Z'
    driftDetected: false
    breakingChangeSinceVersion: null
    columnCount: 24
dynamic:
  volume:
    rowCount: 1042893
    rowCountDelta: 0
    expectedRangeMin: 1000000
    expectedRangeMax: 1100000
    withinExpectation: true
  freshness:
    lastUpdatedAt: '2026-03-13T07:45:00Z'
    lagMinutes: 75
    maxAllowedLagMinutes: 30
    withinExpectation: false
  quality:
    rulesTotal: 12
    rulesPassed: 9
    rulesFailed: 3
    checks:
    - rule: warehouse_id_not_null
      column: warehouse_id
      status: failed
      nullRate: 0.043
      failRate: null
      message: 4.3% of rows have null warehouse_id
    - rule: quantity_positive
      column: quantity
      status: failed
      nullRate: null
      failRate: 0.002
      message: 0.2% of rows have non-positive quantity
    - rule: product_id_ref_check
      column: product_id
      status: failed
      nullRate: null
      failRate: 0.011
      message: 1.1% of product_ids have no match in products table
    - rule: stock_level_not_null
      column: stock_level
      status: passed
      nullRate: 0.0
      failRate: null
      message: null
slo:
  uptime:
    objectivePct: 99.5
    actualPct: 99.9
    windowDays: 30
    met: true
  freshness:
    objectiveMinutes: 30
    actualMinutes: 75
    met: false
  qualityScore:
    objectivePassRate: 1.0
    actualPassRate: 0.75
    met: false
  responseTime: null
outputPorts:
- name: inventory_snapshot
  version: 2.0.0
  contractId: c2798941-1b7e-4b03-9e0d-955b1a872b33
  status: critical
  freshness:
    lastUpdatedAt: '2026-03-13T07:45:00Z'
    lagMinutes: 75
    maxAllowedLagMinutes: 30
    withinExpectation: false
  quality:
    rulesTotal: 12
    rulesPassed: 9
    rulesFailed: 3
    checks: []
  usage:
    activeConsumers: 2
    queryCount: 94
    lastAccessedAt: '2026-03-13T08:58:00Z'
lineage:
  upstreamProducts:
  - name: wms-events
    contractId: dbb7b1eb-7628-436e-8914-2a00638ba6db
    status: critical
    lastSeenAt: '2026-03-13T07:44:00Z'
usage:
  activeConsumers: 4
  queryCount: 187
  lastAccessedAt: '2026-03-13T08:58:00Z'
contractUsage:
- contractId: c2798941-1b7e-4b03-9e0d-955b1a872b33
  consumerId: bi-platform
  queryCount: 134
  lastAccessedAt: '2026-03-13T08:58:00Z'
  avgResponseTimeMs: 143
  p95ResponseTimeMs: 289
  sloBreachesReported: 0
  sloBreachDetails: []
- contractId: c2798941-1b7e-4b03-9e0d-955b1a872b33
  consumerId: ml-platform
  queryCount: 53
  lastAccessedAt: '2026-03-13T07:12:00Z'
  avgResponseTimeMs: 310
  p95ResponseTimeMs: 612
  sloBreachesReported: 1
  sloBreachDetails:
  - dimension: freshness
    reportedAt: '2026-03-13T08:10:00Z'
    detail: "Data not updated after 75 min \xE2\u20AC\u201D pipeline failure not reflected\
      \ in producer SLO status at time of access"
customProperties:
- property: com.myplatform.databricks.clusterName
  value: inventory-pipeline-cluster
  description: Databricks cluster used for pipeline execution

```

