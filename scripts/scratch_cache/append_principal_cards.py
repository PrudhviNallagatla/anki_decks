import csv

principal_cards = [
    # --- LOW-LEVEL HEAP & ENGINE FORENSICS ---
    {
        "Question": "What is a HOT (Heap-Only Tuple) update, and why is it crucial for performance?",
        "Answer": "<b>ANSWER:</b> Updating a row without modifying any indexed columns, keeping the new tuple on the same 8KB page.<br><br>• <b>How it works:</b> Instead of updating every index on the table, Postgres points the old tuple directly to the new tuple on the same page. Index pointers remain untouched.<br>• <b>Benefit:</b> Drastically reduces write I/O and completely eliminates index bloat.",
        "Topic": "Engine Internals",
        "Tags": "edb_postgres internals hot_update vacuum"
    },
    {
        "Question": "Why does adding an index on a frequently updated column kill HOT updates?",
        "Answer": "<b>ANSWER:</b> Because HOT requires that NO indexed column is modified by the UPDATE statement.<br><br>If even a single indexed column is altered, Postgres is forced to perform a traditional update: inserting the new tuple AND creating new pointer entries in EVERY index on the table, multiplying write I/O and bloat.",
        "Topic": "Engine Internals",
        "Tags": "edb_postgres internals hot_update indexing"
    },
    {
        "Question": "How does setting table `fillfactor` enable HOT updates?",
        "Answer": "<b>ANSWER:</b> Reserves empty space inside each 8KB data page during initial INSERTs.<br><br><b>The SQL:</b><br><code>ALTER TABLE orders SET (fillfactor = 70);</code><br><br>By default, fillfactor is 100% (pages packed completely). Lowering it to 70–80% reserves 20–30% free space on every page for future UPDATEs, guaranteeing room for HOT updates on the same page.",
        "Topic": "Engine Internals",
        "Tags": "edb_postgres internals fillfactor hot_update"
    },
    {
        "Question": "What are the Visibility Map (`.vm`) and Free Space Map (`.fsm`) files?",
        "Answer": "<b>ANSWER:</b> Auxiliary storage files maintained alongside each table fork.<br><br>• <b>Visibility Map (`_vm`):</b> 2 bits per page. Bit 1: 'All-visible' (enables Index-Only Scans and lets VACUUM skip clean pages). Bit 2: 'All-frozen' (lets aggressive freeze vacuum skip pages).<br>• <b>Free Space Map (`_fsm`):</b> A binary tree tracking available bytes per page so INSERTs instantly find a target page without scanning.",
        "Topic": "Engine Internals",
        "Tags": "edb_postgres internals fsm vm storage"
    },
    {
        "Question": "What are 'Hint Bits' in a Postgres tuple header, and why do SELECTs generate write I/O?",
        "Answer": "<b>ANSWER:</b> Status flags (`HEAP_XMIN_COMMITTED`, `HEAP_XMAX_INVALID`) stamped directly on tuple headers.<br><br>When a transaction commits, Postgres marks WAL, not the row headers. The first query (even a `SELECT`) that visits those rows must check `pg_xact` to see if the creating transaction committed, and then 'stamps' the hint bits on the page, turning the page dirty and requiring a disk write.",
        "Topic": "Engine Internals",
        "Tags": "edb_postgres internals hint_bits mvcc io"
    },
    {
        "Question": "What is the `pageinspect` extension used for?",
        "Answer": "<b>ANSWER:</b> Inspecting raw disk page contents, tuple headers, and index internals using SQL.<br><br><b>The SQL:</b><br><code>CREATE EXTENSION pageinspect;</code><br><code>SELECT * FROM heap_page_items(get_raw_page('users', 0));</code><br><br>Reveals internal fields: `t_xmin`, `t_xmax`, `t_ctid`, `t_infomask`, and dead tuple fragmentation directly on disk.",
        "Topic": "Engine Internals",
        "Tags": "edb_postgres internals pageinspect forensics"
    },
    {
        "Question": "How does Postgres detect silent data corruption on disk using Data Checksums?",
        "Answer": "<b>ANSWER:</b> Storing an internal CRC checksum in every 8KB page header.<br><br>• <b>Enable:</b> At `initdb -k` time, or offline using <code>pg_checksums -e -D /path/to/data</code>.<br>• <b>Detection:</b> When Postgres reads a page from disk, it recalculates the checksum. If bit rot or controller corruption altered the page, it immediately throws a fatal error rather than returning corrupt data.",
        "Topic": "Disaster Recovery",
        "Tags": "edb_postgres corruption checksums storage"
    },

    # --- MAJOR UPGRADES & ZERO-DOWNTIME OPERATIONS ---
    {
        "Question": "What is `pg_upgrade --link` and why is it revolutionary for multi-terabyte upgrades?",
        "Answer": "<b>ANSWER:</b> Upgrades major Postgres versions in seconds using OS hard links.<br><br>Instead of copying terabytes of data files to the new cluster (which takes hours/days), `--link` creates filesystem hard links pointing to the existing physical files. An 8TB database can be upgraded in <b>under 1 minute</b>.",
        "Topic": "Database Upgrades",
        "Tags": "edb_postgres upgrade pg_upgrade link"
    },
    {
        "Question": "What is the primary risk of using `pg_upgrade --link`?",
        "Answer": "<b>ANSWER:</b> You cannot revert back to the old cluster once the new cluster starts modifying data.<br><br>Because both clusters share the exact same physical inodes on disk, any write to the new cluster permanently alters the old cluster's data files. Always take a pre-upgrade backup or filesystem LVM/ZFS snapshot.",
        "Topic": "Database Upgrades",
        "Tags": "edb_postgres upgrade pg_upgrade risk"
    },
    {
        "Question": "What step must a DBA always run before executing `pg_upgrade`?",
        "Answer": "<b>ANSWER:</b> Run the check mode: `pg_upgrade --check`.<br><br><b>The Command:</b><br><code>pg_upgrade -b /usr/edb/as16/bin -B /usr/edb/as17/bin -d /data16 -D /data17 --check</code><br><br>Verifies schema compatibility, data types, shared libraries, and tablespace paths with zero risk or downtime.",
        "Topic": "Database Upgrades",
        "Tags": "edb_postgres upgrade pg_upgrade check"
    },
    {
        "Question": "What post-upgrade tasks must immediately be executed after `pg_upgrade` completes?",
        "Answer": "<b>ANSWER:</b> Regenerate optimizer statistics and clean old files.<br><br>1. Run the generated script: <code>./vacuumdb --all --analyze-in-stages</code> (fast preliminary stats so initial queries don't hang).<br>2. Rebuild extension control files.<br>3. When satisfied, run <code>./delete_old_cluster.sh</code> to reclaim storage.",
        "Topic": "Database Upgrades",
        "Tags": "edb_postgres upgrade vacuumdb statistics"
    },
    {
        "Question": "How do you achieve near-zero downtime during a major version upgrade using Logical Replication?",
        "Answer": "<b>ANSWER:</b> Replicate live data between old and new version clusters concurrently.<br><br>1. Stand up new cluster running newer version (e.g. PG17).<br>2. Replicate schemas and establish Logical Replication from PG15 -> PG17.<br>3. Once lag hits 0ms, pause app writes briefly, sync sequences (`setval`), repoint connection pooler to PG17, and resume. Downtime is under 10 seconds.",
        "Topic": "Database Upgrades",
        "Tags": "edb_postgres upgrade logical_replication zero_downtime"
    },
    {
        "Question": "Why must sequences be manually synchronized after upgrading via Logical Replication?",
        "Answer": "<b>ANSWER:</b> Logical replication copies table data (INSERT/UPDATE/DELETE), NOT sequence values.<br><br>Because `nextval` calls on the publisher are not replicated across logical streams, sequence counters on the subscriber remain at initial values, causing subsequent INSERTs to fail with duplicate key violations.",
        "Topic": "Database Upgrades",
        "Tags": "edb_postgres upgrade logical_replication sequences"
    },

    # --- DISASTER RECOVERY & CORRUPTION HANDLING ---
    {
        "Question": "What is the `amcheck` extension and how do you verify index integrity?",
        "Answer": "<b>ANSWER:</b> Validates logical and physical consistency of B-Tree index structures.<br><br><b>The SQL:</b><br><code>CREATE EXTENSION amcheck;</code><br><code>SELECT bt_index_check(c.oid, true) FROM pg_index i JOIN pg_class c ON c.oid = i.indexrelid;</code><br><br>Detects corrupted index pages, out-of-order keys, and structural damage before queries fail.",
        "Topic": "Disaster Recovery",
        "Tags": "edb_postgres corruption amcheck indexing"
    },
    {
        "Question": "What is `pg_resetwal` (formerly `pg_resetxlog`) and why is it called the 'nuclear option'?",
        "Answer": "<b>ANSWER:</b> Forces a corrupt, unstartable Postgres database to start by wiping WAL logs.<br><br>• <b>What it does:</b> Clears the write-ahead log and resets transaction IDs.<br>• <b>Severe Consequence:</b> Destroys transaction consistency. Rows committed right before the crash are orphaned, and indexes may point to non-existent data.<br>• <b>Rule:</b> Only use when no backup exists. Immediately `pg_dumpall`, re-initdb, and reload.",
        "Topic": "Disaster Recovery",
        "Tags": "edb_postgres corruption pg_resetwal disaster"
    },
    {
        "Question": "What 3 configuration settings are required for Point-In-Time Recovery (PITR)?",
        "Answer": "<b>ANSWER:</b> `restore_command`, target criteria, and `recovery_target_action`.<br><br>1. <code>restore_command = 'cp /mnt/wal_archive/%f %p'</code><br>2. <code>recovery_target_time = '2026-09-03 00:00:00 EST'</code><br>3. <code>recovery_target_action = 'promote'</code> (promotes DB to read/write when target is reached).<br>Triggered by placing an empty `recovery.signal` file in `$PGDATA`.",
        "Topic": "Disaster Recovery",
        "Tags": "edb_postgres backup pitr config"
    },
    {
        "Question": "What does the `pg_archivecleanup` utility do?",
        "Answer": "<b>ANSWER:</b> Cleans up obsolete WAL files from an archive directory.<br><br>Used with `archive_cleanup_command` on standbys or in backup automation scripts to remove WAL segments older than the current standby restart point, preventing archived WAL disks from running out of space.",
        "Topic": "Disaster Recovery",
        "Tags": "edb_postgres backup pg_archivecleanup wal"
    },
    {
        "Question": "What is STONITH ('Shoot The Other Node In The Head') in High Availability clusters?",
        "Answer": "<b>ANSWER:</b> Automated fencing that forcefully cuts power to a failed primary node.<br><br>In HA architectures (like Patroni or Pacemaker), before a standby is promoted to primary, it must guarantee the old primary cannot accept writes (preventing Split-Brain). STONITH utilizes IPMI/iLO hardware controllers to reboot or kill the old node.",
        "Topic": "High Availability",
        "Tags": "edb_postgres ha stonith split_brain"
    },

    # --- EDB ADVANCED SERVER EXCLUSIVE SECURITY & PL/SQL ---
    {
        "Question": "What is Data Redaction (`DBMS_REDACT`) in EDB Postgres Advanced Server?",
        "Answer": "<b>ANSWER:</b> Dynamic on-the-fly masking of sensitive data returned by SELECT queries.<br><br>Physical table data remains unaltered and encrypted on disk. However, when non-exempt users query columns (e.g. Credit Card numbers), the data is masked (Full, Partial: `****-****-****-1234`, Random, or Regular Expression) based on application user role.",
        "Topic": "EDB Advanced Security",
        "Tags": "edb_postgres epas security dbms_redact"
    },
    {
        "Question": "What is `edb_sql_protect` and what are its three operation modes?",
        "Answer": "<b>ANSWER:</b> Built-in engine protection against SQL Injection attacks.<br><br>• <code>passive</code>: Logs SQL injection attempts to server log without blocking.<br>• <code>learn</code>: Records queries executed by trusted applications into a protected profile whitelist.<br>• <code>active</code>: Actively aborts and blocks any unauthorized query structure not on the learned profile.",
        "Topic": "EDB Advanced Security",
        "Tags": "edb_postgres epas security edb_sql_protect"
    },
    {
        "Question": "What is Virtual Private Database (`DBMS_RLS`) in EDB Postgres?",
        "Answer": "<b>ANSWER:</b> Fine-grained row-level security implemented via security policies.<br><br>A security function dynamically appends a SQL `WHERE` clause (predicate) to queries executed on a table, transparently restricting users to only viewing rows belonging to their tenant, department, or clearance level.",
        "Topic": "EDB Advanced Security",
        "Tags": "edb_postgres epas security dbms_rls vpd"
    },
    {
        "Question": "What is an Autonomous Transaction in EDB Postgres (`PRAGMA AUTONOMOUS_TRANSACTION`)?",
        "Answer": "<b>ANSWER:</b> A separate sub-transaction that can COMMIT independently of the parent transaction.<br><br>If a main business transaction fails and ROLLBACKs, an autonomous block inside a trigger or procedure can still successfully COMMIT audit logs or failure records without being undone.",
        "Topic": "EDB Advanced Server",
        "Tags": "edb_postgres epas plsql autonomous_transaction"
    },
    {
        "Question": "What is the EDB `wrap` utility used for?",
        "Answer": "<b>ANSWER:</b> Encrypting and obfuscating proprietary PL/SQL and SPL source code.<br><br><b>Command:</b><br><code>wrap -f my_package.sql -o my_package.wrap</code><br><br>Converts cleartext stored procedures, functions, and packages into encrypted bytecode, protecting intellectual property from being viewed in system catalogs (`pg_proc`).",
        "Topic": "EDB Advanced Security",
        "Tags": "edb_postgres epas security wrap obfuscation"
    },
    {
        "Question": "How does EDB Postgres enforce Password Profiles (`CREATE PROFILE`)?",
        "Answer": "<b>ANSWER:</b> Enforcing enterprise password policies at the database engine level.<br><br><b>The SQL:</b><br><code>CREATE PROFILE app_profile LIMIT PASSWORD_LIFE_TIME 90 FAILED_LOGIN_ATTEMPTS 3 PASSWORD_REUSE_MAX 5;</code><br><br>Assigns account expiration, failed login lockouts, and prevents password reuse.",
        "Topic": "EDB Advanced Security",
        "Tags": "edb_postgres epas security profiles passwords"
    },
    {
        "Question": "What are EDB Session Tags in `edb_audit`?",
        "Answer": "<b>ANSWER:</b> Custom tracking metadata injected into audit log records.<br><br>Allows applications to stamp web session IDs, client proxy IPs, or end-user identity into EDB audit trails via <code>SET edb_audit.session_tag = 'user_9921';</code>, linking backend database operations to real frontend users.",
        "Topic": "EDB Advanced Security",
        "Tags": "edb_postgres epas auditing session_tags"
    },

    # --- OS & MEMORY SIZING FORMULAS ---
    {
        "Question": "Why must Linux `vm.overcommit_memory` be set to 2 on Postgres database servers?",
        "Answer": "<b>ANSWER:</b> Prevents the Linux OS Out-Of-Memory (OOM) Killer from terminating Postgres backends.<br><br>• Default (`0`): Linux overcommits RAM, hoping processes won't use all allocated virtual memory. When RAM is exhausted, the OS suddenly kills the `postgres` postmaster.<br>• Setting `2`: OS refuses allocations that exceed `Swap + (RAM * overcommit_ratio)`, ensuring Postgres receives clean allocation failures rather than sudden OS SIGKILL terminations.",
        "Topic": "OS Tuning",
        "Tags": "edb_postgres os_tuning linux oom overcommit"
    },
    {
        "Question": "What is the comprehensive formula to estimate maximum potential Postgres RAM usage?",
        "Answer": "<b>ANSWER:</b> Total RAM = `shared_buffers + (max_connections * (work_mem * active_operators + temp_buffers)) + maintenance_work_mem`.<br><br>Because `work_mem` is allocated per sort/hash node (a single complex query can allocate 5x `work_mem`), setting high `max_connections` with large `work_mem` easily causes catastrophic memory exhaustion.",
        "Topic": "Performance Tuning",
        "Tags": "edb_postgres tuning memory formula oom"
    },
    {
        "Question": "What is the rule of thumb for configuring Parallel Query workers in `postgresql.conf`?",
        "Answer": "<b>ANSWER:</b> Three-tier worker hierarchy based on CPU cores.<br><br>• <code>max_worker_processes</code>: Global cap for all background workers (logical replication, parallel queries). Set to CPU core count.<br>• <code>max_parallel_workers</code>: Cap dedicated to parallel query execution (e.g. 75% of CPU cores).<br>• <code>max_parallel_workers_per_gather</code>: Max workers assigned to a single query plan (typically 2 to 4).",
        "Topic": "Performance Tuning",
        "Tags": "edb_postgres tuning parallel_query workers"
    },
    {
        "Question": "Why does setting `max_connections = 5000` severely degrade throughput even with ample RAM?",
        "Answer": "<b>ANSWER:</b> CPU context switching and lock contention on internal structures (like `ProcArrayLock`).<br><br>Every process connection must scan global lock arrays. Benchmarks show that routing 5,000 connections through PgBouncer into <b>100–200 active Postgres backend connections</b> yields 3x–5x higher query throughput than connecting 5,000 clients directly.",
        "Topic": "Performance Tuning",
        "Tags": "edb_postgres tuning connections procarraylock pgbouncer"
    },
    {
        "Question": "How do you calculate the exact number of Linux Huge Pages (`vm.nr_hugepages`) for Postgres?",
        "Answer": "<b>ANSWER:</b> Divide `shared_buffers` by Huge Page size (usually 2MB) + safety buffer.<br><br><b>Formula:</b><br><code>nr_hugepages = (shared_buffers_bytes / 2097152) + 100</code><br><br>Configured in `/etc/sysctl.conf`. Vastly reduces TLB (Translation Lookaside Buffer) cache misses in CPU memory management for large shared memory pools.",
        "Topic": "OS Tuning",
        "Tags": "edb_postgres os_tuning huge_pages memory"
    },
    {
        "Question": "What Linux dirty page writeback settings prevent system-wide I/O freezing during heavy write bursts?",
        "Answer": "<b>ANSWER:</b> `vm.dirty_background_ratio = 5` and `vm.dirty_ratio = 10`.<br><br>Linux defaults (e.g. 20–30%) allow gigabytes of dirty pages to accumulate in RAM before forcing a synchronous flush, which locks the storage subsystem and stalls database transactions. Lowering these ratios forces smooth, continuous background flushing.",
        "Topic": "OS Tuning",
        "Tags": "edb_postgres os_tuning linux io dirty_ratio"
    },
    {
        "Question": "What is the Linux kernel semaphore requirement for Postgres (`kernel.sem`)?",
        "Answer": "<b>ANSWER:</b> Minimum IPC semaphores required for process concurrency.<br><br><b>Recommended:</b> <code>sysctl -w kernel.sem=\"250 32000 100 128\"</code><br><br>Defines `semmsl` (max semaphores per array), `semmns` (max system-wide semaphores), `semopm` (max operations per semop call), and `semmni` (max semaphore sets). Insufficient semaphores prevent Postgres from starting.",
        "Topic": "OS Tuning",
        "Tags": "edb_postgres os_tuning semaphores kernel"
    }
]

# Append the 35 principal cards
with open('edb_postgres_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in principal_cards:
        writer.writerow(card)

print(f"Successfully appended {len(principal_cards)} Principal DBA cards.")
