import csv

new_cards = [
    # --- LAB SCENARIOS & SYSTEM BENCHMARKING (from Answer Key & Advanced Labs) ---
    {
        "Question": "What does the `pg_test_fsync` utility do, and why should a DBA run it?",
        "Answer": "<b>ANSWER:</b> Benchmarks the fastest and safest `wal_sync_method` for your specific hardware/OS.<br><br>It tests various system calls (e.g., `fdatasync`, `open_datasync`, `fsync`, `fsync_writethrough`). The Linux default is typically `fdatasync`. Running this helps choose the optimal setting in `postgresql.conf` to maximize write throughput.",
        "Topic": "Performance Tuning",
        "Tags": "edb_postgres tuning pg_test_fsync wal"
    },
    {
        "Question": "What is the `hstore` extension in Postgres, and when is it used?",
        "Answer": "<b>ANSWER:</b> A key-value pair data type within a single Postgres column.<br><br><b>The SQL:</b><br><code>CREATE EXTENSION IF NOT EXISTS hstore;</code><br><code>CREATE TABLE config (id serial, properties hstore);</code><br>Useful for semi-structured data where attributes change frequently without needing schema alterations. (Predecessor to JSONB).",
        "Topic": "Extensions",
        "Tags": "edb_postgres extensions hstore nosql"
    },
    {
        "Question": "How does `constraint_exclusion` affect query planning on partitioned tables?",
        "Answer": "<b>ANSWER:</b> Enables the planner to skip partitions based on CHECK constraints.<br><br>• <code>partition</code> (default): Enables partition pruning for partitioned tables.<br>• <code>off</code>: Disables constraint exclusion, forcing the planner to scan ALL child partitions even when WHERE clauses prove rows cannot exist there.<br>• <code>on</code>: Examines constraints on all tables (adds planner overhead).",
        "Topic": "SQL Tuning",
        "Tags": "edb_postgres tuning partitioning constraint_exclusion"
    },
    {
        "Question": "How do you detect which indexes in a database are never used?",
        "Answer": "<b>ANSWER:</b> Inspect the `idx_scan` column in `pg_stat_user_indexes`.<br><br><b>The SQL:</b><br><code>SELECT schemaname, relname, indexrelname, idx_scan <br>FROM pg_stat_user_indexes <br>WHERE idx_scan = 0;<br></code><br>Indexes with 0 scans consume disk space and slow down INSERT/UPDATE operations, and should be considered for removal.",
        "Topic": "Maintenance",
        "Tags": "edb_postgres maintenance indexes pg_stat_user_indexes"
    },
    {
        "Question": "How do you log every temporary disk file created by queries spilling to disk?",
        "Answer": "<b>ANSWER:</b> Set `log_temp_files` in `postgresql.conf`.<br><br><b>Setting:</b><br><code>log_temp_files = 0</code><br><br>`0` logs all temporary files (with size). A positive number (e.g. `10240`) logs files larger than that size in KB. Essential for identifying queries that exceed `work_mem` and spill sorting/hashing to slow disk.",
        "Topic": "Performance Tuning",
        "Tags": "edb_postgres tuning work_mem temp_files"
    },

    # --- CONNECTION POOLING (PGBOUNCER MODES) ---
    {
        "Question": "Explain the three Pool Modes in PgBouncer: Session, Transaction, and Statement.",
        "Answer": "<b>ANSWER:</b> Determines how long a client holds a backend Postgres connection.<br><br>1. <b>Session:</b> Connection held until client disconnects. Safest, but lowest concurrency.<br>2. <b>Transaction (Most Popular):</b> Connection held only for the duration of a single `BEGIN...COMMIT`. Returns to pool immediately after. (Cannot use prepared statements or LISTEN/NOTIFY).<br>3. <b>Statement:</b> Connection held for a single query. Multi-statement transactions not allowed.",
        "Topic": "High Availability",
        "Tags": "edb_postgres pgbouncer pooling architecture"
    },
    {
        "Question": "Why is an 'idle in transaction' session dangerous for a Postgres database?",
        "Answer": "<b>ANSWER:</b> It holds locks and halts table VACUUM progress.<br><br>An uncommitted transaction holds its snapshot and `xmin` transaction horizon. Even if idle, it prevents autovacuum from cleaning dead tuples across the entire database generated after that transaction began, causing catastrophic table and index bloat.",
        "Topic": "Troubleshooting",
        "Tags": "edb_postgres troubleshooting vacuum bloat idle_in_transaction"
    },
    {
        "Question": "How do you automatically terminate sessions left 'idle in transaction'?",
        "Answer": "<b>ANSWER:</b> Configure `idle_in_transaction_session_timeout`.<br><br><b>In postgresql.conf:</b><br><code>idle_in_transaction_session_timeout = '5min'</code><br><br>If an open transaction sits idle without committing or rolling back for 5 minutes, Postgres forcefully terminates the backend connection, releasing all locks and unblocking VACUUM.",
        "Topic": "Configuration",
        "Tags": "edb_postgres config troubleshooting timeout"
    },

    # --- ADVANCED SQL & EXTENSIONS ---
    {
        "Question": "What is the difference between `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()`?",
        "Answer": "<b>ANSWER:</b> How ties (identical values) are ranked.<br><br>Suppose three employees tie for 2nd place:<br>• <code>ROW_NUMBER()</code>: Arbitrarily assigns unique numbers (1, 2, 3, 4).<br>• <code>RANK()</code>: Assigns same rank with gaps after (1, 2, 2, 4).<br>• <code>DENSE_RANK()</code>: Assigns same rank without gaps after (1, 2, 2, 3).",
        "Topic": "Advanced SQL",
        "Tags": "edb_postgres sql window_functions ranking"
    },
    {
        "Question": "How do `COALESCE` and `NULLIF` handle NULL values in SQL?",
        "Answer": "<b>ANSWER:</b> Value substitution vs Null generation.<br><br>• <code>COALESCE(a, b, c)</code>: Returns the first non-null argument. If `a` is null, returns `b`.<br>• <code>NULLIF(a, b)</code>: Returns NULL if `a == b`, otherwise returns `a`. (Often used to prevent division by zero: `total / NULLIF(count, 0)`).",
        "Topic": "SQL Fundamentals",
        "Tags": "edb_postgres sql null coalesce nullif"
    },
    {
        "Question": "What is the `pg_trgm` extension and why is it used for text search?",
        "Answer": "<b>ANSWER:</b> Trigram matching for fast pattern matching and similarity.<br><br>Standard B-Tree indexes cannot index wildcards like `LIKE '%pattern%'`. `pg_trgm` breaks text into 3-letter trigrams and uses a <b>GIN index</b> to make leading-wildcard text searches blazing fast:<br><code>CREATE INDEX idx_trgm ON users USING gin (name gin_trgm_ops);</code>",
        "Topic": "Extensions",
        "Tags": "edb_postgres extensions pg_trgm gin search"
    },
    {
        "Question": "What is the `dblink` extension in Postgres?",
        "Answer": "<b>ANSWER:</b> Executes queries on remote Postgres databases from within a local session.<br><br><b>The SQL:</b><br><code>SELECT * FROM dblink('host=remotedb user=rep dbname=test', 'SELECT id, name FROM users') AS t(id int, name text);</code><br><br>(For modern workloads, `postgres_fdw` is preferred as it conforms to SQL standard Foreign Data Wrappers).",
        "Topic": "Extensions",
        "Tags": "edb_postgres extensions dblink fdw"
    },
    {
        "Question": "What is an Expression Index (Functional Index)?",
        "Answer": "<b>ANSWER:</b> An index built on the result of an expression or function rather than a raw column.<br><br><b>The SQL:</b><br><code>CREATE INDEX idx_lower_email ON users (LOWER(email));</code><br><br>If a user queries `WHERE LOWER(email) = 'test@example.com'`, Postgres will use the index. Without the expression index, it would be forced to run a full table scan.",
        "Topic": "Advanced Indexing",
        "Tags": "edb_postgres indexing expression lower"
    },
    {
        "Question": "How do UNIQUE indexes handle multiple NULL values in Postgres?",
        "Answer": "<b>ANSWER:</b> By default, multiple NULLs are permitted.<br><br>In SQL standard, `NULL != NULL`. Therefore, a standard UNIQUE constraint allows infinite NULL values.<br>In Postgres 15+, you can enforce `UNIQUE NULLS NOT DISTINCT` to treat NULLs as equal and disallow duplicate NULL entries.",
        "Topic": "Advanced Indexing",
        "Tags": "edb_postgres indexing unique nulls"
    },

    # --- ADVANCED CATALOGS & LOCK DIAGNOSTICS ---
    {
        "Question": "What catalog table stores the physical data types and schemas in Postgres?",
        "Answer": "<b>ANSWER:</b> `pg_type` and `pg_namespace`.<br><br>• <code>pg_namespace</code>: Stores all schemas and their owners.<br>• <code>pg_type</code>: Stores all data types (built-in types like `int4`, `varchar`, and user-defined enums, composites, domains).",
        "Topic": "Storage & Catalogs",
        "Tags": "edb_postgres catalogs pg_namespace pg_type"
    },
    {
        "Question": "What is the difference between an AccessExclusiveLock and a RowShareLock?",
        "Answer": "<b>ANSWER:</b> Full table lock vs non-blocking row read.<br><br>• <b>AccessExclusiveLock:</b> Acquired by `DROP TABLE`, `TRUNCATE`, `ALTER TABLE`. Blocks EVERYTHING (reads, writes, other locks).<br>• <b>RowShareLock:</b> Acquired by `SELECT ... FOR SHARE`. Allows concurrent reads and writes, only conflicting with exclusive table locks.",
        "Topic": "Architecture & Locking",
        "Tags": "edb_postgres architecture locking locks"
    },
    {
        "Question": "How do you check cache hit ratio across the entire database?",
        "Answer": "<b>ANSWER:</b> Query `pg_stat_database`.<br><br><b>The SQL:</b><br><code>SELECT datname, <br>  round(100.0 * blks_hit / (blks_hit + blks_read), 2) AS cache_hit_ratio <br>FROM pg_stat_database <br>WHERE blks_hit + blks_read > 0;</code><br><br>In healthy production OLTP systems, this ratio should ideally exceed 99%.",
        "Topic": "Database Monitoring",
        "Tags": "edb_postgres monitoring cache_hit_ratio"
    },
    {
        "Question": "What is `synchronous_commit` and what are its levels?",
        "Answer": "<b>ANSWER:</b> Controls how eagerly WAL must be flushed before reporting COMMIT success.<br><br>• <code>on</code> (default): Waits for local WAL to flush to disk.<br>• <code>off</code>: Asynchronous commit. Returns immediately; up to `3 * wal_writer_delay` of data can be lost in a crash, but write throughput spikes 3x.<br>• <code>remote_write</code> / <code>on</code> / <code>remote_apply</code>: Governs replication standby guarantees.",
        "Topic": "Architecture",
        "Tags": "edb_postgres architecture wal synchronous_commit"
    },
    {
        "Question": "What is the purpose of the `pg_stat_statements_reset()` function?",
        "Answer": "<b>ANSWER:</b> Resets all accumulated query statistics in `pg_stat_statements`.<br><br><b>Usage:</b><br><code>SELECT pg_stat_statements_reset();</code><br><br>DBAs run this before benchmarking, after a deployment, or when investigating a newly emerging performance degradation to clear old historical data.",
        "Topic": "Database Monitoring",
        "Tags": "edb_postgres monitoring pg_stat_statements reset"
    },
    {
        "Question": "What is the difference between `statement_timeout` and `lock_timeout`?",
        "Answer": "<b>ANSWER:</b> Total query duration vs time waiting to acquire a lock.<br><br>• <code>statement_timeout</code>: Aborts any statement that takes longer than the specified milliseconds from start to finish.<br>• <code>lock_timeout</code>: Aborts a statement only if it spends longer than specified trying to acquire a lock on a table or row.",
        "Topic": "Configuration",
        "Tags": "edb_postgres config timeouts locking"
    }
]

# Append the new cards
with open('edb_postgres_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in new_cards:
        writer.writerow(card)

print(f"Successfully added {len(new_cards)} more genuine cards to edb_postgres_deck.csv.")
