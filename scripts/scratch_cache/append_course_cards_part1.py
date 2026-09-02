import csv

new_cards = [
    # --- MODULE: PEM & DATABASE MONITORING (from Chunks 01, 02, 03) ---
    {
        "Question": "What are the three core components of Postgres Enterprise Manager (PEM)?",
        "Answer": "<b>ANSWER:</b> PEM Server, PEM Agent, and PEM Web Client.<br><br>• <b>PEM Server:</b> The backend Postgres database repository storing metrics, alerts, and historical data.<br>• <b>PEM Agent:</b> A lightweight background service installed on each monitored host that collects metrics.<br>• <b>PEM Web Client:</b> The browser-based graphical management dashboard (built on pgAdmin 4).",
        "Topic": "Database Monitoring",
        "Tags": "edb_postgres pem monitoring architecture"
    },
    {
        "Question": "What script is used to configure the PEM Server on Linux after package installation?",
        "Answer": "<b>ANSWER:</b> <code>/usr/edb/pem/bin/configure-pem-server.sh</code><br><br>This interactive script configures: (1) whether to install Web Services, Database, or both, (2) database port and superuser credentials, (3) SSL certificates for secure agent communication.",
        "Topic": "Database Monitoring",
        "Tags": "edb_postgres pem installation linux"
    },
    {
        "Question": "How do you register a PEM Agent with the PEM Server from the command line?",
        "Answer": "<b>ANSWER:</b> Using the `pemworker` utility with `--register-agent`.<br><br><b>The Command:</b><br><code>/usr/edb/pem/agent/bin/pemworker --register-agent</code><br><br>Prompts for PEM Server IP, port, credentials, and agent description to establish mutual SSL trust.",
        "Topic": "Database Monitoring",
        "Tags": "edb_postgres pem agent registration"
    },
    {
        "Question": "What is the purpose of Postgres Cumulative Statistics Views?",
        "Answer": "<b>ANSWER:</b> Monitoring internal server activity metrics since the last statistics reset.<br><br>• <code>pg_stat_database</code>: Transactions committed/rolled back, blocks read/hit.<br>• <code>pg_stat_all_tables</code>: Seq scans, index scans, live vs dead tuples.<br>• <code>pg_statio_all_tables</code>: Disk block reads vs buffer cache hits.",
        "Topic": "Database Monitoring",
        "Tags": "edb_postgres monitoring statistics catalogs"
    },
    {
        "Question": "How do you log queries taking longer than a specific threshold (e.g. 5 seconds)?",
        "Answer": "<b>ANSWER:</b> Set `log_min_duration_statement` in `postgresql.conf`.<br><br><b>Configuration:</b><br><code>log_min_duration_statement = 5000</code><br><br>Value is in milliseconds (5000ms = 5s). Set to `0` to log all queries; set to `-1` to disable.",
        "Topic": "Database Monitoring",
        "Tags": "edb_postgres monitoring logging slow_query"
    },
    {
        "Question": "How do you find which session PID is blocking another session in Postgres?",
        "Answer": "<b>ANSWER:</b> Query `pg_blocking_pids()` in combination with `pg_stat_activity`.<br><br><b>The Query:</b><br><code>SELECT pid, pg_blocking_pids(pid) AS blocked_by, query <br>FROM pg_stat_activity <br>WHERE cardinality(pg_blocking_pids(pid)) > 0;</code>",
        "Topic": "Database Monitoring",
        "Tags": "edb_postgres monitoring locking locks"
    },

    # --- MODULE: SQL TUNING & PLANNER MECHANICS (from Chunks 03, 04) ---
    {
        "Question": "What are the 5 internal stages of SQL statement processing in Postgres?",
        "Answer": "<b>ANSWER:</b> Parse, Rewrite, Plan, Optimize, Execute.<br><br>1. <b>Parser:</b> Checks syntax and transforms SQL into a parse tree.<br>2. <b>Traffic Cop / Rewriter:</b> Applies rewrite rules (e.g. expanding Views).<br>3. <b>Planner/Optimizer:</b> Evaluates access paths and generates the lowest-cost execution plan.<br>4. <b>Executor:</b> Walks the plan tree and returns/modifies tuples.",
        "Topic": "SQL Tuning",
        "Tags": "edb_postgres tuning architecture statement"
    },
    {
        "Question": "What are the core Planner Cost Constants and their default values?",
        "Answer": "<b>ANSWER:</b> Unitless cost estimation metrics used by the query optimizer.<br><br>• <code>seq_page_cost = 1.0</code> (baseline cost for reading a sequential disk page)<br>• <code>random_page_cost = 4.0</code> (cost for random disk access, HDD default)<br>• <code>cpu_tuple_cost = 0.01</code> (CPU cost to process one row)<br>• <code>cpu_index_tuple_cost = 0.005</code> (CPU cost to process one index entry)<br>• <code>cpu_operator_cost = 0.0025</code> (CPU cost for comparison/operator)",
        "Topic": "SQL Tuning",
        "Tags": "edb_postgres tuning planner costs"
    },
    {
        "Question": "Why do DBAs lower `random_page_cost` from 4.0 to 1.1 on SSD/NVMe drives?",
        "Answer": "<b>ANSWER:</b> Because SSDs have virtually zero seek latency penalty.<br><br>At `4.0`, the planner assumes random reads are 4x slower than sequential reads, unfairly favoring Seq Scans. Lowering it to `1.1–1.5` accurately reflects SSD performance, encouraging the planner to use Index Scans where appropriate.",
        "Topic": "SQL Tuning",
        "Tags": "edb_postgres tuning ssd random_page_cost"
    },
    {
        "Question": "What does `EXPLAIN (ANALYZE, BUFFERS)` reveal that standard `EXPLAIN` does not?",
        "Answer": "<b>ANSWER:</b> Actual runtime and buffer cache usage.<br><br>• Standard `EXPLAIN`: Only shows the optimizer's *estimates* without running the query.<br>• `EXPLAIN ANALYZE`: Actually runs the query and displays actual execution time and row counts.<br>• `BUFFERS`: Displays exact buffer hits (`shared hit`), disk reads (`read`), and dirty pages (`dirtied`).",
        "Topic": "SQL Tuning",
        "Tags": "edb_postgres tuning explain buffers"
    },
    {
        "Question": "What are Query Optimizer Hints in EDB Postgres Advanced Server?",
        "Answer": "<b>ANSWER:</b> Directives inside comments that force the optimizer to choose a specific plan.<br><br><b>Examples:</b><br>• <code>/*+ IndexScan(emp emp_idx) */</code> - Force index scan.<br>• <code>/*+ HashJoin(a b) */</code> - Force hash join.<br>• <code>/*+ Leading(t1 (t2 t3)) */</code> - Dictate exact join order.<br>Supported in EDB via the `edb_hint_plan` extension.",
        "Topic": "SQL Tuning",
        "Tags": "edb_postgres tuning hints epas"
    },
    {
        "Question": "What does `default_statistics_target` control, and when should you raise it?",
        "Answer": "<b>ANSWER:</b> The number of histogram buckets stored in `pg_statistic` during `ANALYZE`.<br><br>Default is `100`. For columns with non-uniform data distribution or complex joins that produce inaccurate row estimates, raising it to `500` or `1000` (per column: <code>ALTER TABLE t ALTER c SET STATISTICS 500;</code>) yields vastly better plans.",
        "Topic": "SQL Tuning",
        "Tags": "edb_postgres tuning analyze statistics"
    },

    # --- MODULE: PERFORMANCE TUNING & BUFFER WARMING (from Chunk 05) ---
    {
        "Question": "What is the `pg_prewarm` extension and why is it used?",
        "Answer": "<b>ANSWER:</b> Loading table and index pages into the buffer cache ahead of time.<br><br>After a database restart, caches are 'cold', causing slow initial queries due to disk I/O. `pg_prewarm` warms the cache immediately so production traffic experiences zero initial slowdown.",
        "Topic": "Performance Tuning",
        "Tags": "edb_postgres tuning pg_prewarm memory"
    },
    {
        "Question": "How do you prewarm a specific table into shared buffers using `pg_prewarm`?",
        "Answer": "<b>ANSWER:</b> Run the `pg_prewarm` function in SQL.<br><br><b>The SQL:</b><br><code>CREATE EXTENSION pg_prewarm;</code><br><code>SELECT pg_prewarm('edbuser.customers');</code><br><br>Supported modes: `prefetch` (async OS read), `read` (sync OS read), and `buffer` (default, reads directly into Postgres shared_buffers).",
        "Topic": "Performance Tuning",
        "Tags": "edb_postgres tuning pg_prewarm sql"
    },
    {
        "Question": "How does `autoprewarm` work in EDB Postgres?",
        "Answer": "<b>ANSWER:</b> Automatically saves buffer state on shutdown and restores it on startup.<br><br><b>Configuration:</b><br>Add `pg_prewarm` to `shared_preload_libraries`. The background worker periodically records all buffer page IDs to disk (`autoprewarm_interval = 300s`). On server restart, it automatically restores those exact blocks to shared memory.",
        "Topic": "Performance Tuning",
        "Tags": "edb_postgres tuning autoprewarm config"
    },
    {
        "Question": "What are the three Background Writer (BGWRITER) tuning parameters?",
        "Answer": "<b>ANSWER:</b> `bgwriter_delay`, `bgwriter_lru_maxpages`, and `bgwriter_lru_multiplier`.<br><br>• <code>bgwriter_delay</code>: Sleep interval between rounds (default 200ms).<br>• <code>bgwriter_lru_maxpages</code>: Max dirty buffers written per round (default 100).<br>• <code>bgwriter_lru_multiplier</code>: Multiplier applied to average buffer demand to predict future needs (default 2.0).",
        "Topic": "Performance Tuning",
        "Tags": "edb_postgres tuning bgwriter memory"
    },
    {
        "Question": "What is `checkpoint_completion_target` and why should it be set to 0.9?",
        "Answer": "<b>ANSWER:</b> Spreads checkpoint I/O across the entire checkpoint interval.<br><br>If a checkpoint occurs every 15 minutes, a target of `0.9` tells Postgres to throttle dirty buffer disk writes over 13.5 minutes (90% of the window), preventing catastrophic disk I/O spikes that stall running transactions.",
        "Topic": "Performance Tuning",
        "Tags": "edb_postgres tuning checkpoint io"
    },
    {
        "Question": "What triggers an automatic checkpoint in Postgres?",
        "Answer": "<b>ANSWER:</b> Time elapsed OR Volume of WAL generated.<br><br>1. <b>Time:</b> `checkpoint_timeout` is reached (e.g. every 15 minutes).<br>2. <b>Volume:</b> WAL writes exceed `max_wal_size` (e.g. 16GB).<br>DBAs check logs: frequent WAL-driven checkpoints indicate `max_wal_size` should be increased.",
        "Topic": "Performance Tuning",
        "Tags": "edb_postgres tuning checkpoint wal"
    },

    # --- MODULE: EXTENSIONS & CLONING (from Chunks 06, 07) ---
    {
        "Question": "What three files make up a standard Postgres extension?",
        "Answer": "<b>ANSWER:</b> Control file, SQL script, and optional Shared Object.<br><br>1. <code>extension_name.control</code>: Metadata (version, dependencies, relocatability).<br>2. <code>extension_name--version.sql</code>: SQL commands defining tables, functions, and types.<br>3. <code>extension_name.so / .dll</code>: Compiled C library (if C functions are included).",
        "Topic": "Extensions",
        "Tags": "edb_postgres extensions architecture"
    },
    {
        "Question": "Why do some extensions require `shared_preload_libraries`?",
        "Answer": "<b>ANSWER:</b> Because they register background workers or install shared memory / hook intercepts.<br><br>Extensions like `pg_stat_statements`, `pg_prewarm`, and `auth_delay` must allocate shared memory structures and attach C-level function hooks at postmaster startup, requiring a database restart.",
        "Topic": "Extensions",
        "Tags": "edb_postgres extensions shared_preload_libraries"
    },
    {
        "Question": "How do you clone an entire database using SQL, and what is its major limitation?",
        "Answer": "<b>ANSWER:</b> Using `CREATE DATABASE ... TEMPLATE`.<br><br><b>The SQL:</b><br><code>CREATE DATABASE new_db TEMPLATE source_db;</code><br><br><b>Limitation:</b> No other active user sessions can be connected to `source_db` while the command runs. All connections must be terminated first.",
        "Topic": "Database Administration",
        "Tags": "edb_postgres admin clone template"
    },
    {
        "Question": "What is the EDB `edb_cloneschema` extension?",
        "Answer": "<b>ANSWER:</b> A specialized tool for cloning individual schemas within or between databases.<br><br>Requires `parallel_clone` in `shared_preload_libraries`. It can clone tables, indexes, constraints, and data in parallel threads without requiring connections to the source database to be dropped.",
        "Topic": "EDB Advanced Server",
        "Tags": "edb_postgres epas clone schema"
    },

    # --- MODULE: TRANSPARENT DATA ENCRYPTION (TDE) (from Chunk 07) ---
    {
        "Question": "When must Transparent Data Encryption (TDE) be enabled in EDB Postgres?",
        "Answer": "<b>ANSWER:</b> At database cluster initialization (`initdb`) time only.<br><br><b>The Command:</b><br><code>initdb -D /path/to/data -y --key-provider=...</code><br><br>TDE encrypts data files, WAL, and temporary files at rest. You cannot retroactively turn on TDE on an existing unencrypted cluster without migrating data.",
        "Topic": "Database Security",
        "Tags": "edb_postgres security tde encryption"
    },
    {
        "Question": "What encryption algorithms are supported by EDB Postgres TDE?",
        "Answer": "<b>ANSWER:</b> AES-128 and AES-256.<br><br>AES-128 is the default cipher (`tde_data_encryption_cipher = 'AES_128_CBC'`), but AES-256 (`AES_256_CBC`) is fully supported for enterprise security compliance.",
        "Topic": "Database Security",
        "Tags": "edb_postgres security tde aes"
    },
    {
        "Question": "How does key hierarchy work in EDB Transparent Data Encryption (TDE)?",
        "Answer": "<b>ANSWER:</b> Two-tier key architecture: Master Key and Data Encryption Key (DEK).<br><br>• <b>Data Encryption Key (DEK):</b> Used directly by the database engine to encrypt/decrypt blocks.<br>• <b>Master Key (Key Wrapping Key):</b> Encrypts the DEK. Stored externally in a Key Management Service (AWS KMS, HashiCorp Vault, or local file).",
        "Topic": "Database Security",
        "Tags": "edb_postgres security tde kms"
    },

    # --- MODULE: PSQL & EDB-PSQL TOOLING (from Chunk 09) ---
    {
        "Question": "Explain the difference between `psql` and `edb-psql`.",
        "Answer": "<b>ANSWER:</b> Community CLI vs EDB Enhanced CLI.<br><br>`psql` is the standard PostgreSQL command line interface. `edb-psql` is bundled with EDB Postgres Advanced Server and provides compatibility enhancements for Oracle-style syntax and EDB tools.",
        "Topic": "User Tools",
        "Tags": "edb_postgres tools psql edb-psql"
    },
    {
        "Question": "Name 5 essential `psql` meta-commands used daily by Postgres DBAs.",
        "Answer": "<b>ANSWER:</b> Core slash commands:<br><br>• <code>\\l+</code>: List all databases, owners, encodings, and physical sizes.<br>• <code>\\dt+</code>: List all tables with schema, owner, and disk footprint.<br>• <code>\\di+</code>: List all indexes and their sizes.<br>• <code>\\du+</code>: List all roles, permissions, and group memberships.<br>• <code>\\x</code>: Toggle Expanded display (formats columns vertically, essential for wide rows).",
        "Topic": "User Tools",
        "Tags": "edb_postgres tools psql meta_commands"
    },
    {
        "Question": "How do you run a SQL script file from inside `psql` and redirect output to a file?",
        "Answer": "<b>ANSWER:</b> Using `\\i` (input) and `\\o` (output).<br><br><b>The Commands:</b><br><code>\\o /tmp/query_results.txt</code> (redirects output)<br><code>\\i /path/to/script.sql</code> (executes the script file)<br><code>\\o</code> (resets output back to the terminal screen)",
        "Topic": "User Tools",
        "Tags": "edb_postgres tools psql script"
    },
    {
        "Question": "How do you display execution time for every query in `psql`?",
        "Answer": "<b>ANSWER:</b> Use the `\\timing` meta-command.<br><br><b>Command:</b><br><code>\\timing on</code><br><br>After enabling, every subsequent query will display: <code>Time: 12.345 ms</code> upon completion.",
        "Topic": "User Tools",
        "Tags": "edb_postgres tools psql timing"
    },

    # --- MODULE: SERVER LOGGING & ERROR TROUBLESHOOTING (from Chunks 10, 12) ---
    {
        "Question": "What parameters in `postgresql.conf` configure automatic log file rotation?",
        "Answer": "<b>ANSWER:</b> `logging_collector`, `log_filename`, `log_rotation_age`, and `log_rotation_size`.<br><br>• <code>logging_collector = on</code><br>• <code>log_directory = 'log'</code><br>• <code>log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'</code><br>• <code>log_rotation_age = 1d</code> (rotates daily)<br>• <code>log_rotation_size = 100MB</code> (rotates if size exceeds 100MB)",
        "Topic": "Configuration & Logging",
        "Tags": "edb_postgres logging rotation config"
    },
    {
        "Question": "What does `log_line_prefix` do, and what is a recommended production format?",
        "Answer": "<b>ANSWER:</b> Formats the metadata prepended to every log entry.<br><br><b>Recommended format:</b><br><code>log_line_prefix = '%m [%p] %u@%d client=%h '</code><br><br>• <code>%m</code> = timestamp with ms<br>• <code>%p</code> = process ID<br>• <code>%u</code> = username<br>• <code>%d</code> = database name<br>• <code>%h</code> = client remote host",
        "Topic": "Configuration & Logging",
        "Tags": "edb_postgres logging prefix troubleshooting"
    },
    {
        "Question": "What is the difference between `log_statement = 'ddl'`, `'mod'`, and `'all'`?",
        "Answer": "<b>ANSWER:</b> Filters which statement types are logged.<br><br>• <code>none</code>: Disables statement logging.<br>• <code>ddl</code>: Only logs CREATE, ALTER, DROP statements.<br>• <code>mod</code>: Logs DDL + all data-modifying queries (INSERT, UPDATE, DELETE, TRUNCATE).<br>• <code>all</code>: Logs every single query (including SELECT). Generates massive log volume.",
        "Topic": "Configuration & Logging",
        "Tags": "edb_postgres logging statements audit"
    },
    {
        "Question": "Troubleshoot this error: `psql: could not connect to server: Connection refused (0x0000274D/10061)`",
        "Answer": "<b>ANSWER:</b> The client cannot reach a listening service on that IP/port.<br><br><b>Checklist:</b><br>1. Is Postgres service running? (<code>systemctl status edb-as-17</code>)<br>2. Is Postgres listening on the port? Check `port` in `postgresql.conf`.<br>3. Check `listen_addresses` in `postgresql.conf` (if it's `localhost`, external IPs are refused).<br>4. Check OS firewall / iptables.",
        "Topic": "Troubleshooting",
        "Tags": "edb_postgres troubleshooting network connection"
    },
    {
        "Question": "Troubleshoot this error: `FATAL: no pg_hba.conf entry for host \"192.168.1.50\", user \"appuser\", database \"proddb\", no encryption`",
        "Answer": "<b>ANSWER:</b> The incoming connection does not match any entry in `pg_hba.conf`.<br><br><b>Fix:</b> Add an authorized line to `pg_hba.conf`:<br><code>host  proddb  appuser  192.168.1.50/32  scram-sha-256</code><br>Then run <code>SELECT pg_reload_conf();</code>. No restart required.",
        "Topic": "Troubleshooting",
        "Tags": "edb_postgres troubleshooting pg_hba security"
    },

    # --- MODULE: SCHEMAS, SEQUENCES & CONSTRAINTS (from Chunks 11, 13) ---
    {
        "Question": "What is a Schema in Postgres and what is the default schema?",
        "Answer": "<b>ANSWER:</b> A logical namespace within a database containing database objects.<br><br>The default schema is <code>public</code>. Schemas allow multiple users/applications to use the same database without table name collisions (e.g. `hr.employees` vs `sales.employees`).",
        "Topic": "Data Management",
        "Tags": "edb_postgres schemas ddl"
    },
    {
        "Question": "How does Postgres determine which schema to look in when a table name is unquoted?",
        "Answer": "<b>ANSWER:</b> Using the `search_path` configuration parameter.<br><br><b>Default:</b> <code>\"$user\", public</code><br>Postgres searches from left to right: first in a schema matching the current user's name, then in `public`. You can set it per session: <code>SET search_path TO myschema, public;</code>",
        "Topic": "Data Management",
        "Tags": "edb_postgres schemas search_path"
    },
    {
        "Question": "What are the three core sequence functions in Postgres?",
        "Answer": "<b>ANSWER:</b> `nextval()`, `currval()`, and `setval()`.<br><br>• <code>nextval('seq_name')</code>: Advances sequence and returns new value.<br>• <code>currval('seq_name')</code>: Returns most recent value generated by nextval in current session.<br>• <code>setval('seq_name', 1000)</code>: Manually resets sequence counter to specified value.",
        "Topic": "SQL Primer",
        "Tags": "edb_postgres sql sequences"
    },
    {
        "Question": "Why do Sequence values have gaps, and can rolled-back transactions be recovered?",
        "Answer": "<b>ANSWER:</b> Sequences never roll back (by design).<br><br>To allow high concurrency, `nextval` does not take transaction locks. If a transaction calls `nextval()`, receives ID `42`, and then ROLLBACKs, number 42 is permanently lost. This prevents transactions from blocking each other.",
        "Topic": "SQL Primer",
        "Tags": "edb_postgres sql sequences concurrency"
    },
    {
        "Question": "What is the difference between `SERIAL` and `IDENTITY` columns in Postgres 10+?",
        "Answer": "<b>ANSWER:</b> Legacy Postgres pseudo-type vs ANSI SQL standard.<br><br>• <code>SERIAL</code>: Automatically creates an underlying sequence and sets `DEFAULT nextval()`. Easy to bypass accidentally.<br>• <code>GENERATED ALWAYS AS IDENTITY</code>: Standard SQL compliant, integrates tightly with table metadata, and prevents manual insertion unless explicitly overridden.",
        "Topic": "SQL Primer",
        "Tags": "edb_postgres sql identity serial"
    },
    {
        "Question": "How do you add a CHECK constraint to a massive production table without locking it?",
        "Answer": "<b>ANSWER:</b> Use `NOT VALID` followed by `VALIDATE CONSTRAINT`.<br><br><b>Step 1:</b><br><code>ALTER TABLE orders ADD CONSTRAINT chk_price CHECK (price > 0) NOT VALID;</code><br>(Acquires brief lock, enforces only on new rows).<br><b>Step 2:</b><br><code>ALTER TABLE orders VALIDATE CONSTRAINT chk_price;</code><br>(Validates existing rows without blocking concurrent reads or writes).",
        "Topic": "SQL Primer",
        "Tags": "edb_postgres sql constraints production"
    },

    # --- MODULE: ADVANCED BACKUP OPTIONS & PG_DUMP FLAGS (from Chunk 14) ---
    {
        "Question": "What are the advantages of `pg_dump` Custom Format (`-F c`) over Plain Text (`-F p`)?",
        "Answer": "<b>ANSWER:</b> Compression, flexibility, and selective parallel restoration.<br><br>• Automatically compressed by default (saves disk space).<br>• Can be restored using `pg_restore`.<br>• Allows selective table/schema restoration without editing SQL files.<br>• Supports multi-job parallel restoration via `pg_restore -j <cores>`.",
        "Topic": "Backup & Recovery",
        "Tags": "edb_postgres backup pg_dump custom_format"
    },
    {
        "Question": "How do you dump only the data of a specific schema using `pg_dump`?",
        "Answer": "<b>ANSWER:</b> Combine the `-n` (schema) and `-a` (data-only) flags.<br><br><b>The Command:</b><br><code>pg_dump -U postgres -d edbstore -n edbuser -a -F c -f edbuser_data.dump</code>",
        "Topic": "Backup & Recovery",
        "Tags": "edb_postgres backup pg_dump schema data"
    },
    {
        "Question": "Why would you use `--disable-triggers` during a `pg_dump` or `pg_restore`?",
        "Answer": "<b>ANSWER:</b> To prevent cascading trigger execution during bulk restoration.<br><br>If tables have triggers that compute totals or insert audit rows, running them on millions of restored rows will drastically slow down the restore and duplicate audit entries. `--disable-triggers` turns them off during data copy.",
        "Topic": "Backup & Recovery",
        "Tags": "edb_postgres backup pg_dump triggers"
    },
    {
        "Question": "What does `pg_dumpall -g` (or `--globals-only`) dump?",
        "Answer": "<b>ANSWER:</b> Cluster-wide global objects only.<br><br>It exports cluster-level definitions that exist outside individual databases: (1) Roles, users, and passwords, and (2) Tablespace definitions. It dumps zero table or schema data.",
        "Topic": "Backup & Recovery",
        "Tags": "edb_postgres backup pg_dumpall globals"
    },
    {
        "Question": "How do you perform a parallel restore using `pg_restore`?",
        "Answer": "<b>ANSWER:</b> Use the `-j` (jobs) flag on a directory or custom archive dump.<br><br><b>The Command:</b><br><code>pg_restore -U enterprisedb -d target_db -j 4 /path/to/dump_dir</code><br><br>Restores multiple tables and indexes concurrently using 4 worker threads, reducing restore time drastically.",
        "Topic": "Backup & Recovery",
        "Tags": "edb_postgres backup pg_restore parallel"
    },

    # --- MODULE: HIGH-SPEED LOADING & STREAMING REPLICATION (from Chunks 15, 16) ---
    {
        "Question": "What is `COPY ... WITH (FREEZE)` and when should a DBA use it?",
        "Answer": "<b>ANSWER:</b> Freezes rows during initial bulk insertion into newly created tables.<br><br><b>The SQL:</b><br><code>COPY my_table FROM '/data/file.csv' WITH (FORMAT csv, FREEZE);</code><br><br>Pre-freezes tuples with frozen XIDs, eliminating the need for future VACUUM freeze passes on those rows. Must be run in the same transaction that created or truncated the table.",
        "Topic": "Data Loading",
        "Tags": "edb_postgres data_loading copy freeze"
    },
    {
        "Question": "What file in `$PGDATA` tells Postgres 12+ to start in Standby (Replica) mode?",
        "Answer": "<b>ANSWER:</b> `standby.signal`<br><br>In Postgres 12 and newer, `recovery.conf` was removed. Creating an empty file named `standby.signal` in the cluster data directory tells Postgres to start in read-only standby mode and stream WAL from the Primary.",
        "Topic": "Replication & HA",
        "Tags": "edb_postgres replication standby_signal"
    },
    {
        "Question": "What parameter in `postgresql.conf` configures how a standby connects to its primary?",
        "Answer": "<b>ANSWER:</b> `primary_conninfo`<br><br><b>Example:</b><br><code>primary_conninfo = 'host=192.168.1.10 port=5444 user=repuser password=secret'</code><br><br>Also pair with `primary_slot_name = 'standby_1_slot'` to associate connection with a replication slot.",
        "Topic": "Replication & HA",
        "Tags": "edb_postgres replication primary_conninfo"
    },
    {
        "Question": "How do you promote a Postgres Standby server to become the new Primary server?",
        "Answer": "<b>ANSWER:</b> Using `pg_ctl promote` or the SQL function `pg_promote()`.<br><br><b>CLI:</b><br><code>pg_ctl promote -D /var/lib/edb/as17/data</code><br><br><b>SQL:</b><br><code>SELECT pg_promote();</code><br><br>Postgres finishes replaying remaining WAL, removes `standby.signal`, switches WAL timeline, and begins accepting writes.",
        "Topic": "Replication & HA",
        "Tags": "edb_postgres replication promote failover"
    },
    {
        "Question": "What is Cascading Replication in Postgres?",
        "Answer": "<b>ANSWER:</b> A standby server streaming WAL to other standbys rather than from the primary.<br><br>Primary -> Standby 1 (Relay) -> Standby 2 & Standby 3.<br>This relieves network and CPU load on the Primary server when deploying many read replicas across multiple data centers.",
        "Topic": "Replication & HA",
        "Tags": "edb_postgres replication cascading"
    }
]

# Append the new cards
with open('edb_postgres_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in new_cards:
        writer.writerow(card)

print(f"Successfully added {len(new_cards)} genuine course cards to edb_postgres_deck.csv.")
