# Data Product Observability Standard

## Executive Summary

Runtime observability metrics for a Bitol ODPS data product, surfaced via the managementPort. SLO fields mirror objectives declared in the linked ODCS output port contracts.

## Schema Details

**Schema Version:** `0.0.1`
**Schema File:** [`../schema/odps-observability-json-schema-v0.0.1.json`](../schema/odps-observability-json-schema-v0.0.1.json)
**Schema ID:** `https://bitol-io.github.io/open-data-product-observability-standard/schema/odps-observability-json-schema-v0.0.1.json`

## Fundamentals

### Example

```yaml
schemaVersion: 1.0.0
productId: fbe8d147-28db-4f1d-bedf-a3fe9f458427
asOf: '2026-03-13T09:00:00Z'
period: PT1H
status: critical
```

### Field Descriptions

| Key | UX label | Required | Description | Example |
|---|---|---|---|---|
| `schemaVersion` | Schema Version | Yes | Semantic version of this schema. Consumers should use this for compatibility checks. | `0.0.1` |
| `kind` | Kind | No | The kind of file this is. Valid value is `DataProductObservability`. | `DataProductObservability` |
| `productId` | Product Id | Yes | UUID of the data product as declared in the ODPS | `fbe8d147-28db-4f1d-bedf-a3fe9f458427` |
| `asOf` | As Of | Yes | ISO 8601 UTC timestamp at which these metrics were collected. |  |
| `period` | Period | Yes | ISO 8601 duration representing the observation window for rate-based metrics (e.g. query volume, pipeline runs). | `PT1H` |
| `status` | Status | Yes | Composite any-case health status derived across all dimensions and output ports. Maps directly to the node shading colour in the mesh visualisation. | `healthy` |

## Physical Metrics

### Example

```yaml
physical:
  pipeline:
    lastRunAt: '2026-03-13T08:45:00Z'
    durationSeconds: null
    status: failed
    recordsProcessed: null
    computeCreditsUsed: null
    errorMessage: 'Source system unavailable: connection timeout after 30s'
  storage:
    sizeBytes: 2147483648
    partitionCount: 365
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
| `physical.storage` | Storage | No | Object. Physical storage footprint of the data product's output ports. |  |
| `physical.storage.sizeBytes` | Size Bytes | No | Total uncompressed bytes across all output port tables/files. |  |
| `physical.storage.partitionCount` | Partition Count | No | Number of physical partitions. Relevant for partitioned tables (e.g. Delta Lake). |  |

## Static Metrics

### Example

```yaml
static:
  schema:
    version: 2.3.0
    lastValidatedAt: '2026-03-13T08:00:00Z'
    driftDetected: false
    breakingChangeSinceVersion: null
    columnCount: 24
```

### Field Descriptions

| Key | UX label | Required | Description | Example |
|---|---|---|---|---|
| `static` | Static | No | Object. Static-space metrics (Petrella ch.4): schema structure and contract conformance — what the data looks like, not what the values are. |  |
| `static.schema` | Schema | No | Object. Schema health relative to the declared ODCS output port contract. |  |
| `static.schema.version` | Version | No | Semantic version of the schema currently in production. | `2.3.0` |
| `static.schema.lastValidatedAt` | Last Validated At | No | UTC timestamp of the last schema validation run against the linked ODCS contract. |  |
| `static.schema.driftDetected` | Drift Detected | No | True if the current schema deviates from the version declared in the ODCS contract. |  |
| `static.schema.breakingChangeSinceVersion` | Breaking Change Since Version | No | If a breaking schema change has been detected, the last known-good schema version. Null otherwise. | `2.2.0` |
| `static.schema.columnCount` | Column Count | No | Total number of columns/fields in the primary output port schema. |  |

## Dynamic Metrics

### Example

```yaml
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
```

### Field Descriptions

| Key | UX label | Required | Description | Example |
|---|---|---|---|---|
| `dynamic` | Dynamic | No | Object. Dynamic-space metrics (Petrella ch.5): data values, volume, freshness, and quality rules — the runtime fitness of the data itself. |  |
| `dynamic.responseTime` | Response Time | No | Object. Query/access latency SLO. Applicable to output ports served via APIs or interactive query engines. |  |
| `dynamic.responseTime.objectiveMs` | Objective Ms | No | Declared maximum p95 response time in milliseconds. |  |
| `dynamic.responseTime.actualP95Ms` | Actual P95 Ms | No | Measured p95 response time in milliseconds over the observation period. |  |
| `dynamic.responseTime.met` | Met | No | True if actualP95Ms <= objectiveMs. |  |
| `dynamic.volume` | Volume | No | Object. Row/record count health. Unexpected volume changes are a leading indicator of upstream issues. |  |
| `dynamic.volume.rowCount` | Row Count | No | Current total row count of the primary output port. |  |
| `dynamic.volume.rowCountDelta` | Row Count Delta | No | Change in row count over the observation period. Negative values indicate deletion or compaction. |  |
| `dynamic.volume.expectedRangeMin` | Expected Range Min | No | Lower bound of the expected row count range for the given period. Derived from historical baselines or ODCS quality rules. |  |
| `dynamic.volume.expectedRangeMax` | Expected Range Max | No | Upper bound of the expected row count range. |  |
| `dynamic.volume.withinExpectation` | Within Expectation | No | True if rowCount falls within [expectedRangeMin, expectedRangeMax]. Null if no expectation is defined. |  |
| `dynamic.freshness` | Freshness | No | Object. Data freshness relative to the update frequency SLO declared in the ODCS contract. |  |
| `dynamic.freshness.lastUpdatedAt` | Last Updated At | No | UTC timestamp of the most recent data write to the primary output port. |  |
| `dynamic.freshness.lagMinutes` | Lag Minutes | No | Current lag in minutes: difference between asOf and lastUpdatedAt. |  |
| `dynamic.freshness.maxAllowedLagMinutes` | Max Allowed Lag Minutes | No | Maximum lag permitted under the ODCS contract SLO. Source of truth for the withinExpectation evaluation. |  |
| `dynamic.freshness.withinExpectation` | Within Expectation | Yes | True if lagMinutes <= maxAllowedLagMinutes. Null if no freshness SLO is declared. |  |
| `dynamic.quality` | Quality | No | Object. Data quality rule evaluation results. Rules are defined in the linked ODCS contract and evaluated per-run. |  |
| `dynamic.quality.rulesTotal` | Rules Total | Yes | Total number of quality rules evaluated in this run. |  |
| `dynamic.quality.rulesPassed` | Rules Passed | Yes | Number of rules that passed. |  |
| `dynamic.quality.rulesFailed` | Rules Failed | Yes | Number of rules that failed. |  |
| `dynamic.quality.checks[]` | Checks | No | Array of objects. Per-rule detail. Consumers can use this to understand which specific checks are failing. |  |
| `dynamic.quality.checks[].rule` | Rule | Yes | Machine-readable rule identifier, matching the rule name in the ODCS contract. | `customer_id_not_null` |
| `dynamic.quality.checks[].column` | Column | No | Column or field the rule applies to. Null for dataset-level rules. |  |
| `dynamic.quality.checks[].status` | Status | Yes | Result of this rule evaluation. | `passed` |
| `dynamic.quality.checks[].failRate` | Fail Rate | No | Fraction of rows that violated this rule (0.0–1.0). Null for rules that do not produce a rate. |  |
| `dynamic.quality.checks[].nullRate` | Null Rate | No | Fraction of null values in the target column. Populated for not-null rules. |  |
| `dynamic.quality.checks[].message` | Message | No | Human-readable explanation for a failed or warning result. |  |

## Output Ports

### Example

```yaml
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
```

### Field Descriptions

| Key | UX label | Required | Description | Example |
|---|---|---|---|---|
| `outputPorts[]` | Output Ports | No | Array of objects. Per-output-port health breakdown. Each entry corresponds to an outputPort declared in the ODPS YAML, identified by name+version and linked via contractId. Allows consumers to evaluate the health of the specific port they depend on. |  |
| `outputPorts[].name` | Name | Yes | Output port name as declared in the ODPS YAML outputPorts[].name. | `rawtransactions` |
| `outputPorts[].version` | Version | Yes | Output port version as declared in the ODPS YAML outputPorts[].version. | `1.0.0` |
| `outputPorts[].contractId` | Contract Id | Yes | ODCS contract UUID as declared in ODPS YAML outputPorts[].contractId. The contract is the authoritative source of SLO objectives and quality rules for this port. |  |
| `outputPorts[].status` | Status | Yes | Any-case composite health for this specific output port. | `healthy` |
| `outputPorts[].freshness` | Freshness | No | Object. Freshness metrics scoped to this output port. |  |
| `outputPorts[].freshness.lastUpdatedAt` | Last Updated At | No | UTC timestamp of the most recent data write to the primary output port. |  |
| `outputPorts[].freshness.lagMinutes` | Lag Minutes | No | Current lag in minutes: difference between asOf and lastUpdatedAt. |  |
| `outputPorts[].freshness.maxAllowedLagMinutes` | Max Allowed Lag Minutes | No | Maximum lag permitted under the ODCS contract SLO. Source of truth for the withinExpectation evaluation. |  |
| `outputPorts[].freshness.withinExpectation` | Within Expectation | Yes | True if lagMinutes <= maxAllowedLagMinutes. Null if no freshness SLO is declared. |  |
| `outputPorts[].quality` | Quality | No | Object. Quality rule results scoped to this output port. |  |
| `outputPorts[].quality.rulesTotal` | Rules Total | Yes | Total number of quality rules evaluated in this run. |  |
| `outputPorts[].quality.rulesPassed` | Rules Passed | Yes | Number of rules that passed. |  |
| `outputPorts[].quality.rulesFailed` | Rules Failed | Yes | Number of rules that failed. |  |
| `outputPorts[].quality.checks[]` | Checks | No | Array of objects. Per-rule detail. Consumers can use this to understand which specific checks are failing. |  |
| `outputPorts[].quality.checks[].rule` | Rule | Yes | Machine-readable rule identifier, matching the rule name in the ODCS contract. | `customer_id_not_null` |
| `outputPorts[].quality.checks[].column` | Column | No | Column or field the rule applies to. Null for dataset-level rules. |  |
| `outputPorts[].quality.checks[].status` | Status | Yes | Result of this rule evaluation. | `passed` |
| `outputPorts[].quality.checks[].failRate` | Fail Rate | No | Fraction of rows that violated this rule (0.0–1.0). Null for rules that do not produce a rate. |  |
| `outputPorts[].quality.checks[].nullRate` | Null Rate | No | Fraction of null values in the target column. Populated for not-null rules. |  |
| `outputPorts[].quality.checks[].message` | Message | No | Human-readable explanation for a failed or warning result. |  |
| `outputPorts[].usage` | Usage | No | Object. Aggregate consumption signals scoped to this output port and its ODCS contract. Answers 'is this contract actively used?' at the port level — complement to the per-consumer breakdown in contractUsage[]. |  |
| `outputPorts[].usage.activeConsumers` | Active Consumers | No | Number of distinct consumers that accessed this output port during the observation period. |  |
| `outputPorts[].usage.queryCount` | Query Count | No | Total queries or API calls against this output port during the observation period. |  |
| `outputPorts[].usage.lastAccessedAt` | Last Accessed At | No | UTC timestamp of the most recent consumer access on this output port. |  |

## Lineage

### Example

```yaml
lineage:
  upstreamProducts:
  - name: wms-events
    contractId: dbb7b1eb-7628-436e-8914-2a00638ba6db
    status: critical
    lastSeenAt: '2026-03-13T07:44:00Z'
```

### Field Descriptions

| Key | UX label | Required | Description | Example |
|---|---|---|---|---|
| `lineage` | Lineage | No | Object. Upstream dependency health. Surfaces whether the data products feeding this one are themselves healthy, enabling mesh-level impact analysis. |  |
| `lineage.upstreamProducts[]` | Upstream Products | No | Array of objects.  |  |
| `lineage.upstreamProducts[].name` | Name | Yes | Name of the upstream data product. | `payments` |
| `lineage.upstreamProducts[].contractId` | Contract Id | Yes | ODCS contract UUID of the upstream output port this product consumes, as declared in ODPS inputPorts[].contractId. |  |
| `lineage.upstreamProducts[].status` | Status | Yes | Last known health status of the upstream product. Sourced from that product's own /observe/metrics endpoint. | `healthy` |
| `lineage.upstreamProducts[].lastSeenAt` | Last Seen At | No | UTC timestamp of the last successful data receipt from this upstream product. |  |

## Usage

### Example

```yaml
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
```

### Field Descriptions

| Key | UX label | Required | Description | Example |
|---|---|---|---|---|
| `usage` | Usage | No | Object. Product-wide consumer usage signals aggregated across all output ports over the observation period. From Implementing Data Mesh: usage metrics demonstrate the data product's value and inform governance decisions. For per-contract and per-consumer breakdowns see outputPorts[].usage and contractUsage[]. |  |
| `usage.activeConsumers` | Active Consumers | No | Number of distinct consumers that accessed any output port during the observation period. |  |
| `usage.queryCount` | Query Count | No | Total number of queries or API calls made against all output ports during the observation period. |  |
| `usage.lastAccessedAt` | Last Accessed At | No | UTC timestamp of the most recent consumer access across all output ports. |  |
| `contractUsage[]` | Contract Usage | No | Array of objects. Per-consumer, per-contract usage breakdown over the observation period. Provides the finest-grained consumption view: which consumer is hitting which ODCS contract, how often, and whether they are experiencing the SLAs they were promised. Dehghani notes that consumer-reported SLO experience is the ground truth for data product fitness — this array captures that signal explicitly. |  |
| `contractUsage[].contractId` | Contract Id | Yes | ODCS contract UUID identifying which output port contract this consumption record relates to. Matches outputPorts[].contractId. |  |
| `contractUsage[].consumerId` | Consumer Id | Yes | Identifier of the consuming entity — typically the consuming data product ID, service name, or platform identifier as registered in the mesh. | `bi-platform` |
| `contractUsage[].queryCount` | Query Count | No | Number of queries or API calls this consumer made against the contract's output port during the observation period. |  |
| `contractUsage[].lastAccessedAt` | Last Accessed At | No | UTC timestamp of this consumer's most recent access. |  |
| `contractUsage[].avgResponseTimeMs` | Avg Response Time Ms | No | Average query response time in milliseconds experienced by this consumer during the observation period. Consumer-side latency may differ from producer-side SLO measurements due to network or middleware. |  |
| `contractUsage[].p95ResponseTimeMs` | P95 Response Time Ms | No | 95th percentile response time in milliseconds experienced by this consumer. Primary signal for response time SLO evaluation from the consumer perspective. |  |
| `contractUsage[].sloBreachesReported` | Slo Breaches Reported | No | Number of SLO breaches reported by this consumer against this contract during the observation period. A non-zero value here when the producer's own slo.* shows met=true indicates a perception gap that warrants investigation. |  |
| `contractUsage[].sloBreachDetails[]` | Slo Breach Details | No | Array of objects. Optional detail on each consumer-reported SLO breach. Useful for reconciling producer-observed vs. consumer-experienced fitness. |  |
| `contractUsage[].sloBreachDetails[].dimension` | Dimension | Yes | The SLO dimension the consumer observed as breached. | `freshness` |
| `contractUsage[].sloBreachDetails[].reportedAt` | Reported At | Yes | UTC timestamp when the breach was reported or detected. |  |
| `contractUsage[].sloBreachDetails[].detail` | Detail | No | Human-readable description of the breach as experienced by the consumer. |  |

## Custom Properties

### Example

```yaml
customProperties:
- property: com.myplatform.databricks.clusterName
  value: inventory-pipeline-cluster
  description: Databricks cluster used for pipeline execution
```

### Field Descriptions

| Key | UX label | Required | Description | Example |
|---|---|---|---|---|
| `customProperties[]` | Custom Properties | No | Array of objects. Extension point for platform-specific or domain-specific metrics not covered by the standard schema. Mirrors the customProperties pattern used throughout Bitol ODPS. |  |
| `customProperties[].property` | Property | Yes | Property key, using reverse-DNS namespacing to avoid collisions. | `com.myplatform.databricks.clusterName` |
| `customProperties[].value` | Value | Yes | Property value. Any JSON-serialisable type is permitted. |  |
| `customProperties[].description` | Description | No | Human-readable explanation of what this property measures. |  |

