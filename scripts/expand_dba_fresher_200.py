import csv

extra_fresher_cards = [
    # --- REAL-WORLD OUTAGE & INCIDENT SCENARIOS ---
    {
        "Question": "The production database is completely frozen at 100% CPU. What are the first 3 commands you run to diagnose it?",
        "Answer": "<b>ANSWER:</b> (1) OS top, (2) Active sessions, and (3) Blocking lock trees.<br><br>1. <code>top -c</code>: Find which backend PIDs are burning CPU.<br>2. <code>SELECT pid, usename, state, query, age(clock_timestamp(), query_start) FROM pg_stat_activity WHERE state != 'idle' ORDER BY query_start ASC;</code>: Find the longest-running queries.<br>3. <code>SELECT pid, pg_blocking_pids(pid), query FROM pg_stat_activity WHERE cardinality(pg_blocking_pids(pid)) > 0;</code>: Find who is blocking whom.",
        "Topic": "Production Triage",
        "Tags": "dba postgres outage triage cpu locks"
    },
    {
        "Question": "A developer says: 'My query took 4 hours and didn't finish!' How do you diagnose why it hung?",
        "Answer": "<b>ANSWER:</b> Check if it is actively running or waiting on an exclusive lock.<br><br><b>Inspection SQL:</b><br><code>SELECT pid, wait_event_type, wait_event, state, query <br>FROM pg_stat_activity WHERE pid = 12345;</code><br>• If `wait_event_type = 'Lock'`: It is completely stuck waiting for another transaction to release a lock.<br>• If `wait_event_type = 'IO'`: It is stuck reading terabytes off slow disk.",
        "Topic": "Production Triage",
        "Tags": "dba postgres wait_events lock hung"
    },
    {
        "Question": "How do you add an index to a busy production table with 50 million rows without locking out users?",
        "Answer": "<b>ANSWER:</b> Use `CREATE INDEX CONCURRENTLY`.<br><br><b>The SQL:</b><br><code>CREATE INDEX CONCURRENTLY idx_users_email ON users (email);</code><br>• Standard `CREATE INDEX` takes a `ShareLock` that blocks all `INSERT`, `UPDATE`, and `DELETE` writes until done.<br>• `CONCURRENTLY` builds the index in two passes while allowing live continuous writes. Takes longer, but causes zero downtime.",
        "Topic": "Zero-Downtime Operations",
        "Tags": "dba postgres indexes concurrently zero_downtime"
    },
    {
        "Question": "What happens if a `CREATE INDEX CONCURRENTLY` fails or is cancelled halfway through?",
        "Answer": "<b>ANSWER:</b> It leaves behind an `INVALID` index that consumes disk space and degrades write performance.<br><br>Postgres marks it as invalid (`indisvalid = false`). The query planner will NEVER use it, but every subsequent `INSERT` must still write to it!<br><b>Fix:</b> You must manually run: <code>DROP INDEX CONCURRENTLY idx_name;</code> and rebuild it.",
        "Topic": "Zero-Downtime Operations",
        "Tags": "dba postgres indexes invalid concurrently fix"
    },
    {
        "Question": "What is Replication Lag in PostgreSQL and what causes it?",
        "Answer": "<b>ANSWER:</b> The delay between transactions committing on Primary and being applied on Standby.<br><br>• <b>Check lag:</b> Query `pg_stat_replication` on Primary.<br>• <b>Causes:</b> (1) Sudden massive batch writes generating gigabytes of WAL, (2) Slow network bandwidth between data centers, or (3) Long-running reporting queries on the Standby holding locks that conflict with incoming WAL replay.",
        "Topic": "Replication & HA",
        "Tags": "dba postgres replication lag monitoring"
    },
    {
        "Question": "What is an Orphaned Replication Slot and why is it a database killer?",
        "Answer": "<b>ANSWER:</b> An inactive replication slot from a decommissioned or dead standby replica.<br><br><b>The Disaster:</b> PostgreSQL promises never to delete WAL logs needed by an active slot. If the standby dies and nobody drops the slot, PostgreSQL will retain every single WAL file on disk indefinitely until the storage hits 100% full and crashes the primary server!",
        "Topic": "Replication & HA",
        "Tags": "dba postgres replication_slots wal disk_full disaster"
    },
    {
        "Question": "How do you find and drop an inactive/orphaned replication slot in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Query `pg_replication_slots` and call `pg_drop_replication_slot()`.<br><br><b>1. Find inactive slots:</b><br><code>SELECT slot_name, active, pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS retained_bytes <br>FROM pg_replication_slots WHERE active = false;</code><br><b>2. Drop it:</b><br><code>SELECT pg_drop_replication_slot('dead_replica_slot');</code>",
        "Topic": "Replication & HA",
        "Tags": "dba postgres replication_slots drop cleanup"
    },
    {
        "Question": "Why should every production PostgreSQL database have `statement_timeout` configured?",
        "Answer": "<b>ANSWER:</b> To prevent accidental runaway queries from hanging forever and exhausting resources.<br><br><b>Example in postgresql.conf:</b><br><code>statement_timeout = '30s'</code><br>Any query running longer than 30 seconds is automatically aborted with an error, preventing accidental cartesian product joins from freezing production.",
        "Topic": "Postgres Configuration",
        "Tags": "dba postgres statement_timeout configuration safety"
    },
    {
        "Question": "What is `idle_in_transaction_session_timeout` and why is it mandatory?",
        "Answer": "<b>ANSWER:</b> Automatically terminates sessions that opened a `BEGIN` transaction and went idle without committing.<br><br><b>The Hazard:</b> An idle transaction holds open an old transaction ID (`xmin`), which prevents Autovacuum from cleaning dead tuples across the entire database, causing severe table bloat.<br><b>Setting:</b> <code>idle_in_transaction_session_timeout = '10min'</code>.",
        "Topic": "Postgres Configuration",
        "Tags": "dba postgres idle_in_transaction timeouts bloat"
    },
    {
        "Question": "What happens when you add a column with a default value to a 100M-row table in PostgreSQL 11+?",
        "Answer": "<b>ANSWER:</b> It executes in 1 millisecond with zero table rewrite!<br><br><b>Syntax:</b> <code>ALTER TABLE orders ADD COLUMN status TEXT DEFAULT 'PENDING';</code><br>In Postgres 11+, default values are stored in system catalogs (`pg_attribute`), and missing column values are populated on the fly during reads. (Prior to Postgres 11, it rewrote all 100 million rows, locking the table for hours).",
        "Topic": "Zero-Downtime Operations",
        "Tags": "dba postgres alter_table default zero_downtime"
    },
    {
        "Question": "What is a Read-Only Transaction and why should reporting replicas use it?",
        "Answer": "<b>ANSWER:</b> A transaction mode that guarantees zero write locks or catalog changes.<br><br><b>The SQL:</b><br><code>BEGIN TRANSACTION READ ONLY;</code><br>Informs PostgreSQL that the transaction will only read. Prevents accidental `UPDATE`/`DELETE` bugs in analytics scripts and improves planner concurrency.",
        "Topic": "Transactions & ACID",
        "Tags": "dba postgres read_only transactions analytics"
    },
    {
        "Question": "How do you recover if a junior developer runs `UPDATE users SET status = 'INACTIVE';` without a WHERE clause?",
        "Answer": "<b>ANSWER:</b> Rollback if uncommitted, or Point-In-Time Recovery (PITR) if committed.<br><br>• <b>If inside an open transaction:</b> Immediately issue `ROLLBACK;` (all changes are instantly undone).<br>• <b>If committed:</b> Stop writes immediately and execute a PITR restore to 1 second before the update executed using base backup and WAL logs.",
        "Topic": "Production Triage",
        "Tags": "dba disaster update_without_where rollback pitr"
    },

    # --- ESSENTIAL POSTGRESQL EXTENSIONS ---
    {
        "Question": "How do you install and enable an extension in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> `CREATE EXTENSION extension_name;`<br><br><b>Example:</b><br><code>CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";</code><br>Installs pre-compiled C functions, datatypes, and operators into the database catalogs.",
        "Topic": "Postgres Extensions",
        "Tags": "dba postgres extensions create_extension"
    },
    {
        "Question": "What is `pg_stat_statements` and why is it a DBA's #1 query performance extension?",
        "Answer": "<b>ANSWER:</b> Tracks execution statistics for all SQL statements executed across the database.<br><br>Normalizes queries (replacing parameters with `$1, $2`) and records: total execution time, call count, rows returned, and RAM buffer cache hits. Requires `shared_preload_libraries = 'pg_stat_statements'` in `postgresql.conf`.",
        "Topic": "Postgres Extensions",
        "Tags": "dba postgres pg_stat_statements extensions tuning"
    },
    {
        "Question": "How do you find the Top 5 queries consuming the most total CPU time using `pg_stat_statements`?",
        "Answer": "<b>ANSWER:</b> Query `pg_stat_statements` sorted by `total_exec_time DESC`.<br><br><b>The SQL:</b><br><code>SELECT query, calls, round(total_exec_time::numeric, 2) AS total_ms, <br>       round(mean_exec_time::numeric, 2) AS avg_ms, rows <br>FROM pg_stat_statements <br>ORDER BY total_exec_time DESC LIMIT 5;</code>",
        "Topic": "Postgres Extensions",
        "Tags": "dba postgres pg_stat_statements slow_queries tuning"
    },
    {
        "Question": "What is `pg_repack` and why is it preferred over `VACUUM FULL`?",
        "Answer": "<b>ANSWER:</b> Online table and index bloat rebuilder with ZERO read or write locks.<br><br>• <b>`VACUUM FULL`:</b> Reclaims disk space by rewriting the table, but acquires an `AccessExclusiveLock` that blocks ALL reads and writes for hours.<br>• <b>`pg_repack`:</b> Rebuilds tables in the background using trigger logs while the application continues reading and writing freely.",
        "Topic": "Postgres Extensions",
        "Tags": "dba postgres pg_repack vacuum_full bloat"
    },
    {
        "Question": "What is `pgaudit` (PostgreSQL Audit Extension)?",
        "Answer": "<b>ANSWER:</b> An enterprise compliance extension providing granular session and object auditing.<br><br>Records detailed audit logs of who executed which `SELECT`, `INSERT`, `UPDATE`, or `DDL` statements, including session user and exact query text, for SOC2, HIPAA, and PCI compliance.",
        "Topic": "Postgres Extensions",
        "Tags": "dba postgres pgaudit compliance security"
    },
    {
        "Question": "What is `postgres_fdw` (Foreign Data Wrapper)?",
        "Answer": "<b>ANSWER:</b> Allows querying tables on remote PostgreSQL servers as if they were local tables.<br><br><b>Syntax:</b><br><code>CREATE SERVER remote_pg FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host '10.0.1.50', dbname 'sales');</code><br>You can join local customer tables directly with remote order tables across network servers using standard SQL.",
        "Topic": "Postgres Extensions",
        "Tags": "dba postgres fdw foreign_data_wrapper federation"
    },
    {
        "Question": "What is `pgcrypto` in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> A cryptographic extension providing in-database hashing and symmetric/asymmetric encryption.<br><br><b>Example:</b> Secure password hashing with bcrypt:<br><code>INSERT INTO users (password_hash) VALUES (crypt('MyPassword', gen_salt('bf')));</code>",
        "Topic": "Postgres Extensions",
        "Tags": "dba postgres pgcrypto encryption security"
    },
    {
        "Question": "How do you generate native UUIDs in PostgreSQL without installing third-party extensions?",
        "Answer": "<b>ANSWER:</b> Use the built-in `gen_random_uuid()` function.<br><br><b>The SQL:</b><br><code>CREATE TABLE devices (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT);</code><br>Built natively into core PostgreSQL (v13+) without requiring `uuid-ossp`.",
        "Topic": "Postgres Extensions",
        "Tags": "dba postgres uuid gen_random_uuid ddl"
    },
    {
        "Question": "Where must binary extensions like `pg_stat_statements` be enabled in `postgresql.conf`?",
        "Answer": "<b>ANSWER:</b> In `shared_preload_libraries`.<br><br><b>Config line:</b><br><code>shared_preload_libraries = 'pg_stat_statements, pgaudit'</code><br>Requires a full server restart to allocate shared memory structures before `CREATE EXTENSION` can be run in SQL.",
        "Topic": "Postgres Configuration",
        "Tags": "dba postgres shared_preload_libraries configuration"
    },
    {
        "Question": "How do you reset query statistics in `pg_stat_statements`?",
        "Answer": "<b>ANSWER:</b> Call `pg_stat_statements_reset()`.<br><br><b>The SQL:</b><br><code>SELECT pg_stat_statements_reset();</code><br>Clears all accumulated execution counters so you can benchmark performance before and after a query optimization deployment.",
        "Topic": "Postgres Extensions",
        "Tags": "dba postgres pg_stat_statements benchmark"
    },

    # --- PRODUCTION SIZING, UPGRADES & ARCHITECTURE NUANCE ---
    {
        "Question": "What is the difference between a PostgreSQL Minor Version Upgrade and a Major Version Upgrade?",
        "Answer": "<b>ANSWER:</b> Bugfix/security patch vs. On-disk format change.<br><br>• <b>Minor Upgrade (16.1 -> 16.2):</b> On-disk binary compatible. Simply replace binaries and restart service (takes 10 seconds).<br>• <b>Major Upgrade (15 -> 16):</b> Internal data catalog and storage formats change. Requires `pg_upgrade` or dumping/restoring data.",
        "Topic": "Maintenance & Upgrades",
        "Tags": "dba postgres upgrades major minor"
    },
    {
        "Question": "How does `pg_upgrade --link` perform multi-terabyte upgrades in under 2 minutes?",
        "Answer": "<b>ANSWER:</b> Creates Hard Links to existing data files instead of copying terabytes of disk blocks.<br><br>Upgrades system catalogs in memory and creates hard links pointing to the exact same disk blocks in the new `$PGDATA` directory, eliminating hours of disk copy I/O.",
        "Topic": "Maintenance & Upgrades",
        "Tags": "dba postgres pg_upgrade link zero_downtime"
    },
    {
        "Question": "What is Declarative Table Partitioning in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Splitting a giant logical table into smaller physical child tables based on a partition key.<br><br><b>The SQL:</b><br><code>CREATE TABLE logs (id BIGINT, log_date DATE) PARTITION BY RANGE (log_date);</code><br><code>CREATE TABLE logs_2024_01 PARTITION OF logs FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');</code>",
        "Topic": "Partitioning & Storage",
        "Tags": "dba postgres partitioning range ddl"
    },
    {
        "Question": "What is Partition Pruning in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> The query optimizer skipping child partition tables that cannot possibly match the query condition.<br><br>If querying <code>WHERE log_date = '2024-01-15'</code>, Postgres scans ONLY the `logs_2024_01` table and completely ignores all other 50 monthly partitions, slashing disk reads by 98%.",
        "Topic": "Partitioning & Storage",
        "Tags": "dba postgres partitioning pruning optimizer"
    },
    {
        "Question": "What are Tablespaces in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Mapping logical database objects to specific physical disk mount points on the server.<br><br><b>Use Case:</b> Place active, frequently queried indexes on ultra-fast NVMe SSDs (`/mnt/nvme`), and place historical archive tables on cheaper spinning hard drives (`/mnt/archive`).",
        "Topic": "Partitioning & Storage",
        "Tags": "dba postgres tablespaces storage nvme"
    },
    {
        "Question": "Why should `fsync` NEVER be set to `off` in production PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Disabling `fsync` guarantees catastrophic database corruption upon server crash or power loss.<br><br>`fsync` forces physical writes to permanent storage. If disabled, dirty buffers remain in the OS file cache; if power is cut, partial writes corrupt data block headers, rendering the database unstartable.",
        "Topic": "Postgres Configuration",
        "Tags": "dba postgres fsync corruption durability safety"
    },
    {
        "Question": "What does `synchronous_commit = off` do and when is it safe to use?",
        "Answer": "<b>ANSWER:</b> Asynchronous transaction commits for high write throughput.<br><br>Returns 'Commit Successful' to client as soon as WAL is written to RAM cache, flushing to disk in background.<br>• <b>Trade-off:</b> Survives software crashes without corruption, but power loss could lose the last ~200ms of committed transactions. Ideal for non-financial telemetry/analytics.",
        "Topic": "Postgres Configuration",
        "Tags": "dba postgres synchronous_commit wal performance"
    },
    {
        "Question": "What is `checkpoint_completion_target = 0.9` and why is it recommended?",
        "Answer": "<b>ANSWER:</b> Spreads disk write I/O evenly across 90% of the checkpoint duration.<br><br>Prevents 'checkpoint I/O spikes' where the database tries to flush 10GB of dirty buffers in 10 seconds, which would freeze client query latency. Spreading I/O provides smooth, consistent query performance.",
        "Topic": "Postgres Configuration",
        "Tags": "dba postgres checkpoint checkpoint_completion_target tuning"
    },
    {
        "Question": "What is `autovacuum_vacuum_scale_factor` and why should you lower it on massive tables?",
        "Answer": "<b>ANSWER:</b> The percentage of dead tuples required to trigger an automatic vacuum pass (default `0.2` or 20%).<br><br><b>The Problem:</b> On a 100-million row table, 20% means Autovacuum will NOT run until <b>20 million dead rows</b> accumulate!<br><b>Fix:</b> Lower scale factor on large tables: <code>ALTER TABLE orders SET (autovacuum_vacuum_scale_factor = 0.05);</code>.",
        "Topic": "Routine Maintenance",
        "Tags": "dba postgres autovacuum scale_factor tuning bloat"
    },
    {
        "Question": "What system view allows you to monitor the real-time progress of an active VACUUM job?",
        "Answer": "<b>ANSWER:</b> `pg_stat_progress_vacuum`<br><br><b>The SQL:</b><br><code>SELECT pid, phase, heap_blks_scanned, heap_blks_total, num_dead_tuples <br>FROM pg_stat_progress_vacuum;</code><br>Shows the current phase (scanning heap, vacuuming indexes) and percentage completed.",
        "Topic": "Routine Maintenance",
        "Tags": "dba postgres vacuum pg_stat_progress_vacuum monitoring"
    },
    {
        "Question": "What is `REINDEX CONCURRENTLY` in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Rebuilds a corrupted or bloated index in the background without blocking writes.<br><br><b>The SQL:</b><br><code>REINDEX INDEX CONCURRENTLY idx_users_email;</code><br>Replaces standard `REINDEX` (which locks out all writes). Frees wasted disk space and restores B-Tree balance safely online.",
        "Topic": "Routine Maintenance",
        "Tags": "dba postgres reindex concurrently maintenance"
    },

    # --- PRACTICAL JUNIOR DBA DRILLS & COMMANDS ---
    {
        "Question": "How do you check the human-readable total size of a table including its indexes?",
        "Answer": "<b>ANSWER:</b> Use `pg_size_pretty(pg_total_relation_size('table_name'))`.<br><br><b>The SQL:</b><br><code>SELECT pg_size_pretty(pg_total_relation_size('orders')) AS total_size, <br>       pg_size_pretty(pg_relation_size('orders')) AS table_only, <br>       pg_size_pretty(pg_indexes_size('orders')) AS index_size;</code>",
        "Topic": "Routine Maintenance",
        "Tags": "dba postgres size pg_total_relation_size storage"
    },
    {
        "Question": "How do you find the Top 5 most bloated tables with the highest number of dead tuples?",
        "Answer": "<b>ANSWER:</b> Query `pg_stat_user_tables` sorted by `n_dead_tup DESC`.<br><br><b>The SQL:</b><br><code>SELECT relname, n_live_tup, n_dead_tup, <br>       round(n_dead_tup::numeric / nullif(n_live_tup + n_dead_tup, 0) * 100, 2) AS dead_pct, <br>       last_vacuum, last_autovacuum <br>FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 5;</code>",
        "Topic": "Routine Maintenance",
        "Tags": "dba postgres bloat dead_tuples pg_stat_user_tables"
    },
    {
        "Question": "How do you check when the PostgreSQL server was started and its uptime?",
        "Answer": "<b>ANSWER:</b> Use `pg_postmaster_start_time()`.<br><br><b>The SQL:</b><br><code>SELECT pg_postmaster_start_time(), <br>       age(clock_timestamp(), pg_postmaster_start_time()) AS uptime;</code>",
        "Topic": "Routine Maintenance",
        "Tags": "dba postgres uptime start_time postmaster"
    },
    {
        "Question": "How do you manually promote a Standby replica to become the new Primary server?",
        "Answer": "<b>ANSWER:</b> Use `pg_promote()` in SQL or `pg_ctl promote` on OS shell.<br><br>• <b>SQL Method:</b> <code>SELECT pg_promote();</code><br>• <b>Shell Method:</b> <code>pg_ctl promote -D /data/dir</code><br>Signals the standby to finish applying active WAL streams, exit recovery mode, and begin accepting write transactions.",
        "Topic": "Replication & HA",
        "Tags": "dba postgres promote failover standby"
    },
    {
        "Question": "What is `pg_waldump` and when does a DBA use it?",
        "Answer": "<b>ANSWER:</b> Decodes binary WAL log files into human-readable transaction records.<br><br><b>Usage:</b><br><code>pg_waldump /data/pg_wal/000000010000000100000001</code><br>Used for forensic analysis to see what operations generated massive WAL bursts or caused table corruption.",
        "Topic": "Postgres Tools",
        "Tags": "dba postgres pg_waldump forensics wal"
    },
    {
        "Question": "How do you dump only a single specific table using `pg_dump`?",
        "Answer": "<b>ANSWER:</b> Use the `-t` (or `--table`) flag.<br><br><b>The Command:</b><br><code>pg_dump -U postgres -d proddb -t sales_orders -F c -f sales_orders.dump</code><br>Exports only `sales_orders` and its indexes without backing up the rest of the 500GB database.",
        "Topic": "Backup & Recovery",
        "Tags": "dba postgres pg_dump single_table backup"
    },
    {
        "Question": "How do you check if a Standby replica is actively receiving and applying WAL streams?",
        "Answer": "<b>ANSWER:</b> Query `pg_stat_wal_receiver` on the Standby server.<br><br><b>The SQL:</b><br><code>SELECT status, receive_start_lsn, written_lsn, flushed_lsn, sender_host <br>FROM pg_stat_wal_receiver;</code><br>Returns `status = 'streaming'` if actively connected and replicating.",
        "Topic": "Replication & HA",
        "Tags": "dba postgres pg_stat_wal_receiver standby replication"
    }
]

# Append extra cards to decks/dba_fresher_deck.csv
with open('decks/dba_fresher_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in extra_fresher_cards:
        writer.writerow(card)

print(f"Successfully added {len(extra_fresher_cards)} cards to dba_fresher_deck.csv!")
