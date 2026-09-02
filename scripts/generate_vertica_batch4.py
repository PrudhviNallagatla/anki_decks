import csv

batch4_cards = [
    {
        "Question": "What does `COPY ... ON ANY NODE` do in Vertica?",
        "Answer": "<b>ANSWER:</b> Distributes file parsing and ingestion across multiple cluster nodes in parallel.<br><br><b>Syntax:</b><br><code>COPY sales FROM 's3://bucket/*.csv' ON ANY NODE DIRECT;</code><br><br>Instead of a single initiator node reading all files and suffering an I/O bottleneck, Vertica divides the files among all available nodes to load in parallel at line rate.",
        "Topic": "Data Ingestion",
        "Tags": "vertica ingestion copy on_any_node parallel"
    },
    {
        "Question": "How do you capture rejected rows and parsing errors during a `COPY` operation?",
        "Answer": "<b>ANSWER:</b> Use the `REJECTED DATA` and `EXCEPTIONS` clauses.<br><br><b>Syntax:</b><br><code>COPY users FROM 'users.csv' <br>REJECTED DATA 'rejected.log' EXCEPTIONS 'exceptions.log' DIRECT;</code><br><br>Valid rows are committed; malformed or type-mismatched rows are written to the rejected data file with the exact failure reason without aborting the entire load.",
        "Topic": "Data Ingestion",
        "Tags": "vertica ingestion copy rejected_data exceptions"
    },
    {
        "Question": "What is `ANALYZE_STATISTICS()` in Vertica and when must a DBA run it?",
        "Answer": "<b>ANSWER:</b> Collects data distribution statistics (histograms, distinct counts) for the query optimizer.<br><br><b>The SQL:</b><br><code>SELECT ANALYZE_STATISTICS('sales_fact');</code><br><br>Must be run after large initial data loads or major data modifications. Without statistics, the optimizer relies on generic defaults and may choose disastrous join algorithms.",
        "Topic": "Query Tuning",
        "Tags": "vertica tuning analyze_statistics optimizer"
    },
    {
        "Question": "How does Table Partitioning in Vertica differ from traditional database partitioning?",
        "Answer": "<b>ANSWER:</b> Vertica uses Partition Expressions rather than rigid manual tablespaces.<br><br><b>Example:</b><br><code>PARTITION BY (sales_date::date);</code><br>Or monthly: <code>PARTITION BY (date_part('year', sales_date)*100 + date_part('month', sales_date));</code><br>Partitions are used for easy data lifecycle management (`DROP_PARTITIONS`) and partition pruning, NOT for parallelism (Segmentation handles parallelism).",
        "Topic": "Storage Management",
        "Tags": "vertica partitioning table storage"
    },
    {
        "Question": "What is Hierarchical Partitioning (Partition Groups) in Vertica?",
        "Answer": "<b>ANSWER:</b> Grouping older daily/monthly partitions into broader yearly partition groups.<br><br>Prevents partition explosion and ROS sprawl. Active current data stays in daily partitions for fast pruning; historical data is automatically consolidated into yearly groups by the Tuple Mover.",
        "Topic": "Storage Management",
        "Tags": "vertica partitioning partition_groups maintenance"
    },
    {
        "Question": "How do you instantly drop 5 years of historical data from a partitioned table?",
        "Answer": "<b>ANSWER:</b> Use the `DROP_PARTITIONS()` function.<br><br><b>The SQL:</b><br><code>SELECT DROP_PARTITIONS('sales', 201801, 202212);</code><br><br>Instantly deletes metadata pointers and associated ROS containers on disk in milliseconds without scanning the table or creating deletion vectors.",
        "Topic": "Storage Management",
        "Tags": "vertica partitioning drop_partitions purge"
    },
    {
        "Question": "What are the lock modes in Vertica and where do you view active locks?",
        "Answer": "<b>ANSWER:</b> `V_MONITOR.LOCKS`<br><br>• <b>Modes:</b> `T` (Tuple Mover lock), `S` (Shared read lock), `X` (Exclusive write lock), `O` (Owner DDL lock).<br>• <b>Inspection SQL:</b><br><code>SELECT node_name, object_name, lock_mode, lock_scope <br>FROM v_monitor.locks;</code>",
        "Topic": "System Catalogs",
        "Tags": "vertica catalogs locks concurrency"
    },
    {
        "Question": "What is the Vertica Data Collector and how do you query historical component metrics?",
        "Answer": "<b>ANSWER:</b> An internal subsystem that continuously records operational metrics into ring-buffer tables.<br><br>Persisted in tables named `DC_*` (e.g. `V_MONITOR.DC_RESOURCE_POOL_STATUS`, `DC_REQUESTS_COMPLETED`). Allows DBAs to investigate query performance and resource usage hours or days after an incident occurred.",
        "Topic": "Cluster Administration",
        "Tags": "vertica administration data_collector dc_tables"
    },
    {
        "Question": "What is the difference between `V_MONITOR.SESSIONS` and `V_CATALOG.USERS`?",
        "Answer": "<b>ANSWER:</b> Real-time connected sessions vs. static user definitions.<br><br>• <code>V_MONITOR.SESSIONS</code>: Active TCP sessions, client IP addresses, session start times, currently running statement IDs.<br>• <code>V_CATALOG.USERS</code>: Permanent user catalog accounts, default resource pools, password expiry settings.",
        "Topic": "System Catalogs",
        "Tags": "vertica catalogs sessions users"
    },
    {
        "Question": "What is the `FLATTEN()` table function in Vertica?",
        "Answer": "<b>ANSWER:</b> Explodes JSON or nested arrays into individual relational rows.<br><br><b>The SQL:</b><br><code>SELECT user_id, FLATTEN(tags) OVER (PARTITION BY user_id) <br>FROM user_profiles;</code><br>Converts an array `['sql', 'vertica', 'aws']` into 3 discrete rows for standard relational aggregation.",
        "Topic": "Analytical SQL",
        "Tags": "vertica sql flatten json arrays"
    },
    {
        "Question": "What are Virtual (Generated) Columns in Vertica?",
        "Answer": "<b>ANSWER:</b> Computed columns whose values are derived from expressions on other columns.<br><br><b>Syntax:</b><br><code>ALTER TABLE orders ADD COLUMN total_with_tax AS (price * 1.08);</code><br>Can be included in projection sort orders, enabling fast filter evaluation on derived calculations without physically storing duplicate data.",
        "Topic": "Columnar Architecture",
        "Tags": "vertica ddl virtual_columns expressions"
    },
    {
        "Question": "What is the difference between `REFRESH` modes: `REBUILD` vs `SCRATCH` in Vertica?",
        "Answer": "<b>ANSWER:</b> How projection data is refreshed from existing projections.<br><br>• <b>REBUILD:</b> Builds the new projection by scanning and sorting an existing, compatible projection. Highly efficient.<br>• <b>SCRATCH:</b> Builds the projection from scratch by scanning the underlying table data when no compatible sorted projection exists.",
        "Topic": "Projection Design",
        "Tags": "vertica projections refresh rebuild scratch"
    },
    {
        "Question": "What does `SELECT CLOSE_ALL_SESSIONS();` do?",
        "Answer": "<b>ANSWER:</b> Immediately terminates all user sessions across the entire cluster.<br><br>Must be run by `dbadmin` when preparing the database for emergency maintenance, an immediate shutdown, or exclusive single-user operations.",
        "Topic": "Cluster Administration",
        "Tags": "vertica administration sessions close_all_sessions"
    },
    {
        "Question": "What is the `dbLog` file in Vertica?",
        "Answer": "<b>ANSWER:</b> A human-readable record of major database lifecycle and administrative events.<br><br>Logs cluster startup, shutdown, node additions, node failures, and major catalog transactions. Located in the database catalog directory alongside `vertica.log`.",
        "Topic": "Cluster Administration",
        "Tags": "vertica administration dblog logging"
    },
    {
        "Question": "What is Spread Tracing and when should a Vertica DBA enable it?",
        "Answer": "<b>ANSWER:</b> Debug logging for cluster networking and consensus communication.<br><br>Enabled via <code>admintools -t set_spread_logging</code> when investigating phantom node dropouts, split-brain false alarms, or inter-node UDP packet loss across network switches.",
        "Topic": "Cluster Administration",
        "Tags": "vertica spread networking troubleshooting"
    },
    {
        "Question": "How does Vertica handle transactions across multiple nodes during bulk loading?",
        "Answer": "<b>ANSWER:</b> Two-Phase Commit (2PC) coordinated by the Initiator node.<br><br>The client connects to any arbitrary node (the Initiator). The Initiator distributes data slices, coordinates prepare messages, and issues the commit epoch broadcast via the Spread daemon.",
        "Topic": "Columnar Architecture",
        "Tags": "vertica architecture 2pc commit transactions"
    },
    {
        "Question": "What is the `AUDIT_LICENSE_SIZE()` grace period behavior in Vertica?",
        "Answer": "<b>ANSWER:</b> 30-day compliance grace period before restricting write operations.<br><br>If total uncompressed data exceeds licensed capacity, Vertica sends administrative alerts and grants a 30-day grace window. If unresolved after 30 days, Vertica disables new write operations (`INSERT`, `COPY`, `UPDATE`) while queries continue reading.",
        "Topic": "Cluster Administration",
        "Tags": "vertica licensing compliance grace_period"
    },
    {
        "Question": "What is the `CLEAR_DATA_COLLECTOR()` function in Vertica?",
        "Answer": "<b>ANSWER:</b> Flushes in-memory operational metrics from Data Collector ring buffers to disk.<br><br>Used by DBAs before running diagnostic scripts or clearing memory after resolving high-intensity system outages.",
        "Topic": "Cluster Administration",
        "Tags": "vertica administration data_collector maintenance"
    }
]

# Append Batch 4 to decks/vertica_deck.csv
with open('decks/vertica_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in batch4_cards:
        writer.writerow(card)

print(f"Batch 4 complete: appended {len(batch4_cards)} cards.")
