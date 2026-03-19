# Scenario 02: Competitive Landscape — Enterprise Data Platform Selection

## Parameters

- **audience**: VP of Engineering and CTO making a platform decision
- **audience_type**: executive
- **purpose**: decide
- **tone**: executive
- **output_format**: html
- **theme**: dark-keynote
- **presentation_mode**: slides
- **include_speaker_notes**: true
- **include_appendix**: true

## Expected Framework

SCQA -> Pyramid (decision variant — recommendation as Answer)

## Source Material

COMPETITIVE ANALYSIS OUTPUT
Specialist: competitive-analysis / Version: 1.0
Comparison type: head-to-head
Subjects: Snowflake, Databricks, BigQuery
Dimensions: 8
Quality score: 0.84

COMPETITIVE ANALYSIS BRIEF
Three leading enterprise data platforms compared across cost, performance, ecosystem integration, governance, real-time capabilities, ML/AI support, migration complexity, and vendor lock-in risk. Snowflake leads on ease of use and separation of compute/storage, Databricks dominates the ML/AI pipeline story with Unity Catalog governance, and BigQuery offers the strongest serverless economics for Google Cloud-native organizations. The decision hinges on whether the organization prioritizes ML-first workflows (Databricks), SQL-first analytics (Snowflake), or serverless cost efficiency with existing GCP investment (BigQuery).

COMPARISON MATRIX

subject: Snowflake | dimension: Cost Model | rating: strong | evidence: "Per-second billing with automatic suspension. Virtual warehouse pricing ranges from $2-$128/credit depending on edition. Typical enterprise spend: $15-40K/month for mid-scale deployments. Storage billed separately at $23-40/TB/month." | confidence: high
subject: Databricks | dimension: Cost Model | rating: moderate | evidence: "DBU-based pricing varies by workload type. SQL Warehouse costs $0.22-0.55/DBU. Jobs compute at $0.07-0.40/DBU. Unity Catalog adds per-table governance costs. Total cost can exceed Snowflake by 20-35% for pure analytics workloads but is 15-25% cheaper for ML-heavy pipelines." | confidence: high
subject: BigQuery | dimension: Cost Model | rating: strong | evidence: "On-demand pricing at $6.25/TB scanned. Flat-rate slots at $2,000/month per 100 slots. Serverless model eliminates idle compute costs entirely. Most cost-effective for intermittent/burst workloads. Storage at $0.02/GB/month with automatic tiering." | confidence: high

subject: Snowflake | dimension: Query Performance | rating: strong | evidence: "Consistently top-tier for complex SQL workloads. Automatic query optimization with adaptive execution. Multi-cluster warehouses enable workload isolation. P95 query latency under 3 seconds for typical dashboard queries in benchmarks." | confidence: high
subject: Databricks | dimension: Query Performance | rating: strong | evidence: "Photon engine delivers 2-5x speedup over Spark SQL for most workloads. Delta Lake ACID transactions add overhead but provide consistency. SQL Warehouse performance now competitive with Snowflake for standard BI queries." | confidence: medium
subject: BigQuery | dimension: Query Performance | rating: moderate | evidence: "Serverless architecture introduces variable latency. Slot-based model can create contention under heavy concurrent load. Excellent for large-scale batch processing. BI Engine provides sub-second caching for repeated queries." | confidence: high

subject: Snowflake | dimension: ML/AI Integration | rating: moderate | evidence: "Snowpark enables Python/Java/Scala UDFs running natively. ML model deployment via Snowflake ML Functions is GA but limited compared to Databricks. Snowflake Cortex provides managed LLM access. Lacks native notebook experience — requires external tools." | confidence: high
subject: Databricks | dimension: ML/AI Integration | rating: strong | evidence: "Native MLflow integration for experiment tracking and model registry. Managed notebook experience. Feature Store integrated with Unity Catalog. GPU-attached clusters for training. Most complete ML lifecycle platform of the three. Model Serving for real-time inference." | confidence: high
subject: BigQuery | dimension: ML/AI Integration | rating: moderate | evidence: "BigQuery ML enables SQL-based model training for common algorithms. Vertex AI integration for advanced ML. Less cohesive than Databricks — requires moving between products. AutoML capabilities are strong for non-ML-engineers." | confidence: medium

subject: Snowflake | dimension: Data Governance | rating: strong | evidence: "Row-level and column-level security. Dynamic data masking. Object tagging and classification. Comprehensive access history and audit logging. Tag-based governance policies. Snowflake Horizon provides data discovery." | confidence: high
subject: Databricks | dimension: Data Governance | rating: strong | evidence: "Unity Catalog provides centralized governance across all data assets. Fine-grained ACLs, lineage tracking, and data classification. Audit logging. Most comprehensive metadata management of the three. Row and column level filtering with Delta Sharing." | confidence: high
subject: BigQuery | dimension: Data Governance | rating: moderate | evidence: "Column-level security and data masking via policy tags. Relies on broader Google Cloud IAM which adds complexity. Data Catalog for discovery. Audit logging through Cloud Audit Logs. Less granular than Snowflake or Databricks native offerings." | confidence: medium

subject: Snowflake | dimension: Real-time Capabilities | rating: moderate | evidence: "Snowpipe for continuous micro-batch ingestion (latency: 1-2 minutes). Dynamic Tables for incremental materialization. No true streaming engine — requires Kafka/Spark/Flink in front for sub-minute latency." | confidence: high
subject: Databricks | dimension: Real-time Capabilities | rating: strong | evidence: "Native Structured Streaming on Spark. Delta Live Tables for declarative ETL pipelines with streaming support. Sub-second latency achievable. Most mature streaming story of the three platforms." | confidence: high
subject: BigQuery | dimension: Real-time Capabilities | rating: moderate | evidence: "BigQuery streaming insert API for real-time ingestion. Dataflow (Apache Beam) for stream processing. BigQuery subscriptions from Pub/Sub. Good but requires orchestrating multiple GCP services." | confidence: medium

subject: Snowflake | dimension: Ecosystem Integration | rating: strong | evidence: "400+ technology partners. Native connectors for all major BI tools, ETL platforms, and data integration services. Snowflake Marketplace for third-party data. Broad ISV ecosystem." | confidence: high
subject: Databricks | dimension: Ecosystem Integration | rating: strong | evidence: "Open-source foundation (Spark, Delta Lake, MLflow) ensures broad compatibility. Delta Sharing for cross-platform data sharing. Growing marketplace. Strong DevOps integration with Terraform and CI/CD tools." | confidence: high
subject: BigQuery | dimension: Ecosystem Integration | rating: moderate | evidence: "Excellent within Google Cloud ecosystem. Looker integration is seamless. Third-party tool support is good but narrower than Snowflake. BigQuery Omni extends to AWS/Azure but with limitations." | confidence: medium

subject: Snowflake | dimension: Migration Complexity | rating: strong | evidence: "SQL-based interface minimizes retraining. SnowConvert tool assists automated migration from Teradata, Oracle, Netezza. Separation of storage/compute simplifies phased migration. Typical enterprise migration: 3-6 months." | confidence: medium
subject: Databricks | dimension: Migration Complexity | rating: moderate | evidence: "Steeper learning curve for teams without Spark experience. Migration from SQL-centric platforms requires workflow redesign. Unity Catalog migration for existing Databricks users is non-trivial. Typical migration: 4-8 months." | confidence: medium
subject: BigQuery | dimension: Migration Complexity | rating: moderate | evidence: "BigQuery Migration Service assists from Teradata, Redshift, Netezza. SQL dialect differences require query rewrites. Tight GCP coupling means organizational commitment to Google Cloud is prerequisite. Typical migration: 3-7 months." | confidence: medium

subject: Snowflake | dimension: Vendor Lock-in Risk | rating: moderate | evidence: "Proprietary platform with multi-cloud deployment. Data is accessible but workloads are not portable. Iceberg Tables support provides some openness. No on-premises option." | confidence: high
subject: Databricks | dimension: Vendor Lock-in Risk | rating: strong | evidence: "Open-source core (Spark, Delta Lake, MLflow) significantly reduces lock-in. Delta Lake format is open. Unity Catalog is open-sourced. Can run on any major cloud. Strongest portability story of the three." | confidence: high
subject: BigQuery | dimension: Vendor Lock-in Risk | rating: weak | evidence: "Tightly coupled to Google Cloud. BigQuery Omni provides limited multi-cloud access. Proprietary storage format. Migration away requires significant effort. Highest lock-in risk of the three platforms." | confidence: high

PROFILES
subject: Snowflake | primary_advantage: Best-in-class SQL analytics with the simplest operational model — zero tuning, instant scaling, and a mature governance story that requires no data engineering expertise | weakness: ML/AI workflows require bolting on external tools; no true streaming capability; premium pricing for pure compute
subject: Databricks | primary_advantage: Most complete data + AI platform with the strongest open-source commitment — native ML lifecycle, streaming, and governance in a single unified lakehouse architecture | weakness: Higher learning curve for SQL-centric teams; cost unpredictability for mixed workloads; Unity Catalog migration complexity for existing users
subject: BigQuery | primary_advantage: Most cost-efficient serverless model for burst/intermittent workloads with seamless Looker and Vertex AI integration for Google Cloud-native organizations | weakness: Highest vendor lock-in risk; governance relies on broader GCP IAM adding complexity; ecosystem integration narrower outside Google Cloud

WIN CONDITIONS
subject: Snowflake | wins_when: Organization is SQL-first with a mature BI practice, needs multi-cloud deployment flexibility, and values operational simplicity over ML pipeline depth | loses_when: Primary use case is ML/AI model training and deployment, or organization needs true sub-second streaming
subject: Databricks | wins_when: Organization's strategic direction is data + AI convergence, engineering team has Python/Spark skills, and real-time streaming is a core requirement | loses_when: Team is primarily SQL analysts without engineering support, or workloads are predominantly BI dashboards and ad-hoc queries
subject: BigQuery | wins_when: Organization is already invested in Google Cloud, workloads are intermittent/burst, and serverless cost economics are the top priority | loses_when: Multi-cloud strategy is important, or organization needs fine-grained governance beyond what GCP IAM provides

POSITIONING GAPS
gap: No platform fully addresses the hybrid transactional-analytical processing (HTAP) use case without significant architectural workarounds | benefits: Databricks (closest with Delta Lake ACID)
gap: Edge computing and IoT data processing is not a core strength of any platform — all require additional services | benefits: Databricks (Spark Streaming closest fit)
gap: Cost transparency and predictability remains a challenge across all three — customers consistently report bill surprise | benefits: Snowflake (most transparent credit model)

EVIDENCE GAPS
dimension: Total Cost of Ownership | reason: Long-term TCO comparisons beyond 12 months are scarce; most benchmarks are vendor-funded
dimension: Migration Success Rate | reason: No independent data on migration project success rates or timeline accuracy across platforms
dimension: Customer Satisfaction | reason: NPS and satisfaction data is vendor-reported; no independent survey found for 2025

QUALITY THRESHOLD RESULT: MET
