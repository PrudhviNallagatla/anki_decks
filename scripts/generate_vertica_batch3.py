import csv

batch3_cards = [
    # --- MODULE 7: QUERY EXECUTION & EXPLAIN PLAN FORENSICS ---
    {
        "Question": "What command generates a query execution plan in Vertica?",
        "Answer": "<b>ANSWER:</b> The `EXPLAIN` statement.<br><br><b>Syntax:</b><br><code>EXPLAIN SELECT customer_id, SUM(amount) FROM sales GROUP BY 1;</code><br><br>Displays the optimizer's execution tree: projection choices, join algorithms, network distribution (broadcast vs resegment), and grouping paths.",
        "Topic": "Query Tuning",
        "Tags": "vertica tuning explain query_plan"
    },
    {
        "Question": "What is the difference between a Merge Join and a Hash Join in Vertica?",
        "Answer": "<b>ANSWER:</b> Streaming pre-sorted join vs. in-memory hash table lookup.<br><br>• <b>Merge Join (Fastest):</b> Requires both projections to be pre-sorted on the join keys. Streams data with zero memory footprint.<br>• <b>Hash Join:</b> Requires Vertica to build an in-memory hash table of the inner relation. Consumes significant RAM and can spill to disk if memory is insufficient.",
        "Topic": "Query Tuning",
        "Tags": "vertica tuning joins merge_join hash_join"
    },
    {
        "Question": "What is a Local Co-located Join in a Vertica execution plan?",
        "Answer": "<b>ANSWER:</b> A join where matching rows reside on the exact same physical node with ZERO network communication.<br><br>Occurs when both tables are segmented on the same join key (or when one is an unsegmented replicated dimension). This is the holy grail of Vertica join performance.",
        "Topic": "Query Tuning",
        "Tags": "vertica tuning joins co_located network"
    },
    {
        "Question": "What is a Broadcast Join in Vertica?",
        "Answer": "<b>ANSWER:</b> Sending an entire copy of a smaller table across the network to every node.<br><br>Vertica chooses this when joining a segmented fact table with an unsegmented or differently segmented small dimension table. Low overhead if the broadcast table is small.",
        "Topic": "Query Tuning",
        "Tags": "vertica tuning joins broadcast network"
    },
    {
        "Question": "What is a Resegment Join in Vertica, and why is it expensive?",
        "Answer": "<b>ANSWER:</b> Dynamically hashing and transmitting rows from BOTH tables across all cluster nodes during query execution.<br><br>Occurs when neither table is segmented by the join key. Incurs massive network I/O and memory overhead. Fix by designing projections segmented on the common join key.",
        "Topic": "Query Tuning",
        "Tags": "vertica tuning joins resegment network"
    },
    {
        "Question": "What is the difference between `GROUPBY PIPELINED` and `GROUPBY HASH` in an execution plan?",
        "Answer": "<b>ANSWER:</b> Zero-memory streaming aggregation vs. in-memory hash aggregation.<br><br>• <b>GROUPBY PIPELINED:</b> Occurs when projection sort order matches the `GROUP BY` columns. Vertica aggregates rows on the fly in CPU registers without buffering.<br>• <b>GROUPBY HASH:</b> Must construct an in-memory hash table to group unsorted values, consuming pool memory.",
        "Topic": "Query Tuning",
        "Tags": "vertica tuning aggregations groupby pipelined"
    },
    {
        "Question": "What is the Database Designer (`designer.sh`) in Vertica?",
        "Answer": "<b>ANSWER:</b> An automated physical schema design tool built into Vertica.<br><br>Analyzes a sample query workload and table statistics, and automatically generates SQL scripts to create optimal projections, sort orders, and column compression encodings.",
        "Topic": "Query Tuning",
        "Tags": "vertica database_designer projections optimization"
    },
    {
        "Question": "What is the difference between Comprehensive Design and Incremental Design in Database Designer?",
        "Answer": "<b>ANSWER:</b> Whole-database redesign vs. tuning for specific new queries.<br><br>• <b>Comprehensive:</b> Generates a brand-new, complete set of superprojections and buddy projections for all tables.<br>• <b>Incremental:</b> Adds targeted secondary projections to optimize specific slow queries without modifying existing projections.",
        "Topic": "Query Tuning",
        "Tags": "vertica database_designer comprehensive incremental"
    },
    {
        "Question": "How do you profile an executing query to view exact runtime metrics per operator?",
        "Answer": "<b>ANSWER:</b> Use the `PROFILE` keyword before the statement.<br><br><b>The SQL:</b><br><code>PROFILE SELECT count(*) FROM sales;</code><br><br>Populates detailed execution metrics into `V_MONITOR.EXECUTION_ENGINE_PROFILES`, showing actual rows processed, memory used, and disk spill bytes per node.",
        "Topic": "Query Tuning",
        "Tags": "vertica tuning profile metrics"
    },
    {
        "Question": "How do you detect if a query spilled memory to disk during execution?",
        "Answer": "<b>ANSWER:</b> Query `V_MONITOR.EXECUTION_ENGINE_PROFILES` for spill counters.<br><br><b>The SQL:</b><br><code>SELECT operator_name, counter_name, counter_value <br>FROM v_monitor.execution_engine_profiles <br>WHERE counter_name LIKE '%spill%';</code><br><br>Spilling indicates the Resource Pool's query memory budget was too small for the sort or hash operation.",
        "Topic": "Query Tuning",
        "Tags": "vertica tuning memory spill profiling"
    },
    {
        "Question": "What is Directed Query in Vertica?",
        "Answer": "<b>ANSWER:</b> A saved query execution plan pinned to a specific SQL statement.<br><br>Used by DBAs to freeze an optimal execution plan, preventing the optimizer from choosing a worse plan after statistics updates or software upgrades (Vertica's equivalent to query hints/plan pinning).",
        "Topic": "Query Tuning",
        "Tags": "vertica tuning directed_queries plan_pinning"
    },
    {
        "Question": "What does the `STORAGE ACCESS` path operator indicate in an EXPLAIN plan?",
        "Answer": "<b>ANSWER:</b> Reading column blocks directly from physical ROS storage containers.<br><br>Shows projection name, columns read, and any filter predicates evaluated directly on compressed storage blocks before loading into memory.",
        "Topic": "Query Tuning",
        "Tags": "vertica tuning explain storage_access"
    },

    # --- MODULE 8: ADMINISTRATION, BACKUP & OPERATIONS ---
    {
        "Question": "What is `admintools` and what OS user must run it?",
        "Answer": "<b>ANSWER:</b> The primary administration command-line interface for Vertica clusters.<br><br>Must be executed by the <b>`dbadmin`</b> operating system user. Handles database creation, start/stop, adding/dropping nodes, license installation, and viewing cluster state.",
        "Topic": "Cluster Administration",
        "Tags": "vertica admintools dbadmin administration"
    },
    {
        "Question": "How do you start and stop a Vertica database using `admintools`?",
        "Answer": "<b>ANSWER:</b> Use `-t start_db` and `-t stop_db`.<br><br><b>Start:</b><br><code>admintools -t start_db -d vdb -p secret</code><br><b>Stop:</b><br><code>admintools -t stop_db -d vdb -p secret --force</code>",
        "Topic": "Cluster Administration",
        "Tags": "vertica admintools start_db stop_db"
    },
    {
        "Question": "How do you restart a downed node in an active cluster using `admintools`?",
        "Answer": "<b>ANSWER:</b> Use `-t restart_node`.<br><br><b>The Command:</b><br><code>admintools -t restart_node -d vdb -s 192.168.1.51 -p secret</code><br><br>Starts the Vertica process on the downed node, which then joins cluster quorum and initiates historical recovery.",
        "Topic": "Cluster Administration",
        "Tags": "vertica admintools restart_node recovery"
    },
    {
        "Question": "List the 5 primary Node Lifecycle States in Vertica.",
        "Answer": "<b>ANSWER:</b> `INITIALIZING`, `UP`, `DOWN`, `RECOVERING`, and `STANDBY`.<br><br>• <b>UP:</b> Fully active, participating in query execution.<br>• <b>DOWN:</b> Process stopped or unreachable.<br>• <b>RECOVERING:</b> Pulling missing transactions from buddy nodes.<br>• <b>INITIALIZING:</b> Starting up and contacting Spread daemon.<br>• <b>STANDBY:</b> Eon Mode spare compute node.",
        "Topic": "Cluster Administration",
        "Tags": "vertica administration node_states lifecycle"
    },
    {
        "Question": "What is `vbr` (Vertica Backup and Restore)?",
        "Answer": "<b>ANSWER:</b> The dedicated snapshot backup utility for Vertica.<br><br>Uses configuration files (`backup.ini`) to take consistent, multi-node snapshots to remote backup hosts, local disk, or cloud object storage (S3). Supports full, incremental, and hard-link backups.",
        "Topic": "Backup & Recovery",
        "Tags": "vertica vbr backup restore disaster"
    },
    {
        "Question": "How does `vbr` perform Object-Level Backup and Restore?",
        "Answer": "<b>ANSWER:</b> Backing up or restoring specific tables rather than the entire cluster.<br><br>Configured in the `.ini` file via <code>objects = schema1.table1, schema2.table2</code>. Restored using <code>vbr --task restore --config-file backup.ini</code>.",
        "Topic": "Backup & Recovery",
        "Tags": "vertica vbr object_level backup"
    },
    {
        "Question": "What is Cross-Cluster Replication in Vertica using `vbr`?",
        "Answer": "<b>ANSWER:</b> Replicating snapshot data from a primary cluster directly to a standby DR cluster.<br><br><b>Syntax:</b><br><code>vbr --task replicate --config-file replicate.ini</code><br><br>Synchronizes communal data or local partitions between two independent Vertica clusters for disaster recovery.",
        "Topic": "Backup & Recovery",
        "Tags": "vertica vbr replication disaster_recovery"
    },
    {
        "Question": "How do you audit licensed database data size in Vertica?",
        "Answer": "<b>ANSWER:</b> Run `AUDIT_LICENSE_SIZE()`.<br><br><b>The SQL:</b><br><code>SELECT AUDIT_LICENSE_SIZE();</code><br><code>SELECT * FROM v_catalog.license_audits ORDER BY audit_start_timestamp DESC LIMIT 1;</code><br><br>Calculates raw uncompressed data size across all tables to verify compliance with licensed terabyte limits.",
        "Topic": "Cluster Administration",
        "Tags": "vertica licensing audit license_size"
    },
    {
        "Question": "How do you terminate a runaway query in Vertica SQL?",
        "Answer": "<b>ANSWER:</b> Use `INTERRUPT_STATEMENT()` or `CLOSE_SESSION()`.<br><br><b>Interrupt specific query:</b><br><code>SELECT INTERRUPT_STATEMENT('session_id', statement_id);</code><br><b>Kill entire session:</b><br><code>SELECT CLOSE_SESSION('session_id');</code><br>Find session IDs in `V_MONITOR.SESSIONS`.",
        "Topic": "Cluster Administration",
        "Tags": "vertica administration sessions terminate"
    },
    {
        "Question": "Where is the primary server log file (`vertica.log`) located?",
        "Answer": "<b>ANSWER:</b> Inside the node's catalog directory.<br><br><b>Path:</b><br><code><catalog_path>/<database_name>/<node_name>_catalog/vertica.log</code><br><br>Contains startup messages, Tuple Mover passes, checkpoint events, recovery logs, and engine errors.",
        "Topic": "Cluster Administration",
        "Tags": "vertica administration logs vertica_log"
    },
    {
        "Question": "What is the Spread Daemon in Vertica?",
        "Answer": "<b>ANSWER:</b> The low-latency internal messaging and cluster membership service.<br><br>Runs on all nodes communicating over UDP/TCP port 4803. Manages cluster heartbeat, node up/down state transitions, and distributed agreement for transaction commits.",
        "Topic": "Cluster Administration",
        "Tags": "vertica spread clustering heartbeat networking"
    },
    {
        "Question": "What is Partition Swapping (`SWAP_PARTITIONS_BETWEEN_TABLES`)?",
        "Answer": "<b>ANSWER:</b> Instant, zero-copy metadata swap of entire table partitions.<br><br><b>The SQL:</b><br><code>SELECT SWAP_PARTITIONS_BETWEEN_TABLES('staging_sales', '2026-08', '2026-08', 'prod_sales');</code><br><br>Swaps physical ROS container pointers between staging and production tables in milliseconds with zero downtime.",
        "Topic": "Data Ingestion",
        "Tags": "vertica partitions swap_partitions staging"
    },

    # --- MODULE 9: ADVANCED ANALYTICAL SQL & VSQL ---
    {
        "Question": "What is the `TIMESERIES` clause in Vertica SQL?",
        "Answer": "<b>ANSWER:</b> Built-in SQL syntax for time series gap filling and regularizing data points.<br><br><b>Example:</b><br><code>SELECT slice_time, symbol, TS_FIRST_VALUE(price, 'CONST') <br>FROM trades <br>TIMESERIES slice_time AS '5 seconds' OVER (PARTITION BY symbol ORDER BY trade_time);</code><br>Generates uniform 5-second interval time slices even if trades occurred irregularly.",
        "Topic": "Analytical SQL",
        "Tags": "vertica sql timeseries gap_filling"
    },
    {
        "Question": "What is `CONDITIONAL_CHANGE_EVENT()` in Vertica?",
        "Answer": "<b>ANSWER:</b> An analytic window function that increments an integer counter whenever a column value changes.<br><br><b>The SQL:</b><br><code>SELECT user_id, action, <br>       CONDITIONAL_CHANGE_EVENT(action) OVER (PARTITION BY user_id ORDER BY event_time) AS session_id <br>FROM user_logs;</code><br>Crucial for sessionizing clickstream data without writing complex procedural loops.",
        "Topic": "Analytical SQL",
        "Tags": "vertica sql analytics conditional_change_event"
    },
    {
        "Question": "What is `CONDITIONAL_TRUE_EVENT()` in Vertica?",
        "Answer": "<b>ANSWER:</b> Increments a counter every time a boolean condition evaluates to TRUE.<br><br><b>Example:</b><br><code>CONDITIONAL_TRUE_EVENT(temp > 100) OVER (PARTITION BY sensor_id ORDER BY time)</code><br>Counts the cumulative number of heat spikes observed over time for each sensor.",
        "Topic": "Analytical SQL",
        "Tags": "vertica sql analytics conditional_true_event"
    },
    {
        "Question": "What is the `MATCH (...)` clause in Vertica SQL?",
        "Answer": "<b>ANSWER:</b> Complex Event Processing (CEP) pattern matching across rows using regular-expression-like syntax.<br><br>Enables querying patterns across ordered sequences of events (e.g. \"Find users who performed Action A, followed within 3 rows by Action B, followed by Action C\").",
        "Topic": "Analytical SQL",
        "Tags": "vertica sql cep pattern_matching match"
    },
    {
        "Question": "What is a Flex Table in Vertica?",
        "Answer": "<b>ANSWER:</b> A hybrid schema-less table for ingesting semi-structured data (JSON, CSV, Avro) without predefined DDL.<br><br><b>The SQL:</b><br><code>CREATE FLEX TABLE raw_events();</code><br><code>COPY raw_events FROM 'data.json' PARSER fjsonparser();</code><br>Data is loaded immediately and queried using standard SQL without defining columns first.",
        "Topic": "Flex Tables",
        "Tags": "vertica flex_tables json nosql"
    },
    {
        "Question": "What is the `__raw__` column in a Vertica Flex Table?",
        "Answer": "<b>ANSWER:</b> An internal VMap binary column that stores all unmapped key-value pairs.<br><br>You query attributes directly using map syntax:<br><code>SELECT __raw__['user']['id']::int FROM raw_events;</code><br>Eliminates data conversion delays during high-velocity data ingestion.",
        "Topic": "Flex Tables",
        "Tags": "vertica flex_tables __raw__ vmap"
    },
    {
        "Question": "Name 5 essential `vsql` meta-commands used by Vertica DBAs.",
        "Answer": "<b>ANSWER:</b> Core slash commands in `vsql`:<br><br>• <code>\\d</code>: List tables, views, and system tables.<br>• <code>\\dj</code>: List projections and their anchor tables.<br>• <code>\\dp</code>: List object privileges and grants.<br>• <code>\\timing</code>: Toggle execution timing display on/off.<br>• <code>\\x</code>: Toggle expanded vertical display for wide rows.",
        "Topic": "User Tools",
        "Tags": "vertica vsql meta_commands dba"
    },
    {
        "Question": "Why should every production SQL script in `vsql` include `\\set ON_ERROR_STOP on`?",
        "Answer": "<b>ANSWER:</b> Halts script execution immediately if any SQL error occurs.<br><br>Without this setting, `vsql` logs the error and blindly continues executing subsequent statements, which can cause disastrous partial data migrations or accidental drops.",
        "Topic": "User Tools",
        "Tags": "vertica vsql on_error_stop scripts"
    },
    {
        "Question": "How do you export Vertica query results directly into Parquet files?",
        "Answer": "<b>ANSWER:</b> Use the `EXPORT TO PARQUET` statement.<br><br><b>The SQL:</b><br><code>EXPORT TO PARQUET(directory = 's3://mybucket/sales_parquet') <br>OVER (PARTITION BY year) AS <br>SELECT * FROM sales;</code><br><br>Directly streams columnar Parquet data to cloud storage or HDFS.",
        "Topic": "Analytical SQL",
        "Tags": "vertica sql export parquet s3"
    },
    {
        "Question": "What is `APPROXIMATE_COUNT_DISTINCT()` in Vertica?",
        "Answer": "<b>ANSWER:</b> HyperLogLog approximation of distinct values for massive datasets.<br><br>Returns a cardinality estimate with typical ~1–2% error rate in a fraction of the time and memory required by exact `COUNT(DISTINCT col)`, ideal for real-time dashboards.",
        "Topic": "Analytical SQL",
        "Tags": "vertica sql analytics hyperloglog approximate"
    }
]

# Append Batch 3 to decks/vertica_deck.csv
with open('decks/vertica_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in batch3_cards:
        writer.writerow(card)

print(f"Batch 3 complete: appended {len(batch3_cards)} cards.")
