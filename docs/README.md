# Data Product Observability Standard

## Executive Summary

Runtime observability metrics for a Bitol ODPS data product, surfaced via the managementPort. SLO fields mirror objectives declared in the linked ODCS output port contracts.

## Schema Details

**Schema Version:** `0.0.1`
**Schema File:** [`../schema/odps-observability-json-schema-v0.0.1.json`](../schema/odps-observability-json-schema-v0.0.1.json)
**Schema ID:** `https://bitol-io.github.io/open-data-product-observability-standard/schema/odps-observability-json-schema-v0.0.1.json`

## Properties

### `schemaVersion`

**Type:** `string` | **Required**

Semantic version of this schema. Consumers should use this for compatibility checks.

**Examples:**
- `0.0.1`

**Pattern:** `^[0-9]+\.[0-9]+\.[0-9]+$`

### `kind`

**Type:** `string` | Optional

The kind of file this is. Valid value is `DataProductObservabilityMetrics`.

**Allowed Values:**
- `DataProductObservabilityMetrics`

### `productId`

**Type:** `string` | **Required**

UUID of the data product as declared in the ODPS

**Examples:**
- `fbe8d147-28db-4f1d-bedf-a3fe9f458427`

### `asOf`

**Type:** `string` | **Required**

ISO 8601 UTC timestamp at which these metrics were collected.

### `period`

**Type:** `string` | **Required**

ISO 8601 duration representing the observation window for rate-based metrics (e.g. query volume, pipeline runs).

**Examples:**
- `PT1H`
- `PT24H`
- `P7D`

**Pattern:** `^P(?:\d+Y)?(?:\d+M)?(?:\d+W)?(?:\d+D)?(?:T(?:\d+H)?(?:\d+M)?(?:\d+S)?)?$`

### `status`

**Type:** `string` | **Required**

Composite any-case health status derived across all dimensions and output ports. Maps directly to the node shading colour in the mesh visualisation.

**Allowed Values:**
- `healthy`
- `degraded`
- `critical`
- `unknown`

### `physical`

**Type:** `object` | Optional

Physical-space metrics (Petrella ch.3): compute, pipeline runtime, and storage — the infrastructure layer beneath the data.

#### `pipeline`

**Type:** `object` | Optional

Most recent pipeline execution for this data product.

##### `lastRunAt`

**Type:** `string | null` | Optional

UTC timestamp when the last pipeline run started.

##### `durationSeconds`

**Type:** `number | null` | Optional

Wall-clock duration of the last run in seconds. Null if the run failed before completion.

##### `status`

**Type:** `string` | **Required**

Terminal or current status of the last pipeline execution.

**Allowed Values:**
- `success`
- `failed`
- `running`
- `skipped`
- `unknown`

##### `errorMessage`

**Type:** `string | null` | Optional

Human-readable error message if status=failed.

##### `recordsProcessed`

**Type:** `integer | null` | Optional

Number of records processed end-to-end by the pipeline in the last run — i.e. records that completed the full source-to-output transformation. Distinct from dynamic.volume.rowCount, which reflects the resulting stored state of the output port. Null if the run failed before completion or if the pipeline does not emit this metric. Aligns with Petrella's physical-space instrumentation of pipeline throughput.

##### `computeCreditsUsed`

**Type:** `number | null` | Optional

Platform-specific compute units consumed (e.g. Databricks DBUs). Null if not applicable or unavailable.

##### `meanTimeBetweenFailuresDays`

**Type:** `number | null` | Optional

MTBF is the average time between repairable failures of a pipeline. Computed from physical.pipeline events: time between status=failed and next status=success.

##### `meanTimeToRecoveryMinutes`

**Type:** `number | null` | Optional

MTTR Mean time to recovery is the average time it takes to recover from an incident. Computed from physical.pipeline events: time between status=failed and next status=success.

#### `storage`

**Type:** `object` | Optional

Physical storage footprint of the data product's output ports.

##### `sizeBytes`

**Type:** `integer | null` | Optional

Total uncompressed bytes across all output port tables/files.

##### `partitionCount`

**Type:** `integer | null` | Optional

Number of physical partitions. Relevant for partitioned tables (e.g. Delta Lake).

### `static`

**Type:** `object` | Optional

Static-space metrics (Petrella ch.4): schema structure and contract conformance — what the data looks like, not what the values are.

#### `schema`

**Type:** `object` | Optional

Schema health relative to the declared ODCS output port contract.

##### `version`

**Type:** `string | null` | Optional

Semantic version of the schema currently in production.

**Examples:**
- `2.3.0`

##### `lastValidatedAt`

**Type:** `string | null` | Optional

UTC timestamp of the last schema validation run against the linked ODCS contract.

##### `driftDetected`

**Type:** `boolean` | Optional

True if the current schema deviates from the version declared in the ODCS contract.

##### `breakingChangeSinceVersion`

**Type:** `string | null` | Optional

If a breaking schema change has been detected, the last known-good schema version. Null otherwise.

**Examples:**
- `2.2.0`
- `None`

##### `columnCount`

**Type:** `integer | null` | Optional

Total number of columns/fields in the primary output port schema.

### `dynamic`

**Type:** `object` | Optional

Dynamic-space metrics (Petrella ch.5): data values, volume, freshness, and quality rules — the runtime fitness of the data itself.

#### `responseTime`

**Type:** `object` | Optional

Query/access latency SLO. Applicable to output ports served via APIs or interactive query engines.

##### `objectiveMs`

**Type:** `number | null` | Optional

Declared maximum p95 response time in milliseconds.

##### `actualP95Ms`

**Type:** `number | null` | Optional

Measured p95 response time in milliseconds over the observation period.

##### `met`

**Type:** `boolean | null` | Optional

True if actualP95Ms <= objectiveMs.

#### `volume`

**Type:** `object` | Optional

Row/record count health. Unexpected volume changes are a leading indicator of upstream issues.

##### `rowCount`

**Type:** `integer | null` | Optional

Current total row count of the primary output port.

##### `rowCountDelta`

**Type:** `integer | null` | Optional

Change in row count over the observation period. Negative values indicate deletion or compaction.

##### `expectedRangeMin`

**Type:** `integer | null` | Optional

Lower bound of the expected row count range for the given period. Derived from historical baselines or ODCS quality rules.

##### `expectedRangeMax`

**Type:** `integer | null` | Optional

Upper bound of the expected row count range.

##### `withinExpectation`

**Type:** `boolean | null` | Optional

True if rowCount falls within [expectedRangeMin, expectedRangeMax]. Null if no expectation is defined.

#### `freshness`

**Type:** `object` | Optional

Data freshness relative to the update frequency SLO declared in the ODCS contract.

##### `lastUpdatedAt`

**Type:** `string | null` | Optional

UTC timestamp of the most recent data write to the primary output port.

##### `lagMinutes`

**Type:** `number | null` | Optional

Current lag in minutes: difference between asOf and lastUpdatedAt.

##### `maxAllowedLagMinutes`

**Type:** `number | null` | Optional

Maximum lag permitted under the ODCS contract SLO. Source of truth for the withinExpectation evaluation.

##### `withinExpectation`

**Type:** `boolean | null` | **Required**

True if lagMinutes <= maxAllowedLagMinutes. Null if no freshness SLO is declared.

#### `quality`

**Type:** `object` | Optional

Data quality rule evaluation results. Rules are defined in the linked ODCS contract and evaluated per-run.

##### `rulesTotal`

**Type:** `integer` | **Required**

Total number of quality rules evaluated in this run.

##### `rulesPassed`

**Type:** `integer` | **Required**

Number of rules that passed.

##### `rulesFailed`

**Type:** `integer` | **Required**

Number of rules that failed.

##### `checks`

**Type:** `array` | Optional

Per-rule detail. Consumers can use this to understand which specific checks are failing.

This is an array of objects with the following properties:

###### `rule`

**Type:** `string` | **Required**

Machine-readable rule identifier, matching the rule name in the ODCS contract.

**Examples:**
- `customer_id_not_null`
- `amount_positive`
- `event_date_not_future`

###### `column`

**Type:** `string | null` | Optional

Column or field the rule applies to. Null for dataset-level rules.

###### `status`

**Type:** `string` | **Required**

Result of this rule evaluation.

**Allowed Values:**
- `passed`
- `failed`
- `warning`
- `skipped`

###### `failRate`

**Type:** `number | null` | Optional

Fraction of rows that violated this rule (0.0–1.0). Null for rules that do not produce a rate.

###### `nullRate`

**Type:** `number | null` | Optional

Fraction of null values in the target column. Populated for not-null rules.

###### `message`

**Type:** `string | null` | Optional

Human-readable explanation for a failed or warning result.

### `outputPorts`

**Type:** `array` | Optional

Per-output-port health breakdown. Each entry corresponds to an outputPort declared in the ODPS YAML, identified by name+version and linked via contractId. Allows consumers to evaluate the health of the specific port they depend on.

This is an array of objects with the following properties:

#### `name`

**Type:** `string` | **Required**

Output port name as declared in the ODPS YAML outputPorts[].name.

**Examples:**
- `rawtransactions`
- `consolidatedtransactions`

#### `version`

**Type:** `string` | **Required**

Output port version as declared in the ODPS YAML outputPorts[].version.

**Examples:**
- `1.0.0`
- `2.0.0`

#### `contractId`

**Type:** `string` | **Required**

ODCS contract UUID as declared in ODPS YAML outputPorts[].contractId. The contract is the authoritative source of SLO objectives and quality rules for this port.

#### `status`

**Type:** `string` | **Required**

Any-case composite health for this specific output port.

**Allowed Values:**
- `healthy`
- `degraded`
- `critical`
- `unknown`

#### `freshness`

**Type:** `object` | Optional

Freshness metrics scoped to this output port.

##### `lastUpdatedAt`

**Type:** `string | null` | Optional

UTC timestamp of the most recent data write to the primary output port.

##### `lagMinutes`

**Type:** `number | null` | Optional

Current lag in minutes: difference between asOf and lastUpdatedAt.

##### `maxAllowedLagMinutes`

**Type:** `number | null` | Optional

Maximum lag permitted under the ODCS contract SLO. Source of truth for the withinExpectation evaluation.

##### `withinExpectation`

**Type:** `boolean | null` | **Required**

True if lagMinutes <= maxAllowedLagMinutes. Null if no freshness SLO is declared.

#### `quality`

**Type:** `object` | Optional

Quality rule results scoped to this output port.

##### `rulesTotal`

**Type:** `integer` | **Required**

Total number of quality rules evaluated in this run.

##### `rulesPassed`

**Type:** `integer` | **Required**

Number of rules that passed.

##### `rulesFailed`

**Type:** `integer` | **Required**

Number of rules that failed.

##### `checks`

**Type:** `array` | Optional

Per-rule detail. Consumers can use this to understand which specific checks are failing.

This is an array of objects with the following properties:

###### `rule`

**Type:** `string` | **Required**

Machine-readable rule identifier, matching the rule name in the ODCS contract.

**Examples:**
- `customer_id_not_null`
- `amount_positive`
- `event_date_not_future`

###### `column`

**Type:** `string | null` | Optional

Column or field the rule applies to. Null for dataset-level rules.

###### `status`

**Type:** `string` | **Required**

Result of this rule evaluation.

**Allowed Values:**
- `passed`
- `failed`
- `warning`
- `skipped`

###### `failRate`

**Type:** `number | null` | Optional

Fraction of rows that violated this rule (0.0–1.0). Null for rules that do not produce a rate.

###### `nullRate`

**Type:** `number | null` | Optional

Fraction of null values in the target column. Populated for not-null rules.

###### `message`

**Type:** `string | null` | Optional

Human-readable explanation for a failed or warning result.

#### `usage`

**Type:** `object` | Optional

Aggregate consumption signals scoped to this output port and its ODCS contract. Answers 'is this contract actively used?' at the port level — complement to the per-consumer breakdown in contractUsage[].

##### `activeConsumers`

**Type:** `integer | null` | Optional

Number of distinct consumers that accessed this output port during the observation period.

##### `queryCount`

**Type:** `integer | null` | Optional

Total queries or API calls against this output port during the observation period.

##### `lastAccessedAt`

**Type:** `string | null` | Optional

UTC timestamp of the most recent consumer access on this output port.

### `lineage`

**Type:** `object` | Optional

Upstream dependency health. Surfaces whether the data products feeding this one are themselves healthy, enabling mesh-level impact analysis.

#### `upstreamProducts`

**Type:** `array` | Optional

This is an array of objects with the following properties:

##### `name`

**Type:** `string` | **Required**

Name of the upstream data product.

**Examples:**
- `payments`
- `orders`

##### `contractId`

**Type:** `string` | **Required**

ODCS contract UUID of the upstream output port this product consumes, as declared in ODPS inputPorts[].contractId.

##### `status`

**Type:** `string` | **Required**

Last known health status of the upstream product. Sourced from that product's own /observe/metrics endpoint.

**Allowed Values:**
- `healthy`
- `degraded`
- `critical`
- `unknown`

##### `lastSeenAt`

**Type:** `string | null` | Optional

UTC timestamp of the last successful data receipt from this upstream product.

### `usage`

**Type:** `object` | Optional

Product-wide consumer usage signals aggregated across all output ports over the observation period. From Implementing Data Mesh: usage metrics demonstrate the data product's value and inform governance decisions. For per-contract and per-consumer breakdowns see outputPorts[].usage and contractUsage[].

#### `activeConsumers`

**Type:** `integer | null` | Optional

Number of distinct consumers that accessed any output port during the observation period.

#### `queryCount`

**Type:** `integer | null` | Optional

Total number of queries or API calls made against all output ports during the observation period.

#### `lastAccessedAt`

**Type:** `string | null` | Optional

UTC timestamp of the most recent consumer access across all output ports.

### `contractUsage`

**Type:** `array` | Optional

Per-consumer, per-contract usage breakdown over the observation period. Provides the finest-grained consumption view: which consumer is hitting which ODCS contract, how often, and whether they are experiencing the SLAs they were promised. Dehghani notes that consumer-reported SLO experience is the ground truth for data product fitness — this array captures that signal explicitly.

This is an array of objects with the following properties:

#### `contractId`

**Type:** `string` | **Required**

ODCS contract UUID identifying which output port contract this consumption record relates to. Matches outputPorts[].contractId.

#### `consumerId`

**Type:** `string` | **Required**

Identifier of the consuming entity — typically the consuming data product ID, service name, or platform identifier as registered in the mesh.

**Examples:**
- `bi-platform`
- `ml-platform`
- `fbe8d147-28db-4f1d-bedf-a3fe9f458427`

#### `queryCount`

**Type:** `integer | null` | Optional

Number of queries or API calls this consumer made against the contract's output port during the observation period.

#### `lastAccessedAt`

**Type:** `string | null` | Optional

UTC timestamp of this consumer's most recent access.

#### `avgResponseTimeMs`

**Type:** `number | null` | Optional

Average query response time in milliseconds experienced by this consumer during the observation period. Consumer-side latency may differ from producer-side SLO measurements due to network or middleware.

#### `p95ResponseTimeMs`

**Type:** `number | null` | Optional

95th percentile response time in milliseconds experienced by this consumer. Primary signal for response time SLO evaluation from the consumer perspective.

#### `sloBreachesReported`

**Type:** `integer | null` | Optional

Number of SLO breaches reported by this consumer against this contract during the observation period. A non-zero value here when the producer's own slo.* shows met=true indicates a perception gap that warrants investigation.

#### `sloBreachDetails`

**Type:** `array` | Optional

Optional detail on each consumer-reported SLO breach. Useful for reconciling producer-observed vs. consumer-experienced fitness.

This is an array of objects with the following properties:

##### `dimension`

**Type:** `string` | **Required**

The SLO dimension the consumer observed as breached.

**Allowed Values:**
- `freshness`
- `quality`
- `responseTime`
- `uptime`

##### `reportedAt`

**Type:** `string` | **Required**

UTC timestamp when the breach was reported or detected.

##### `detail`

**Type:** `string | null` | Optional

Human-readable description of the breach as experienced by the consumer.

### `customProperties`

**Type:** `array` | Optional

Extension point for platform-specific or domain-specific metrics not covered by the standard schema. Mirrors the customProperties pattern used throughout Bitol ODPS.

This is an array of objects with the following properties:

#### `property`

**Type:** `string` | **Required**

Property key, using reverse-DNS namespacing to avoid collisions.

**Examples:**
- `com.myplatform.databricks.clusterName`
- `com.mydomain.regulatory.dataClassification`

#### `value`

**Type:** `any` | **Required**

Property value. Any JSON-serialisable type is permitted.

#### `description`

**Type:** `string | null` | Optional

Human-readable explanation of what this property measures.

