# Software Engineering & Machine Learning Lifecycle Keywords

## Context
Comprehensive reference of industry-standard keywords, skills, technologies, platforms, tools, best practices, and industry standards across the full software engineering and machine learning lifecycles.

---

## Software Engineering Lifecycle (SDLC)

### Methodologies & Frameworks
- Agile (Scrum, Kanban, Scrumban, SAFe, LeSS, Nexus, Disciplined Agile)
- Waterfall, V-Model, Spiral, Incremental, Iterative
- DevOps, DevSecOps, GitOps, ChatOps, AIOps
- SRE (Site Reliability Engineering), Platform Engineering
- Lean Software Development, Theory of Constraints
- Extreme Programming (XP), Pair Programming, Mob Programming
- Test-Driven Development (TDD), Behavior-Driven Development (BDD), Acceptance Test-Driven Development (ATDD)
- Domain-Driven Design (DDD), Bounded Contexts, Ubiquitous Language, Aggregates
- Shape Up (Basecamp), Crystal, Feature-Driven Development (FDD), DSDM
- Continuous Improvement / Kaizen, Retrospectives
- DORA Metrics (Deployment Frequency, Lead Time, Change Failure Rate, MTTR)
- Value Stream Mapping, Flow Efficiency

### Requirements & Planning
- Requirements Engineering, Requirements Gathering, Requirements Traceability
- User Stories, Epics, Themes, Acceptance Criteria, Definition of Done (DoD), Definition of Ready (DoR)
- Product Backlog Refinement / Grooming, Story Point Estimation, T-Shirt Sizing
- Sprint Planning, Sprint Review, Sprint Retrospective, Daily Standup
- Capacity Planning, Resource Planning, Roadmap Planning
- Stakeholder Analysis, Business Requirements Document (BRD), Product Requirements Document (PRD)
- Functional Requirements, Non-Functional Requirements (NFRs), Quality Attributes
- Technical Specifications, Architecture Decision Records (ADRs), Technical Design Documents (TDD)
- Risk Assessment, Risk Mitigation, Feasibility Analysis
- OKRs (Objectives & Key Results), KPIs, North Star Metrics
- Story Mapping, Event Storming, Impact Mapping
- MoSCoW Prioritization (Must/Should/Could/Won't), RICE Scoring, Weighted Shortest Job First (WSJF)
- Jobs-to-be-Done (JTBD) Framework
- Dependency Management, Critical Path Analysis

### Design & Architecture
- System Design, High-Level Design (HLD), Low-Level Design (LLD)
- Microservices Architecture, Monolithic Architecture, Modular Monolith
- Service-Oriented Architecture (SOA), Service Mesh (Istio, Linkerd, Consul Connect)
- Event-Driven Architecture (EDA), CQRS (Command Query Responsibility Segregation), Event Sourcing
- Hexagonal Architecture (Ports & Adapters), Clean Architecture, Onion Architecture, Layered Architecture
- Serverless Architecture, Function-as-a-Service (FaaS)
- API Design: REST, GraphQL, gRPC, WebSocket, Server-Sent Events (SSE), Webhook
- API Versioning, API Rate Limiting, API Throttling, API Gateway Pattern
- Design Patterns: Creational (Factory, Abstract Factory, Builder, Singleton, Prototype), Structural (Adapter, Bridge, Composite, Decorator, Facade, Proxy), Behavioral (Observer, Strategy, Command, State, Template Method, Chain of Responsibility, Mediator, Iterator, Visitor)
- Distributed Systems Patterns: Circuit Breaker, Bulkhead, Retry with Backoff, Saga Pattern, Outbox Pattern, Strangler Fig, Sidecar, Ambassador, Anti-Corruption Layer
- Backend-for-Frontend (BFF), API Composition, API Aggregation
- SOLID Principles, DRY, KISS, YAGNI, Separation of Concerns, Law of Demeter
- UML Diagrams, Sequence Diagrams, Entity-Relationship Diagrams, C4 Model (Context, Container, Component, Code)
- Domain Modeling, Data Modeling, Object-Relational Mapping (ORM)
- Scalability (Horizontal, Vertical), High Availability (HA), Fault Tolerance, Graceful Degradation
- Load Balancing (Round Robin, Least Connections, Consistent Hashing), Reverse Proxy (Nginx, HAProxy, Envoy, Traefik)
- Caching Strategies (Write-Through, Write-Behind, Cache-Aside/Lazy Loading, Read-Through), Cache Invalidation (TTL, Event-Driven)
- Caching Technologies: Redis, Memcached, Varnish, CDN (CloudFront, Cloudflare, Fastly, Akamai)
- Message Queues / Event Streaming: Apache Kafka, RabbitMQ, Amazon SQS/SNS, Google Pub/Sub, Azure Service Bus, Apache Pulsar, NATS, ZeroMQ
- Distributed Consensus (Raft, Paxos), Leader Election
- Idempotency, Exactly-Once Delivery, At-Least-Once, At-Most-Once
- Data Partitioning, Sharding Strategies (Range, Hash, Directory-Based)
- Workflow Orchestration (Temporal, Cadence, Step Functions, Argo Workflows)
- Multi-Tenancy, Tenant Isolation
- Twelve-Factor App Methodology
- Reactive Systems, Reactive Programming (RxJava, RxJS, Project Reactor)
- Asynchronous Processing, Non-Blocking I/O, Event Loop

### Development & Implementation
- Version Control (Git, GitHub, GitLab, Bitbucket, Azure DevOps Repos)
- Branching Strategies: GitFlow, Trunk-Based Development, GitHub Flow, Release Branching, Feature Branching
- Feature Flags / Feature Toggles (LaunchDarkly, Flagsmith, Unleash, Split.io)
- Code Review, Pull Requests, Merge Requests, Pair Programming, Mob Programming, Code Owners
- Clean Code, Refactoring Patterns (Extract Method, Inline, Rename, Move, Introduce Parameter Object)
- Technical Debt Management, Tech Debt Quadrant (Reckless/Prudent × Deliberate/Inadvertent)
- Linting (ESLint, Pylint, Flake8, Ruff, golangci-lint), Formatting (Prettier, Black, gofmt, clang-format)
- Pre-Commit Hooks, Husky, lint-staged, Conventional Commits (Commitlint)
- IDE Proficiency, Debugging, Profiling, Performance Optimization
- Containerization (Docker, Podman, Buildah, containerd)
- Container Orchestration (Kubernetes, Amazon ECS/EKS, Docker Swarm, Nomad)
- Kubernetes Ecosystem: Helm, Kustomize, Operators, CRDs, Ingress Controllers, Service Mesh
- Infrastructure as Code (Terraform, Pulumi, CloudFormation, AWS CDK, Crossplane, Bicep)
- Configuration Management (Ansible, Chef, Puppet, SaltStack)
- Secret Management (HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, SOPS, sealed-secrets)
- Monorepo Tools (Turborepo, Nx, Bazel, Lerna, Rush)
- Dependency Management, Lock Files, Reproducible Builds
- Environment Management (dotenv, direnv, nvm, pyenv, asdf)

### Programming Languages & Ecosystems
- Python, Java, Go, Rust, C, C++, JavaScript, TypeScript, C#, Kotlin, Swift, Ruby, Scala, Elixir, Haskell, R, Julia, Dart, Lua, PHP, Perl
- Backend Frameworks: Spring Boot, Django, Flask, FastAPI, Express.js, NestJS, Gin, Echo, Fiber, ASP.NET, Rails, Phoenix, Actix
- Frontend Frameworks: React, Angular, Vue.js, Svelte, SolidJS, Astro, Remix, Next.js, Nuxt.js, Gatsby
- Mobile: React Native, Flutter, Swift/SwiftUI, Kotlin/Jetpack Compose, Xamarin
- Package Management: pip/Poetry/uv/Conda, npm/yarn/pnpm/Bun, Maven/Gradle, Cargo, Go Modules, NuGet, Gem, CocoaPods/SPM
- Build Systems: Make, CMake, Bazel, Webpack, Vite, esbuild, Rollup, Turbopack, Gradle, Maven, Cargo
- Runtime Environments: Node.js, Deno, Bun, JVM (JDK), .NET Runtime, WASM/WASI
- Data Serialization: JSON, Protocol Buffers (Protobuf), Avro, Thrift, MessagePack, CBOR, YAML, TOML
- File Formats: Parquet, ORC, Arrow (columnar), CSV, HDF5, NetCDF, JSONL/NDJSON

### Testing & Quality Assurance
- Unit Testing, Integration Testing, End-to-End (E2E) Testing, Component Testing
- System Testing, Regression Testing, Smoke Testing, Sanity Testing
- Performance Testing, Load Testing, Stress Testing, Soak/Endurance Testing, Spike Testing
- Performance Tools: JMeter, Locust, k6, Gatling, Artillery, Vegeta, wrk, Apache Bench
- Security Testing: SAST (Static Application Security Testing), DAST (Dynamic Application Security Testing), IAST (Interactive AST), SCA (Software Composition Analysis), Penetration Testing, Fuzz Testing (AFL, libFuzzer, OSS-Fuzz)
- Chaos Engineering (Chaos Monkey, Litmus, Gremlin, Chaos Mesh, Toxiproxy)
- Contract Testing (Pact, Spring Cloud Contract), Consumer-Driven Contracts
- API Testing (Postman, Newman, Hoppscotch, Bruno, REST Assured)
- Test Automation Frameworks: pytest, JUnit, TestNG, Jest, Vitest, Mocha, Cypress, Selenium, Playwright, Puppeteer, Appium, Espresso, XCTest
- Property-Based Testing (Hypothesis, QuickCheck, fast-check)
- Snapshot Testing, Visual Regression Testing (Percy, Chromatic, BackstopJS)
- Accessibility Testing (axe, Lighthouse, Pa11y, WAVE, WCAG 2.1/2.2 Compliance)
- Code Coverage (Istanbul/nyc, JaCoCo, Coverage.py, gcov), Mutation Testing (PIT, mutmut, Stryker)
- Static Analysis (SonarQube, SonarCloud, CodeClimate, Codacy, Coverity)
- Code Quality Gates, Quality Metrics (Cyclomatic Complexity, Cognitive Complexity, Code Churn)
- Shift-Left Testing, Testing Pyramid (Unit > Integration > E2E), Testing Trophy
- Test Data Management, Test Fixtures, Factories (Factory Boy, Faker), Mocking (Mockito, unittest.mock, Sinon, WireMock)
- Test Environments, Environment Parity, Testcontainers

### CI/CD & Deployment
- Continuous Integration (CI), Continuous Delivery (CD), Continuous Deployment
- CI/CD Platforms: Jenkins, GitHub Actions, GitLab CI/CD, CircleCI, Travis CI, Azure Pipelines, Buildkite, TeamCity, Drone, Concourse, Harness
- Artifact Management (Nexus, JFrog Artifactory, ECR, GCR, GAR, ACR, Docker Hub, GitHub Packages)
- Deployment Strategies: Blue-Green, Canary, Rolling, Recreate, Shadow/Dark, Traffic Splitting
- A/B Testing, Progressive Delivery, Feature-Gated Rollouts
- GitOps (ArgoCD, Flux, Weave GitOps), Pull-Based Deployment
- Release Management, Semantic Versioning (SemVer), CalVer, Changelog Generation (Conventional Changelog)
- Immutable Infrastructure, Phoenix Deployments, Cattle vs. Pets
- Deployment Automation, Zero-Downtime Deployment, Database Migration Strategies (Expand-Contract)
- Preview Environments, Ephemeral Environments, Pull Request Environments
- Spinnaker, Harness, Octopus Deploy
- DORA Metrics Tracking (Deployment Frequency, Lead Time for Changes, Change Failure Rate, Mean Time to Recovery)
- Rollback Strategies, Feature Flag Kill Switches

### Cloud & Infrastructure
- AWS, GCP, Azure, Multi-Cloud, Hybrid Cloud, Private Cloud (OpenStack, VMware)
- Serverless: AWS Lambda, Google Cloud Functions, Azure Functions, Cloud Run, Fargate, Knative
- Compute: EC2, GCE, Azure VMs, Spot/Preemptible Instances, Auto Scaling Groups, Managed Instance Groups
- Container Services: EKS, GKE, AKS, ECS, Cloud Run, App Runner, Azure Container Apps
- Storage: S3, GCS, Azure Blob, EBS, EFS, FSx, Persistent Volumes
- Networking: VPC, Subnets, Security Groups, NACLs, Route Tables, Peering, Transit Gateway, Private Link/PrivateLink
- Load Balancing: ALB, NLB, GLB, Cloud Load Balancing, Azure Load Balancer
- DNS: Route 53, Cloud DNS, Azure DNS, Cloudflare DNS
- CDN: CloudFront, Cloud CDN, Azure CDN, Cloudflare, Fastly, Akamai
- API Gateway: Amazon API Gateway, Apigee, Kong, Azure API Management, Tyk
- Database Services: RDS, Aurora, Cloud SQL, AlloyDB, DynamoDB, Firestore, CosmosDB, Cloud Spanner, ElastiCache, MemoryDB
- Identity & Access Management: IAM, OAuth 2.0, OIDC, SAML, SSO, MFA/2FA, Service Accounts, Workload Identity
- Managed Kubernetes: EKS, GKE, AKS (with Autopilot, Fargate profiles)
- Edge Computing: CloudFront Functions, Lambda@Edge, Cloudflare Workers, Deno Deploy
- Cloud Cost Management: FinOps, Reserved Instances, Savings Plans, Spot Instances, Right-Sizing, Cost Explorer, Infracost
- IaC State Management: Terraform State, Remote Backends, State Locking, Drift Detection

### Databases & Data Storage
- Relational (RDBMS): PostgreSQL, MySQL, MariaDB, SQL Server, Oracle, CockroachDB, YugabyteDB, TiDB, Vitess, PlanetScale
- NoSQL Document: MongoDB, Couchbase, Amazon DocumentDB, Firestore
- NoSQL Key-Value: Redis, DynamoDB, etcd, Riak, Aerospike
- NoSQL Wide-Column: Cassandra, HBase, ScyllaDB, Bigtable
- In-Memory: Redis, Memcached, Hazelcast, Apache Ignite
- Graph: Neo4j, Amazon Neptune, ArangoDB, JanusGraph, TigerGraph, Dgraph
- Time-Series: InfluxDB, TimescaleDB, Prometheus (TSDB), QuestDB, Apache Druid
- Search & Analytics: Elasticsearch, OpenSearch, Solr, Apache Lucene, Meilisearch, Typesense, Algolia
- Data Warehousing: BigQuery, Snowflake, Redshift, Databricks SQL, Synapse Analytics, ClickHouse, Apache Druid, StarRocks, DuckDB
- Object Storage: S3, GCS, Azure Blob, MinIO
- Database Design: Normalization (1NF–BCNF), Denormalization, Star Schema, Snowflake Schema
- Indexing: B-Tree, Hash, GiST, GIN, Bitmap, Full-Text, Partial/Filtered Indexes, Covering Indexes
- Query Optimization: EXPLAIN/ANALYZE, Query Plans, Index Selection, Join Strategies, Materialized Views
- ACID Properties, CAP Theorem, BASE (Basically Available, Soft state, Eventually consistent)
- Consistency Models: Strong, Eventual, Causal, Read-Your-Writes, Linearizability
- Database Migration: Flyway, Alembic, Liquibase, Atlas, Prisma Migrate, Rails Migrations
- Connection Pooling (PgBouncer, HikariCP, ProxySQL), Read Replicas, Multi-Primary Replication
- Partitioning (Range, Hash, List, Composite), Table Partitioning, Sharding
- Change Data Capture (CDC): Debezium, Maxwell, AWS DMS, GoldenGate
- Database Backup, Point-in-Time Recovery (PITR), Disaster Recovery (DR)
- NewSQL: CockroachDB, YugabyteDB, TiDB, Spanner

### Networking & Protocols
- TCP/IP, UDP, HTTP/1.1, HTTP/2, HTTP/3 (QUIC)
- TLS/SSL, mTLS (Mutual TLS), Certificate Management (cert-manager, Let's Encrypt, ACM)
- DNS (Resolution, CNAME, A/AAAA, SRV Records, Service Discovery)
- Service Discovery (Consul, etcd, ZooKeeper, CoreDNS, Eureka)
- Load Balancing Algorithms: Round Robin, Weighted, Least Connections, IP Hash, Consistent Hashing
- Reverse Proxy: Nginx, HAProxy, Envoy, Traefik, Caddy
- API Protocols: REST, GraphQL, gRPC (Protocol Buffers), WebSocket, SSE, MQTT, AMQP
- Network Security: Firewalls, WAF (Web Application Firewall), DDoS Protection, VPN, Bastion Hosts, Jump Boxes
- Content Delivery: CDN Configuration, Cache-Control Headers, ETag, Origin Shield
- IPv4/IPv6, CIDR Notation, NAT, Port Forwarding

### Observability & Monitoring
- The Four Golden Signals: Latency, Traffic, Errors, Saturation
- RED Method (Rate, Errors, Duration), USE Method (Utilization, Saturation, Errors)
- Logging: Structured Logging, Log Aggregation, Log Levels
- Logging Platforms: ELK Stack (Elasticsearch, Logstash, Kibana), Splunk, Fluentd/Fluent Bit, Loki, CloudWatch Logs, Datadog Logs
- Metrics: Counters, Gauges, Histograms, Summaries
- Metrics Platforms: Prometheus, Grafana, Datadog, New Relic, Dynatrace, SignalFx, CloudWatch Metrics
- Distributed Tracing: OpenTelemetry, Jaeger, Zipkin, AWS X-Ray, Google Cloud Trace, Honeycomb
- OpenTelemetry (OTel): Traces, Metrics, Logs, Baggage, Collector, SDK, Auto-Instrumentation
- Alerting: PagerDuty, OpsGenie, VictorOps, Alertmanager, Incident.io
- SLIs (Service Level Indicators), SLOs (Service Level Objectives), SLAs (Service Level Agreements), Error Budgets
- APM (Application Performance Monitoring): New Relic, Dynatrace, Datadog APM, Elastic APM
- Real User Monitoring (RUM), Synthetic Monitoring, Uptime Monitoring
- Health Checks, Liveness Probes, Readiness Probes, Startup Probes
- Dashboards, Runbook Automation, Incident Timelines
- Post-Incident Reviews (PIR), Blameless Postmortems, Root Cause Analysis (RCA), Five Whys
- Continuous Profiling (Pyroscope, Parca, Datadog Continuous Profiler)
- Cost Monitoring, Resource Utilization Tracking

### Security Best Practices
- OWASP Top 10, OWASP ASVS (Application Security Verification Standard)
- Secure SDLC (S-SDLC), Security Champions Program
- Threat Modeling (STRIDE, DREAD, PASTA, Attack Trees)
- Authentication: OAuth 2.0, OpenID Connect (OIDC), SAML 2.0, JWT, PASETO, WebAuthn/FIDO2, Passkeys
- Authorization: RBAC (Role-Based), ABAC (Attribute-Based), ReBAC (Relationship-Based), Policy Engines (OPA, Cedar, Casbin)
- Encryption: TLS 1.3, AES-256, RSA, ECDSA, at-rest encryption, in-transit encryption, envelope encryption, key rotation, KMS (AWS KMS, Cloud KMS, Azure Key Vault)
- Hashing: bcrypt, scrypt, Argon2 (password hashing), SHA-256, HMAC
- Vulnerability Management: Vulnerability Scanning, CVE Tracking, Patch Management
- Dependency Scanning: Snyk, Dependabot, Trivy, Grype, OSV-Scanner, Socket
- Container Security: Trivy, Falco, Sysdig, Aqua, Twistlock, Distroless Images, Non-Root Containers
- Zero Trust Architecture, Zero Trust Network Access (ZTNA)
- Compliance Frameworks: SOC 2 (Type I/II), HIPAA, GDPR, PCI-DSS, FedRAMP, ISO 27001/27017/27018, CCPA, NIST 800-53
- Security Incident Response Plan (SIRP), SIEM (Splunk, Sentinel, Chronicle)
- Least Privilege Principle, Principle of Minimal Authority
- Supply Chain Security: SBOM (Software Bill of Materials), Sigstore, Cosign, SLSA Framework, in-toto
- Secrets Detection: git-secrets, TruffleHog, Gitleaks, detect-secrets
- API Security: Rate Limiting, Input Validation, CORS, CSP (Content Security Policy), CSRF Protection
- Infrastructure Security: Network Segmentation, Microsegmentation, mTLS, Certificate Pinning
- Penetration Testing, Bug Bounty Programs, Responsible Disclosure

### Documentation & Communication
- Technical Documentation, System Documentation, Operational Documentation
- API Documentation: OpenAPI/Swagger, AsyncAPI, Redoc, Stoplight, GraphQL Introspection
- Runbooks, Playbooks, Standard Operating Procedures (SOPs), Troubleshooting Guides
- Architecture Decision Records (ADRs), RFCs (Request for Comments), Design Docs
- Knowledge Base (Confluence, Notion, Wiki, Slite, GitBook)
- Diagramming (Mermaid, PlantUML, Lucidchart, Draw.io, Excalidraw, C4 Model)
- Code Documentation (Javadoc, Sphinx, JSDoc, Godoc, Rustdoc)
- README Standards, CONTRIBUTING.md, Code of Conduct
- Technical Writing, Documentation-as-Code (Docs-as-Code), Docs Site Generators (MkDocs, Docusaurus, VitePress)
- Changelog Management (Keep a Changelog, Conventional Changelog)

### Performance Engineering
- Performance Profiling: CPU Profiling, Memory Profiling, I/O Profiling, Network Profiling
- Profiling Tools: pprof, py-spy, cProfile, perf, Instruments (Xcode), Chrome DevTools, Flame Graphs
- Benchmarking: Micro-Benchmarks, Macro-Benchmarks, Continuous Benchmarking
- Memory Management: Garbage Collection Tuning, Memory Leaks, Heap Analysis, Object Pooling
- Concurrency: Threads, Goroutines, Async/Await, Coroutines, Actors, CSP (Communicating Sequential Processes)
- Connection Pooling, Thread Pooling, Worker Pools
- Database Performance: Query Optimization, N+1 Problem, Eager/Lazy Loading, Batch Operations
- Caching Layers: Application Cache, Distributed Cache, HTTP Cache, Browser Cache
- CDN Optimization, Image Optimization, Lazy Loading, Code Splitting, Tree Shaking
- Resource Budgets (Performance Budgets, Bundle Size Budgets)
- Rate Limiting, Throttling, Backpressure, Circuit Breakers
- Horizontal Scaling, Auto-Scaling Policies, Predictive Scaling

### Frontend & UI Engineering
- Responsive Design, Mobile-First, Adaptive Design
- Component-Based Architecture, Atomic Design, Design Systems, Storybook
- State Management: Redux, Zustand, MobX, Recoil, Jotai, Pinia, NgRx, Signals
- Rendering Strategies: CSR (Client-Side Rendering), SSR (Server-Side Rendering), SSG (Static Site Generation), ISR (Incremental Static Regeneration), Streaming SSR, RSC (React Server Components)
- Web Performance: Core Web Vitals (LCP, FID/INP, CLS), Lighthouse, PageSpeed Insights
- PWA (Progressive Web App), Service Workers, Web Workers, WebAssembly (WASM)
- Accessibility (a11y): WCAG 2.1/2.2, ARIA, Screen Reader Testing, Keyboard Navigation
- Internationalization (i18n), Localization (l10n), RTL Support
- CSS: Tailwind CSS, CSS Modules, Styled Components, CSS-in-JS, Sass/SCSS, CSS Grid, Flexbox
- Testing: Jest, Vitest, React Testing Library, Cypress, Playwright, Storybook Tests
- Build & Bundle: Webpack, Vite, esbuild, Turbopack, SWC, Babel
- Micro-Frontends, Module Federation, Single-SPA
- WebSocket, SSE (Server-Sent Events), Long Polling, Real-Time UI

### Data Engineering (Software Context)
- Batch Processing: Apache Spark, Apache Hadoop (MapReduce, HDFS), Hive
- Stream Processing: Apache Kafka Streams, Apache Flink, Apache Beam, Spark Structured Streaming, AWS Kinesis, Google Dataflow
- Data Pipeline Orchestration: Apache Airflow, Prefect, Dagster, Luigi, Mage, Kestra
- ELT/ETL: dbt (Data Build Tool), Fivetran, Airbyte, Stitch, Talend, Informatica
- Data Lakehouse: Delta Lake, Apache Iceberg, Apache Hudi, Databricks Lakehouse
- Data Quality: Great Expectations, Deequ, Soda, dbt tests, Monte Carlo
- Data Modeling: Dimensional Modeling (Kimball), Data Vault, One Big Table (OBT), Activity Schema
- Data Governance: Data Catalog (DataHub, Amundsen, Apache Atlas, Alation), Data Lineage, Metadata Management
- Streaming Architectures: Lambda Architecture, Kappa Architecture
- File Formats: Parquet, ORC, Avro, Arrow, Delta, Iceberg
- Data Serialization: Protobuf, Avro, Thrift, FlatBuffers
- Schema Registry (Confluent Schema Registry), Schema Evolution (Forward/Backward/Full Compatibility)

---

## Machine Learning Lifecycle (MLOps)

### Problem Framing & Scoping
- Business Problem Definition, Success Criteria, Proxy Metrics
- ML Feasibility Assessment, ML vs. Rule-Based Analysis
- Baseline Establishment (Heuristic, Rule-Based, Simple Statistical)
- Ethical AI Assessment, Fairness Audit, Impact Assessment
- ROI Analysis, Cost-Benefit Analysis, Total Cost of Ownership (TCO)
- Responsible AI, AI Governance, AI Strategy
- Data Availability Assessment, Data Readiness
- ML System Design (Design Documents, Architecture Reviews)
- Stakeholder Alignment, Cross-Functional Collaboration (Data Science, ML Engineering, Product, Legal)

### Data Engineering & Management
- Data Collection, Data Acquisition, Data Ingestion (Batch, Streaming, Real-Time)
- ETL / ELT Pipelines (Airflow, Prefect, Dagster, dbt, Fivetran, Airbyte)
- Data Warehousing (BigQuery, Snowflake, Redshift, Databricks Lakehouse)
- Data Lakes / Lakehouses (S3, GCS, ADLS, Delta Lake, Apache Iceberg, Apache Hudi)
- Data Catalog / Data Discovery (DataHub, Amundsen, OpenMetadata, Alation, Apache Atlas)
- Data Quality: Great Expectations, Deequ, Soda, Pandera, data validation, schema validation
- Data Profiling, Data Auditing, Data Quality Dimensions (Completeness, Accuracy, Consistency, Timeliness, Validity, Uniqueness)
- Data Lineage, Data Provenance, Impact Analysis
- Data Versioning (DVC, LakeFS, Delta Lake Time Travel, Pachyderm)
- Data Governance, Data Stewardship, Data Ownership, Data Contracts
- Schema Registry, Schema Evolution, Schema Validation
- Feature Engineering: Feature Extraction, Feature Selection, Feature Transformation, Encoding (One-Hot, Label, Target, Ordinal, Embedding)
- Feature Store (Feast, Tecton, Hopsworks, SageMaker Feature Store, Vertex AI Feature Store)
- Data Labeling, Annotation: Label Studio, Scale AI, Labelbox, Snorkel, Prodigy, Amazon SageMaker Ground Truth, V7
- Active Learning, Weak Supervision (Snorkel), Programmatic Labeling
- Synthetic Data Generation (SDV, CTGAN, Gretel, Mostly AI)
- Data Privacy: PII Detection, PII Masking/Redaction, Anonymization, Pseudonymization, Differential Privacy, k-Anonymity
- Data Augmentation (text, image, audio, tabular)
- Imbalanced Data Handling: SMOTE, ADASYN, Undersampling, Oversampling, Class Weights, Focal Loss
- Big Data Processing: Apache Spark (PySpark, Spark SQL, Spark MLlib), Dask, Ray, Modin, Vaex, Polars

### Exploratory Data Analysis (EDA)
- Statistical Analysis: Descriptive Statistics (Mean, Median, Mode, Std Dev, Variance, Skewness, Kurtosis)
- Inferential Statistics: Confidence Intervals, p-values, Effect Size
- Data Visualization: Matplotlib, Seaborn, Plotly, Altair, Bokeh, D3.js, Tableau, Looker, Power BI, Metabase, Superset
- Correlation Analysis (Pearson, Spearman, Kendall, Point-Biserial), Multicollinearity (VIF)
- Distribution Analysis, Normality Tests (Shapiro-Wilk, Kolmogorov-Smirnov, Anderson-Darling)
- Outlier Detection (IQR, Z-Score, Isolation Forest, DBSCAN, LOF)
- Missing Value Analysis, Imputation Strategies (Mean, Median, KNN, MICE, Iterative)
- Dimensionality Reduction (PCA, t-SNE, UMAP, SVD, Factor Analysis, Autoencoders)
- Hypothesis Testing: t-test, Chi-Square, ANOVA, Mann-Whitney U, Kruskal-Wallis, Wilcoxon
- A/B Testing Framework, Experiment Design, Statistical Power, Sample Size Calculation, Multi-Armed Bandit
- Bayesian Statistics, Prior/Posterior, Bayesian A/B Testing
- Causal Inference, Causal Discovery, DoWhy, CausalML

### Model Development — Classical ML
- Supervised Learning:
  - Classification: Logistic Regression, Decision Trees, Random Forest, Gradient Boosting (XGBoost, LightGBM, CatBoost), SVM, KNN, Naive Bayes, Linear Discriminant Analysis
  - Regression: Linear Regression, Ridge, Lasso, Elastic Net, Polynomial Regression, SVR, Gradient Boosting Regressors, Quantile Regression
- Unsupervised Learning:
  - Clustering: K-Means, DBSCAN, HDBSCAN, Agglomerative/Hierarchical, Gaussian Mixture Models (GMM), Mean Shift, Spectral Clustering
  - Anomaly Detection: Isolation Forest, Local Outlier Factor (LOF), One-Class SVM, Autoencoders, Statistical Methods
  - Dimensionality Reduction: PCA, t-SNE, UMAP, SVD, NMF, Factor Analysis, ICA
  - Association Rules: Apriori, FP-Growth
- Semi-Supervised Learning, Self-Supervised Learning, Contrastive Learning (SimCLR, MoCo, BYOL)
- Reinforcement Learning: Q-Learning, Deep Q-Network (DQN), Policy Gradient, PPO, A3C, SAC, RLHF, DPO (Direct Preference Optimization)
- Multi-Task Learning, Meta-Learning (Few-Shot Learning, MAML)
- Ensemble Methods: Bagging, Boosting, Stacking, Blending, Voting (Hard/Soft)
- Hyperparameter Tuning: Grid Search, Random Search, Bayesian Optimization (Optuna, Hyperopt, Ray Tune, Keras Tuner, BOHB)
- AutoML: Auto-sklearn, AutoGluon, H2O, TPOT, Google AutoML, Azure AutoML, Amazon SageMaker Autopilot, FLAML
- Cross-Validation: k-Fold, Stratified k-Fold, Leave-One-Out, Time-Series Split, Group k-Fold, Nested Cross-Validation
- Regularization: L1 (Lasso), L2 (Ridge), Elastic Net, Dropout, Early Stopping, Data Augmentation, Weight Decay, Batch Normalization, Label Smoothing
- Loss Functions: Cross-Entropy, MSE, MAE, Huber Loss, Focal Loss, Contrastive Loss, Triplet Loss, Hinge Loss, KL Divergence
- Imbalanced Learning: Class Weights, Cost-Sensitive Learning, Threshold Tuning, Oversampling/Undersampling
- Feature Importance, Feature Selection (Filter, Wrapper, Embedded Methods), Recursive Feature Elimination (RFE)
- Model Selection: AIC, BIC, Cross-Validation Score, Learning Curves, Validation Curves

### Model Development — Deep Learning
- Neural Network Fundamentals: Perceptron, MLP, Activation Functions (ReLU, GELU, SiLU/Swish, Sigmoid, Tanh, Softmax), Backpropagation, Gradient Descent (SGD, Adam, AdamW, LAMB, LARS)
- Convolutional Neural Networks (CNNs): ResNet, EfficientNet, VGG, Inception, MobileNet, ConvNeXt, Vision Transformer (ViT)
- Recurrent Neural Networks (RNNs): LSTM, GRU, Bidirectional RNN, Seq2Seq
- Transformers: Self-Attention, Multi-Head Attention, Positional Encoding, Encoder-Decoder, Decoder-Only, Encoder-Only
- Generative Models: GANs (StyleGAN, CycleGAN, Pix2Pix, WGAN), VAEs, Diffusion Models (DDPM, Stable Diffusion, DALL-E), Normalizing Flows
- Graph Neural Networks (GNNs): GCN, GAT, GraphSAGE, Message Passing, Node/Edge/Graph Classification
- State Space Models: Mamba, S4, Structured State Spaces
- Mixture of Experts (MoE), Sparse Transformers
- Neural Architecture Search (NAS), EfficientNet, Once-for-All
- Transfer Learning: Pre-Training, Fine-Tuning, Domain Adaptation, Zero-Shot Transfer
- Multi-Modal Models: CLIP, Flamingo, GPT-4V, Gemini, LLaVA, Multimodal Fusion
- Self-Supervised Pre-Training: BERT (Masked Language Modeling), GPT (Causal Language Modeling), MAE (Masked Autoencoder), DINO, SimCLR
- Training Techniques: Learning Rate Scheduling (Warmup, Cosine Annealing, OneCycleLR), Gradient Clipping, Gradient Accumulation, Mixed Precision Training (AMP), Gradient Checkpointing
- Distributed Training: Data Parallelism (DDP), Model Parallelism, Pipeline Parallelism, Tensor Parallelism, FSDP (Fully Sharded Data Parallel), DeepSpeed (ZeRO-1/2/3), Megatron-LM, Horovod, Ray Train, PyTorch Lightning
- Attention Mechanisms: Scaled Dot-Product, Multi-Head, Multi-Query, Grouped-Query (GQA), Flash Attention, Ring Attention, Sliding Window Attention
- Normalization: Batch Norm, Layer Norm, RMSNorm, Group Norm, Instance Norm

### NLP & Language Models
- Large Language Models (LLMs): GPT-4, Claude (Opus, Sonnet, Haiku), Llama 3, Gemini, Mistral, Mixtral, Phi, Command R, Qwen, DeepSeek, Falcon, BLOOM, OLMo
- Foundation Models, Pre-Trained Models, Base Models vs. Instruction-Tuned vs. Chat Models
- Prompt Engineering: Zero-Shot, Few-Shot, Chain-of-Thought (CoT), Tree-of-Thought, ReAct, Self-Consistency, Prompt Chaining, System Prompts, Prompt Templates
- In-Context Learning (ICL), Instruction Following, Instruction Tuning
- Retrieval-Augmented Generation (RAG): Naive RAG, Advanced RAG, Modular RAG, Agentic RAG, GraphRAG
- RAG Components: Document Loading, Chunking Strategies (Fixed, Semantic, Recursive), Embedding, Retrieval, Reranking (Cross-Encoder, Cohere Rerank), Generation
- Fine-Tuning: Full Fine-Tuning, Parameter-Efficient Fine-Tuning (PEFT), LoRA, QLoRA, DoRA, Adapters, Prefix Tuning, Prompt Tuning, IA3
- Alignment: RLHF, DPO (Direct Preference Optimization), Constitutional AI, RLAIF, PPO, KTO, ORPO
- Tokenization: BPE (Byte-Pair Encoding), SentencePiece, WordPiece, Unigram, tiktoken
- Embeddings: Word2Vec, GloVe, FastText, BERT Embeddings, Sentence Transformers, OpenAI Embeddings, Cohere Embeddings, Voyage AI
- Vector Databases / Vector Search: Pinecone, Weaviate, Milvus, ChromaDB, Qdrant, pgvector, FAISS, Elasticsearch (kNN), Vespa, LanceDB
- Similarity Search: Cosine Similarity, Euclidean Distance, Inner Product, HNSW, IVF, PQ
- Named Entity Recognition (NER), Part-of-Speech Tagging, Dependency Parsing, Coreference Resolution
- Sentiment Analysis, Text Classification, Topic Modeling (LDA, BERTopic), Text Summarization
- Semantic Search, Information Retrieval, BM25, Hybrid Search (Sparse + Dense)
- Document AI, Intelligent Document Processing (IDP), Layout Analysis, Table Extraction
- Text-to-SQL, Code Generation, Code Completion
- Question Answering: Extractive QA, Generative QA, Open-Domain QA, Closed-Domain QA
- Agentic AI, AI Agents, Tool Use / Function Calling, Multi-Agent Systems, Agent Frameworks (LangGraph, CrewAI, AutoGen, Semantic Kernel)
- LLM Orchestration: LangChain, LlamaIndex, Haystack, Semantic Kernel, DSPy
- Guardrails: Guardrails AI, NeMo Guardrails, Content Filtering, Safety Alignment, Output Parsing
- Structured Output: JSON Mode, Tool Use, Pydantic (Instructor), LMQL, Outlines, Guidance
- Hallucination Detection, Grounding, Citation, Retrieval Verification
- LLM Evaluation: HELM, lm-eval-harness, MMLU, HumanEval, GSM8K, TruthfulQA, MT-Bench, Chatbot Arena
- LLM Caching (GPTCache, Semantic Caching), Token Optimization, Context Window Management
- Long Context: Context Window Extension, Rope Scaling, ALiBi, Retrieval over Long Documents

### Computer Vision
- Image Classification, Object Detection (Single-Stage: YOLO, SSD; Two-Stage: Faster R-CNN, Mask R-CNN)
- Semantic Segmentation (U-Net, DeepLab, FCN), Instance Segmentation (Mask R-CNN, YOLACT), Panoptic Segmentation
- Pose Estimation (OpenPose, MediaPipe), Keypoint Detection, Human Pose Estimation
- OCR (Optical Character Recognition): Tesseract, PaddleOCR, EasyOCR, Document Understanding (LayoutLM, Donut)
- Video Analysis: Action Recognition, Video Object Tracking (SORT, DeepSORT, ByteTrack), Temporal Modeling, Optical Flow
- Image Generation: Stable Diffusion, DALL-E, Midjourney, ControlNet, IP-Adapter, DreamBooth
- 3D Vision: NeRF, Gaussian Splatting, Point Clouds, Depth Estimation, Stereo Vision
- Image Embeddings: CLIP, DINOv2, ImageBind
- Data Augmentation: Albumentations, imgaug, RandAugment, CutMix, MixUp, Mosaic, AutoAugment
- Frameworks & Libraries: OpenCV, torchvision, Detectron2, MMDetection, Ultralytics (YOLOv8/v11), SAM (Segment Anything), Grounding DINO, Florence
- Visual Question Answering (VQA), Image Captioning, Visual Grounding
- Medical Imaging, Satellite/Geospatial Imagery, Industrial Inspection, Autonomous Driving Vision

### Speech & Audio ML
- Automatic Speech Recognition (ASR): Whisper, Wav2Vec 2.0, Conformer, DeepSpeech, Google Speech-to-Text, Azure Speech
- Text-to-Speech (TTS): Coqui TTS, Bark, Tortoise TTS, VITS, XTTS, ElevenLabs
- Speaker Diarization, Speaker Verification, Voice Cloning
- Audio Classification, Sound Event Detection
- Music Generation (MusicGen, AudioCraft)
- Speech Enhancement, Noise Reduction
- Audio Feature Extraction: MFCCs, Spectrograms, Mel-Spectrograms, Wav2Vec Embeddings

### Time Series & Forecasting
- Classical Methods: ARIMA, SARIMA, ETS (Exponential Smoothing), Prophet, VAR
- ML Methods: XGBoost for Time Series, LightGBM, Random Forest, Gradient Boosting
- Deep Learning: LSTM, GRU, Temporal Convolutional Networks (TCN), Temporal Fusion Transformers (TFT), N-BEATS, N-HiTS, PatchTST, TimeGPT, Chronos, Lag-Llama
- Libraries: statsmodels, Prophet, NeuralProphet, Darts, GluonTS, sktime, tslearn, tsfresh
- Feature Engineering: Lag Features, Rolling Statistics, Fourier Features, Calendar Features, Holiday Effects
- Anomaly Detection in Time Series, Changepoint Detection
- Multi-Step Forecasting, Multi-Variate Forecasting, Hierarchical Forecasting, Probabilistic Forecasting (Quantile Regression, Conformal Prediction)

### Recommender Systems
- Collaborative Filtering: User-Based, Item-Based, Matrix Factorization (SVD, ALS, NMF)
- Content-Based Filtering, Hybrid Recommenders
- Deep Learning Recommenders: Neural Collaborative Filtering (NCF), Wide & Deep, DeepFM, Two-Tower Models, DLRM
- Sequential Recommendations: Session-Based (GRU4Rec), Transformer-Based (SASRec, BERT4Rec)
- Knowledge Graph Embeddings, Graph-Based Recommendations
- Multi-Armed Bandit, Contextual Bandit (Exploration-Exploitation)
- Evaluation: Hit Rate, NDCG, MRR, MAP, Diversity, Coverage, Novelty, Serendipity
- Cold-Start Problem, Popularity Bias, Filter Bubbles
- Feature Store Integration, Real-Time Recommendation Serving
- Libraries/Platforms: Surprise, LightFM, RecBole, Merlin (NVIDIA), Amazon Personalize, Google Recommendations AI

### Tabular ML
- Gradient Boosting: XGBoost, LightGBM, CatBoost (still dominant for tabular data)
- Deep Learning for Tabular: TabNet, FT-Transformer, TabTransformer, SAINT, NODE
- AutoML for Tabular: AutoGluon, FLAML, Auto-sklearn, H2O, TPOT
- Feature Engineering: Encoding (One-Hot, Target, Ordinal, Binary, Hash), Binning, Polynomial Features, Interaction Features
- Handling: Missing Values, Categorical Features, High Cardinality, Multi-Collinearity
- Interpretability: SHAP, LIME, Partial Dependence Plots, ICE Plots, Feature Importance

### ML Frameworks & Libraries
- Deep Learning: PyTorch, TensorFlow, JAX, Keras, MXNet, Flax, Equinox
- Training Utilities: PyTorch Lightning, Hugging Face Accelerate, Fabric, DeepSpeed, FairScale
- Classical ML: scikit-learn, XGBoost, LightGBM, CatBoost, statsmodels
- NLP/LLM: Hugging Face (Transformers, Datasets, Tokenizers, Accelerate, PEFT, TRL, Evaluate), LangChain, LlamaIndex, Haystack, DSPy, spaCy, NLTK, Gensim, Flair, Stanza
- Computer Vision: OpenCV, torchvision, Detectron2, MMDetection, Ultralytics, Albumentations, Kornia
- Data Processing: NumPy, Pandas, Polars, Dask, PySpark, Modin, Vaex, Apache Arrow, CuDF (RAPIDS)
- Scientific Computing: SciPy, SymPy, Numba, CuPy (GPU-accelerated NumPy)
- Visualization: Matplotlib, Seaborn, Plotly, Altair, Bokeh, Wandb Plots
- Experiment Management: MLflow, Weights & Biases, Neptune, Comet ML, ClearML, Sacred, Aim
- Notebooks: Jupyter, JupyterLab, JupyterHub, Google Colab, Kaggle Notebooks, SageMaker Studio, Vertex AI Workbench, Databricks Notebooks, Hex, Deepnote, Marimo
- Model Serialization: pickle, joblib, ONNX, TorchScript, SavedModel, safetensors

### Experiment Tracking & Model Registry
- Experiment Tracking: MLflow Tracking, Weights & Biases (wandb), Neptune, Comet ML, ClearML, Aim, TensorBoard, SageMaker Experiments, Vertex AI Experiments
- Model Registry: MLflow Model Registry, Weights & Biases Model Registry, SageMaker Model Registry, Vertex AI Model Registry, BentoML
- Model Versioning, Model Lineage, Model Metadata
- Hyperparameter Logging, Metric Logging, Artifact Logging
- Reproducibility: Random Seeds, Environment Pinning (Conda Lock, Poetry Lock, pip-tools), Deterministic Training, Docker Images, DVC Pipelines
- Experiment Comparison, Parameter Sweep Visualization, Parallel Coordinates
- Model Staging (Staging → Production), Model Approval Workflows, Model Promotion

### Model Evaluation & Validation
- Classification: Accuracy, Precision, Recall, F1-Score (Micro/Macro/Weighted), AUC-ROC, AUC-PR, Log Loss, Matthews Correlation Coefficient (MCC), Cohen's Kappa, Balanced Accuracy, Specificity, Sensitivity
- Regression: MSE, RMSE, MAE, MAPE, SMAPE, R², Adjusted R², Explained Variance, Median Absolute Error, Quantile Loss
- Ranking: NDCG, MRR, MAP, Precision@K, Recall@K, Hit Rate
- NLP/LLM Metrics: BLEU, ROUGE (1/2/L), METEOR, BERTScore, Perplexity, MAUVE, TER, CIDEr, Faithfulness, Answer Relevancy
- LLM-as-Judge, G-Eval, Pairwise Comparison, Arena-Style Evaluation
- Confusion Matrix, Classification Report, ROC Curve, Precision-Recall Curve
- Calibration: Calibration Curves (Reliability Diagrams), Expected Calibration Error (ECE), Platt Scaling, Isotonic Regression, Temperature Scaling
- Bias & Fairness: Demographic Parity, Equalized Odds, Predictive Parity, Disparate Impact, Counterfactual Fairness, AIF360, Fairlearn, What-If Tool
- Explainability / Interpretability (XAI): SHAP (TreeSHAP, DeepSHAP, KernelSHAP), LIME, Integrated Gradients, Attention Visualization, Grad-CAM, Saliency Maps, Counterfactual Explanations, Partial Dependence Plots, Individual Conditional Expectation (ICE), Permutation Feature Importance, Anchors
- Model Cards (Google), Datasheets for Datasets, FactSheets
- Statistical Significance: Paired t-test, McNemar's Test, Bootstrap Confidence Intervals, Permutation Tests
- Error Analysis, Failure Mode Analysis, Slice-Based Evaluation (Sliceline), Data-Centric Evaluation
- Adversarial Testing, Robustness Evaluation, Out-of-Distribution (OOD) Detection, Uncertainty Quantification (Epistemic, Aleatoric)
- Backtesting (Time Series), Walk-Forward Validation
- Online Evaluation: Interleaving, A/B Testing, Multi-Armed Bandit

### Model Optimization & Serving
- Model Compression: Quantization (Post-Training: INT8, INT4, GPTQ, AWQ, GGUF/GGML; Quantization-Aware Training: QAT), Pruning (Structured, Unstructured, Magnitude-Based), Knowledge Distillation (Teacher-Student), Low-Rank Factorization
- Model Formats: ONNX, TensorRT, TorchScript, SavedModel, Core ML, TFLite, OpenVINO, safetensors
- Inference Optimization: Operator Fusion, Graph Optimization, Memory Optimization, KV Cache, PagedAttention, Speculative Decoding, Continuous Batching
- Model Serving Frameworks: TorchServe, TFServing, Triton Inference Server, vLLM, TGI (Text Generation Inference), Ollama, LMDeploy, BentoML, Ray Serve, Seldon Core, KServe
- Batch Inference vs. Real-Time Inference vs. Near-Real-Time, Streaming Inference
- Edge Deployment: TensorFlow Lite, ONNX Runtime Mobile, Core ML, TensorRT (Jetson), MediaPipe, OpenVINO (Intel), Qualcomm AI Engine
- GPU/TPU/NPU Optimization: CUDA, cuDNN, Mixed Precision Training (FP16, BF16, FP8, INT8), Tensor Cores, Multi-GPU Inference, Model Parallelism
- Hardware: NVIDIA GPUs (A100, H100, H200, B200), Google TPUs (v4, v5e), AWS Trainium/Inferentia, AMD MI300X, Apple Neural Engine, Intel Gaudi
- Model Caching, Request Batching (Dynamic Batching, Static Batching), Token Streaming
- A/B Testing for Models, Multi-Armed Bandit, Interleaving
- Shadow Deployment, Champion-Challenger, Canary Deployment for Models
- Auto-Scaling Inference, Serverless Inference (SageMaker Serverless, Vertex AI Endpoints), Scale-to-Zero
- Cost Optimization: Instance Selection, Spot/Preemptible Instances, Batching, Caching, Quantization

### MLOps & Production
- ML Platforms: SageMaker, Vertex AI, Azure ML, Databricks, MLflow, Kubeflow, ClearML, Domino Data Lab, Weights & Biases, Comet ML, Neptune, Determined AI, Union (Flyte)
- ML Pipelines: Kubeflow Pipelines, Vertex AI Pipelines, SageMaker Pipelines, Metaflow, ZenML, Kedro, Flyte, Prefect, Dagster, Argo Workflows
- CI/CD for ML: CML (Continuous Machine Learning), GitHub Actions for ML, GitLab CI for ML, MLflow CI/CD, DVC Pipelines
- Model Monitoring:
  - Data Drift (Distribution Shift): PSI (Population Stability Index), KS Test, Wasserstein Distance, Jensen-Shannon Divergence, Chi-Square
  - Concept Drift (Target Drift), Feature Drift, Prediction Drift
  - Performance Degradation Monitoring, Accuracy Decay
  - Monitoring Tools: Evidently AI, WhyLabs, Arize AI, Fiddler, NannyML, Seldon Alibi Detect, Amazon SageMaker Model Monitor, Vertex AI Model Monitoring
- Feature Monitoring, Prediction Logging, Ground Truth Collection
- Automated Retraining: Trigger-Based (Drift, Schedule, Performance), Continuous Training
- Model Governance: Model Approval Workflows, Model Audit Trail, Model Inventory, Model Risk Management (MRM)
- Model Lifecycle Management: Development → Staging → Production → Archived/Deprecated
- ML Infrastructure: GPU Clusters, Spot/Preemptible Instances, Auto-Scaling, Kubernetes for ML, Ray Clusters, Slurm (HPC)
- Cost Optimization: Instance Selection, Spot/Preemptible, Batch vs. Real-Time, Right-Sizing, Reserved Capacity
- Containerized ML: Docker, Kubernetes, KServe, BentoML, Seldon Core
- Data Pipeline Orchestration (Airflow, Dagster, Prefect, Flyte)
- Reproducibility: DVC, MLflow, Docker, Conda/Poetry Lock Files, Deterministic Builds, Git Tags
- LLMOps: LLM-Specific Monitoring, Prompt Management, Prompt Versioning, A/B Testing Prompts, Cost Tracking (Token Usage), Latency Monitoring, LangSmith, Langfuse, Helicone, Portkey, Braintrust

### Responsible AI & Governance
- Fairness, Accountability, Transparency (FAT/FATE)
- AI Ethics, Bias Mitigation (Pre-Processing, In-Processing, Post-Processing)
- Fairness Tools: AIF360, Fairlearn, What-If Tool, Aequitas
- Model Explainability (XAI): Global vs. Local Explanations, Model-Agnostic vs. Model-Specific
- Privacy-Preserving ML: Federated Learning (Cross-Device, Cross-Silo), Differential Privacy (DP-SGD, Opacus), Secure Multi-Party Computation (SMPC), Homomorphic Encryption, Confidential Computing (TEEs)
- AI Regulation & Compliance: EU AI Act (Risk Tiers: Unacceptable, High, Limited, Minimal), NIST AI Risk Management Framework (AI RMF), Executive Order on AI Safety, IEEE 7000 Series, Canada AIDA
- Human-in-the-Loop (HITL), Human-on-the-Loop (HOTL), Human-over-the-Loop
- Red Teaming, Safety Evaluation, Alignment Testing, Jailbreak Testing
- Hallucination Detection, Grounding, Citation, Source Attribution, Retrieval Verification
- AI Safety: Alignment, Robustness, Monitoring for Harmful Outputs, Content Safety
- Model Documentation: Model Cards, Datasheets for Datasets, System Cards, AI Factsheets
- Data Ethics: Informed Consent, Right to Explanation, Right to Erasure, Data Minimization
- Intellectual Property: Training Data Rights, Model Output Ownership, Copyright Considerations
- Environmental Impact: Carbon Footprint of Training, Compute Efficiency, Green AI, ML Carbon Impact

---

## Cross-Cutting Best Practices

### Industry Standards & Certifications
- ISO 27001 (Information Security), ISO 27017 (Cloud Security), ISO 27018 (PII in Cloud)
- ISO 25010 (Software Quality Model), ISO 9001 (Quality Management)
- ISO/IEC 42001 (AI Management System), ISO/IEC 23894 (AI Risk Management)
- CMMI (Capability Maturity Model Integration)
- ITIL (IT Service Management), ITSM
- IEEE/ISO Software Engineering Standards (IEEE 730, 829, 1012)
- NIST Cybersecurity Framework (CSF), NIST SP 800-53, NIST AI RMF
- TOGAF (Enterprise Architecture), Zachman Framework
- Well-Architected Framework (AWS 6 Pillars, GCP, Azure)
- Cloud Certifications: AWS (SAA, SAP, MLS), GCP (PCA, PMLE), Azure (AZ-305, AI-102)
- Security Certifications: CISSP, CEH, CompTIA Security+, OSCP
- Agile Certifications: CSM, PSM, PMI-ACP, SAFe Agilist
- Data/ML Certifications: AWS Machine Learning Specialty, GCP Professional ML Engineer, Azure AI Engineer, TensorFlow Developer Certificate, Databricks Certifications

### Engineering Culture & Process
- Blameless Culture, Psychological Safety, Growth Mindset
- Technical Debt Quantification & Prioritization, Refactoring Sprints
- Architecture Reviews, Design Reviews, Code Reviews, Security Reviews
- On-Call Rotations, Incident Response, Incident Command System (ICS), Runbooks
- Capacity Planning, Cost Engineering (FinOps), Cloud Cost Optimization
- Developer Experience (DevEx), Developer Productivity Engineering (DPE), Platform Engineering, Internal Developer Platform (IDP)
- Documentation-as-Code, Everything-as-Code, Policy-as-Code
- Observability-Driven Development, Observability Engineering
- Chaos Engineering, Game Days, Disaster Recovery (DR) Drills, Tabletop Exercises
- Toil Reduction, Automation-First Mindset, Self-Service Platforms
- Inner Source, Open Source Contribution, Open Source Program Office (OSPO)
- Engineering Ladders, IC (Individual Contributor) vs. Management Track, Staff+ Engineering
- Technical Leadership, Architecture Ownership, System Ownership
- Sprint Velocity, Burndown Charts, Cumulative Flow Diagrams
- Change Management, Release Trains, Deployment Cadence
- Knowledge Sharing: Tech Talks, Brown Bags, Guilds/Chapters, Communities of Practice

### Collaboration & Project Management Tools
- Project Management: Jira, Linear, Asana, Shortcut, ClickUp, Monday.com, Azure Boards, Trello
- Documentation: Confluence, Notion, Coda, Slite, GitBook, Docusaurus
- Communication: Slack, Microsoft Teams, Discord, Zoom, Google Meet
- Source Control: GitHub, GitLab, Bitbucket, Azure DevOps
- Design: Figma, Sketch, Adobe XD, Zeplin (Design Handoff)
- Whiteboarding: Miro, FigJam, Lucidspark, Excalidraw
- Analytics & BI: Looker, Tableau, Power BI, Metabase, Superset, Mode, Hex, Amplitude, Mixpanel
- Incident Management: PagerDuty, OpsGenie, Incident.io, FireHydrant, Rootly
- Status Pages: Statuspage (Atlassian), Betteruptime, Instatus
- Security: 1Password, Okta, Auth0, Clerk

### Soft Skills & Leadership (Engineering Context)
- Technical Communication, Cross-Functional Collaboration
- Stakeholder Management, Executive Communication
- Mentorship, Technical Mentoring, Onboarding
- Influence Without Authority, Consensus Building
- Project Estimation, Risk Communication
- Trade-Off Analysis, Decision Documentation
- System Thinking, First Principles Thinking
- Incident Leadership, War Room Facilitation
- Technical Interviewing, Hiring Bar Raising
- Vendor Evaluation, Build vs. Buy Analysis
