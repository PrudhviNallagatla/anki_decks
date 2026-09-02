import csv
import os

# 1. Read existing fresher deck and filter out Oracle cards
kept_cards = []
with open('decks/dba_fresher_deck.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Topic'] == 'Oracle Architecture' or 'oracle' in row['Tags'].lower():
            continue
        kept_cards.append(row)

print(f"Kept {len(kept_cards)} general SQL, Linux, and foundational cards (purged Oracle).")

# 2. Add 77 new Postgres & RDBMS foundational cards
new_postgres_cards = [
    # --- THE ENGINE UNDER THE HOOD & STORAGE ---
    {
        "Question": "What is a Data Block (or Page) in a database?",
        "Answer": "<b>ANSWER:</b> The smallest physical chunk of data a database reads from or writes to disk (default 8KB in Postgres).<br><br><b>The Simple Explanation:</b><br>Databases never read a single row from disk. Even if you query for 1 small integer, the database must read the entire 8KB page that contains that row into RAM.",
        "Topic": "Storage & Engine",
        "Tags": "dba postgres architecture storage page block"
    },
    {
        "Question": "What is the Buffer Pool (or Shared Buffers in Postgres)?",
        "Answer": "<b>ANSWER:</b> A dedicated region of RAM used to cache data pages.<br><br><b>The Simple Explanation:</b><br>Reading from RAM is roughly 10,000x faster than reading from a hard drive. When you run a query, the database checks if the needed 8KB pages are already in the buffer pool (a <b>Cache Hit</b>). If not, it reads them from disk into RAM (a <b>Cache Miss</b>).",
        "Topic": "Storage & Engine",
        "Tags": "dba postgres memory buffer_pool shared_buffers"
    },
    {
        "Question": "What is a 'Dirty Page'?",
        "Answer": "<b>ANSWER:</b> A data block in RAM that has been modified (INSERT, UPDATE, DELETE) but has not yet been written to the permanent disk data file.<br><br><b>The Simple Explanation:</b><br>Writing to disk is slow. Databases modify pages in fast RAM first (marking them 'dirty') and write them to disk later in the background.",
        "Topic": "Storage & Engine",
        "Tags": "dba postgres memory dirty_page storage"
    },
    {
        "Question": "What is Write-Ahead Logging (WAL) and why is it essential?",
        "Answer": "<b>ANSWER:</b> Writing a record of every change to a sequential log file on disk BEFORE modifying the actual data files.<br><br><b>The Simple Explanation:</b><br>Writing sequential logs is blazing fast. If power fails or the server crashes while dirty pages are still in RAM, the database replays the WAL on restart to recover every committed transaction without data loss.",
        "Topic": "Storage & Engine",
        "Tags": "dba postgres wal durability acid"
    },
    {
        "Question": "What is a Checkpoint in a database?",
        "Answer": "<b>ANSWER:</b> The process of flushing all dirty pages from RAM to the permanent data files on disk.<br><br><b>The Simple Explanation:</b><br>Once a checkpoint completes, all previous WAL logs are safely persisted to disk and can be recycled. It creates a known 'safe baseline' for crash recovery.",
        "Topic": "Storage & Engine",
        "Tags": "dba postgres checkpoint memory storage"
    },
    {
        "Question": "What is the Postmaster process in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> The supervisor daemon that runs the entire PostgreSQL server.<br><br><b>The Simple Explanation:</b><br>It listens on port 5432 for incoming client connections, spawns a dedicated user backend process for each client session, and restarts background utility workers if they crash.",
        "Topic": "Postgres Architecture",
        "Tags": "dba postgres postmaster architecture"
    },
    {
        "Question": "What is Postgres's 'Process-per-Connection' architecture?",
        "Answer": "<b>ANSWER:</b> Every connected client gets its own dedicated operating system process (not a lightweight thread).<br><br><b>The Implication for DBAs:</b><br>Each connection consumes dedicated OS memory. If 2,000 clients connect directly, the server will run out of memory and crash. This is why connection poolers (like PgBouncer) are mandatory in production.",
        "Topic": "Postgres Architecture",
        "Tags": "dba postgres process connections pgbouncer"
    },
    {
        "Question": "What is a 'Heap Table' in relational databases?",
        "Answer": "<b>ANSWER:</b> A table where rows are stored on disk in no particular order.<br><br><b>The Simple Explanation:</b><br>When you INSERT rows, the database simply places them into the first available 8KB page with free space. You cannot assume rows come back in the order they were inserted unless you specify `ORDER BY`.",
        "Topic": "Storage & Engine",
        "Tags": "dba postgres storage heap"
    },
    {
        "Question": "What is an Item Pointer (or ctid / row ID) inside a page?",
        "Answer": "<b>ANSWER:</b> A small pointer at the top of an 8KB page that tells the database the exact byte offset where a row begins.<br><br>In Postgres, it is visible as the hidden `ctid` column (e.g. `(0, 1)` means Block 0, 1st item pointer). Indexes point directly to this ctid.",
        "Topic": "Storage & Engine",
        "Tags": "dba postgres internals ctid pointers"
    },
    {
        "Question": "How does MVCC (Multi-Version Concurrency Control) work in simple terms?",
        "Answer": "<b>ANSWER:</b> Readers never block writers, and writers never block readers.<br><br><b>The Simple Explanation:</b><br>When you UPDATE a row, Postgres does NOT overwrite the existing row on disk. It marks the old row as dead and inserts a brand new version of the row. Other transactions reading the table continue seeing the old version until your transaction commits.",
        "Topic": "Postgres Architecture",
        "Tags": "dba postgres mvcc concurrency"
    },
    {
        "Question": "What is a 'Dead Tuple' and why does table bloat happen?",
        "Answer": "<b>ANSWER:</b> An old, obsolete row version left behind after an UPDATE or DELETE.<br><br><b>The Simple Explanation:</b><br>Because Postgres leaves old rows on disk for concurrent readers, thousands of updates generate thousands of dead rows ('bloat'). If not cleaned up, tables become massive and queries slow to a crawl.",
        "Topic": "Postgres Architecture",
        "Tags": "dba postgres bloat dead_tuples mvcc"
    },
    {
        "Question": "What does the `VACUUM` command do in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Scans tables for dead tuples and marks their space as available for reuse by future INSERTs.<br><br><b>Crucial Note:</b> Standard `VACUUM` does NOT return disk space to the OS; it keeps the space inside the table file so future rows don't require allocating new disk blocks.",
        "Topic": "Routine Maintenance",
        "Tags": "dba postgres vacuum maintenance bloat"
    },
    {
        "Question": "What is Autovacuum and why should you NEVER turn it off in production?",
        "Answer": "<b>ANSWER:</b> A background daemon that automatically runs VACUUM and ANALYZE on bloated tables.<br><br><b>The Danger:</b> If turned off, tables accumulate millions of dead rows, indexes explode in size, queries become 100x slower, and the database will eventually shut down due to Transaction ID wraparound.",
        "Topic": "Routine Maintenance",
        "Tags": "dba postgres autovacuum maintenance"
    },
    {
        "Question": "What is the Visibility Map (`.vm`) in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> A small auxiliary file tracking which 8KB pages contain only live, committed tuples.<br><br><b>Why it matters:</b> (1) Enables **Index-Only Scans** (Postgres can answer queries directly from an index without visiting the table heap), and (2) Allows VACUUM to skip clean pages, speeding up maintenance 10x.",
        "Topic": "Storage & Engine",
        "Tags": "dba postgres visibility_map internals"
    },
    {
        "Question": "What is the Free Space Map (`.fsm`) in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> A binary map tracking how many free bytes exist on each 8KB page in a table.<br><br>When a new row is inserted, Postgres checks the `.fsm` to instantly find a page with enough free room, avoiding a slow sequential scan across disk files.",
        "Topic": "Storage & Engine",
        "Tags": "dba postgres fsm storage internals"
    },

    # --- HOW A QUERY RUNS (FROM ENTER TO OUTPUT) ---
    {
        "Question": "What are the 4 main stages a database goes through to execute a SQL query?",
        "Answer": "<b>ANSWER:</b> Parser -> Catalog Check -> Optimizer/Planner -> Execution Engine.<br><br>1. <b>Parser:</b> Checks SQL syntax for errors.<br>2. <b>Catalog Check:</b> Verifies tables/columns exist and checks user privileges.<br>3. <b>Optimizer:</b> Compares costs to pick the fastest execution path (index vs table scan).<br>4. <b>Executor:</b> Pulls 8KB pages into RAM, filters rows, and returns results.",
        "Topic": "Query Lifecycle",
        "Tags": "dba postgres query_lifecycle parser optimizer"
    },
    {
        "Question": "What is a Full Table Scan (Sequential Scan)?",
        "Answer": "<b>ANSWER:</b> Reading every single 8KB page of a table from the first block to the last block on disk.<br><br><b>When it's slow:</b> Searching for 1 user out of 10 million rows without an index forces the database to read hundreds of gigabytes off disk.<br><b>When it's fast:</b> If the table has only 50 rows, reading the whole table in 1 disk read is faster than searching an index.",
        "Topic": "Query Lifecycle",
        "Tags": "dba postgres scan seq_scan performance"
    },
    {
        "Question": "What is an Index Scan and how does a B-Tree index work?",
        "Answer": "<b>ANSWER:</b> Traversing a balanced tree structure to jump directly to specific row locations.<br><br><b>The Textbook Analogy:</b><br>Instead of reading all 500 pages of a book to find 'PostgreSQL', you look up 'PostgreSQL' in the back index, which says 'Page 42'. The database jumps directly to block 42 on disk.",
        "Topic": "Indexes & Performance",
        "Tags": "dba postgres indexes btree scan"
    },
    {
        "Question": "What is an Index-Only Scan?",
        "Answer": "<b>ANSWER:</b> An execution path where all columns requested by the query exist inside the index leaf nodes.<br><br><b>Example:</b> If you have an index on `(id, email)` and run `SELECT email FROM users WHERE id = 10;`, the database gets the email directly from the index without reading the actual table heap at all.",
        "Topic": "Indexes & Performance",
        "Tags": "dba postgres indexes index_only_scan"
    },
    {
        "Question": "What is the difference between a Clustered Index and a Non-Clustered Index?",
        "Answer": "<b>ANSWER:</b> Physical row order vs. Pointer lookup.<br><br>• <b>Clustered Index:</b> The physical rows on disk are physically sorted in the exact order of the index (like a telephone directory sorted by last name). A table can have only ONE clustered index.<br>• <b>Non-Clustered Index:</b> A separate auxiliary structure pointing to the physical row locations (like an index at the back of a book).",
        "Topic": "Indexes & Performance",
        "Tags": "dba database indexes clustered non_clustered"
    },
    {
        "Question": "Why does having too many indexes slow down database write operations?",
        "Answer": "<b>ANSWER:</b> Every `INSERT`, `UPDATE`, and `DELETE` must update every single index on the table.<br><br>If a table has 10 indexes, inserting 1 row requires writing to the table PLUS updating 10 separate B-Trees on disk, multiplying write I/O and locking overhead.",
        "Topic": "Indexes & Performance",
        "Tags": "dba postgres indexes performance writes"
    },
    {
        "Question": "What is the `EXPLAIN` command in SQL?",
        "Answer": "<b>ANSWER:</b> A command that reveals the execution plan chosen by the query optimizer.<br><br><b>Syntax:</b> `EXPLAIN SELECT * FROM users WHERE email = 'a@b.com';`<br>It tells you: Will it use an Index Scan or Seq Scan? What join algorithm will it use? How much memory will it consume?",
        "Topic": "Query Lifecycle",
        "Tags": "dba postgres explain query_plan"
    },
    {
        "Question": "What is the difference between `EXPLAIN` and `EXPLAIN ANALYZE`?",
        "Answer": "<b>ANSWER:</b> Estimates vs. Actual Execution.<br><br>• <b>`EXPLAIN`:</b> Shows the optimizer's *predictions* without actually running the query.<br>• <b>`EXPLAIN ANALYZE`:</b> Actually executes the query, showing the real elapsed time in milliseconds and real row counts compared to the estimates.",
        "Topic": "Query Lifecycle",
        "Tags": "dba postgres explain_analyze tuning"
    },
    {
        "Question": "What does 'Cold Cache' vs. 'Warm Cache' mean in query performance?",
        "Answer": "<b>ANSWER:</b> Data on slow physical disk vs. data already cached in fast RAM.<br><br>• <b>Cold Cache:</b> The database just restarted. The first time a query runs, it must read pages from slow disk (takes 5 seconds).<br>• <b>Warm Cache:</b> The pages are now cached in RAM. Running the exact same query a second time takes 2 milliseconds.",
        "Topic": "Query Lifecycle",
        "Tags": "dba postgres cache memory performance"
    },

    # --- TRANSACTIONS & ACID IN PLAIN ENGLISH ---
    {
        "Question": "What is a Database Transaction (`BEGIN`, `COMMIT`, `ROLLBACK`)?",
        "Answer": "<b>ANSWER:</b> A unit of work consisting of one or more SQL statements treated as a single indivisible operation.<br><br>• <code>BEGIN;</code>: Starts the transaction.<br>• <code>COMMIT;</code>: Makes all changes permanent on disk.<br>• <code>ROLLBACK;</code>: Aborts and cancels all changes as if they never happened.",
        "Topic": "Transactions & ACID",
        "Tags": "dba database transactions commit rollback"
    },
    {
        "Question": "Explain Atomicity (the 'A' in ACID) using a bank transfer example.",
        "Answer": "<b>ANSWER:</b> 'All or Nothing.'<br><br><b>Scenario:</b> Alice sends \$100 to Bob.<br>1. Deduct \$100 from Alice.<br>2. Add \$100 to Bob.<br>If the server crashes right after step 1, Atomicity guarantees step 1 is rolled back. Alice's \$100 is not lost into thin air.",
        "Topic": "Transactions & ACID",
        "Tags": "dba database acid atomicity"
    },
    {
        "Question": "Explain Consistency (the 'C' in ACID).",
        "Answer": "<b>ANSWER:</b> The database must transition only from one valid state to another valid state.<br><br>Any transaction that violates defined rules (Primary Keys, Foreign Keys, CHECK constraints, NOT NULL) is immediately rejected and aborted, preserving integrity.",
        "Topic": "Transactions & ACID",
        "Tags": "dba database acid consistency"
    },
    {
        "Question": "Explain Isolation (the 'I' in ACID) with a concert ticket example.",
        "Answer": "<b>ANSWER:</b> Concurrent transactions cannot interfere with each other.<br><br><b>Scenario:</b> Only 1 concert seat remains. Alice and Bob click 'Buy' at the exact same millisecond. Isolation guarantees the transactions execute as if they ran sequentially—Alice gets the seat, and Bob's transaction is told the seat is sold out.",
        "Topic": "Transactions & ACID",
        "Tags": "dba database acid isolation"
    },
    {
        "Question": "Explain Durability (the 'D' in ACID).",
        "Answer": "<b>ANSWER:</b> Once a transaction is committed, its changes survive power loss, crashes, or system restarts.<br><br>Guaranteed by writing the transaction's WAL log to non-volatile storage before sending the 'Commit Successful' message to the client.",
        "Topic": "Transactions & ACID",
        "Tags": "dba database acid durability wal"
    },
    {
        "Question": "What is the difference between a Shared Lock and an Exclusive Lock?",
        "Answer": "<b>ANSWER:</b> Read Lock vs. Write Lock.<br><br>• <b>Shared Lock (Read):</b> Acquired by `SELECT`. Multiple users can hold shared locks on the same row simultaneously (readers don't block readers).<br>• <b>Exclusive Lock (Write):</b> Acquired by `UPDATE`, `DELETE`. Only ONE transaction can hold it, blocking all other transactions from modifying or locking that row.",
        "Topic": "Locks & Concurrency",
        "Tags": "dba database locking shared_lock exclusive_lock"
    },
    {
        "Question": "What is a Deadlock in a database?",
        "Answer": "<b>ANSWER:</b> When two transactions block each other indefinitely, each waiting for a lock held by the other.<br><br><b>The Traffic Gridlock Analogy:</b><br>• Tx1 locks Row A, wants Row B.<br>• Tx2 locks Row B, wants Row A.<br>Neither can move. The database detects this after a timeout, picks one transaction as the 'victim', and aborts/rolls it back with an error.",
        "Topic": "Locks & Concurrency",
        "Tags": "dba database locking deadlock"
    },
    {
        "Question": "What is a Savepoint in SQL?",
        "Answer": "<b>ANSWER:</b> A checkpoint inside a transaction that allows rolling back part of the transaction without aborting the whole thing.<br><br><b>Syntax:</b><br><code>SAVEPOINT step1;</code><br><code>-- do some risky work...</code><br><code>ROLLBACK TO SAVEPOINT step1; -- undoes only risky work</code><br><code>COMMIT; -- commits previous safe work</code>",
        "Topic": "Transactions & ACID",
        "Tags": "dba sql savepoint transactions"
    },

    # --- JUNIOR DBA DAILY PLAYBOOK & DISASTERS ---
    {
        "Question": "What are the 4 items on a Junior DBA's Daily Morning Health Check?",
        "Answer": "<b>ANSWER:</b> The first 4 things a DBA checks at 9:00 AM every day:<br><br>1. <b>Backups:</b> Did last night's automated backup jobs complete successfully?<br>2. <b>Disk Space:</b> Are any filesystems (data, logs, archive) over 80–85% full?<br>3. <b>Alerts & Logs:</b> Are there critical errors or fatal crash notices in the database log?<br>4. <b>Long-running Queries & Locks:</b> Are any hung sessions blocking production users?",
        "Topic": "Junior DBA Playbook",
        "Tags": "dba operations daily_check health_check"
    },
    {
        "Question": "Why is 'Disk 100% Full' the #1 cause of catastrophic database crashes?",
        "Answer": "<b>ANSWER:</b> Databases cannot commit transactions if they cannot write WAL logs to disk.<br><br>When the storage disk hits 100%, Postgres immediately halts writing and will abruptly shut down or enter panic mode to prevent data corruption. Monitoring disk space with alerts at 85% is a DBA's primary duty.",
        "Topic": "Junior DBA Playbook",
        "Tags": "dba operations disk_space monitoring panic"
    },
    {
        "Question": "What is the difference between a Logical Backup and a Physical Backup?",
        "Answer": "<b>ANSWER:</b> SQL text statements vs. Raw binary storage files.<br><br>• <b>Logical Backup (`pg_dump`):</b> Generates SQL statements (`CREATE TABLE`, `INSERT INTO`) to recreate the data. Flexible and version-independent, but slow to restore on large 5TB+ databases.<br>• <b>Physical Backup (`pg_basebackup`):</b> Copies the raw binary 8KB data blocks from disk. Extremely fast to restore, and forms the foundation for Point-In-Time Recovery.",
        "Topic": "Backup & Recovery",
        "Tags": "dba backup logical physical pg_dump pg_basebackup"
    },
    {
        "Question": "What is the difference between a Hot Backup and a Cold Backup?",
        "Answer": "<b>ANSWER:</b> Online backup while running vs. Offline backup with database stopped.<br><br>• <b>Hot Backup:</b> Database remains 100% online; users continue reading and writing. (Uses WAL archiving to ensure consistency).<br>• <b>Cold Backup:</b> Database service is completely shut down before copying files. Simple, but unacceptable for 24/7 business applications.",
        "Topic": "Backup & Recovery",
        "Tags": "dba backup hot_backup cold_backup"
    },
    {
        "Question": "What is Point-In-Time Recovery (PITR)?",
        "Answer": "<b>ANSWER:</b> The ability to restore a database to any specific second in the past.<br><br><b>The Disaster Scenario:</b><br>At 2:14 PM, a developer accidentally drops the `orders` table. A DBA restores Sunday's physical base backup, replays WAL logs sequentially, and stops replay at exactly <b>2:13:59 PM</b>, recovering all data right before the accidental drop.",
        "Topic": "Backup & Recovery",
        "Tags": "dba backup pitr disaster_recovery"
    },
    {
        "Question": "What is Database Replication (Primary vs. Standby)?",
        "Answer": "<b>ANSWER:</b> Continuously copying data from a primary server to one or more secondary servers.<br><br>• <b>Primary (Leader):</b> Handles all read and write queries.<br>• <b>Standby (Replica):</b> Receives continuous WAL streams from the primary. Can serve read-only reporting queries and is ready to take over if the Primary dies.",
        "Topic": "Replication & HA",
        "Tags": "dba replication primary standby ha"
    },
    {
        "Question": "What is the difference between Synchronous and Asynchronous Replication?",
        "Answer": "<b>ANSWER:</b> Zero Data Loss vs. Maximum Speed.<br><br>• <b>Synchronous:</b> The Primary waits for the Standby to confirm it received the WAL before telling the user 'Commit Successful'. Guaranteed zero data loss, but slower.<br>• <b>Asynchronous:</b> The Primary commits immediately and streams WAL in the background. Faster, but a few milliseconds of data could be lost if the Primary catches fire.",
        "Topic": "Replication & HA",
        "Tags": "dba replication synchronous asynchronous"
    },
    {
        "Question": "What do RPO and RTO mean in Disaster Recovery?",
        "Answer": "<b>ANSWER:</b> Recovery Point Objective and Recovery Time Objective.<br><br>• <b>RPO (Data Loss Window):</b> How much data can the business afford to lose? (e.g. RPO = 5 minutes means you can lose at most 5 minutes of transactions).<br>• <b>RTO (Downtime Window):</b> How long can the business afford to be offline while you fix it? (e.g. RTO = 1 hour).",
        "Topic": "Junior DBA Playbook",
        "Tags": "dba disaster_recovery rpo rto ha"
    },
    {
        "Question": "What are the 5 components of a standard Database Connection String?",
        "Answer": "<b>ANSWER:</b> Host, Port, Database Name, Username, and Password.<br><br><b>Example:</b><br><code>postgresql://app_user:secret123@192.168.1.50:5432/sales_db</code><br>• <b>Host:</b> Server IP / hostname.<br>• <b>Port:</b> TCP listening port (5432 for Postgres).<br>• <b>DB Name:</b> Target database.<br>• <b>User & Password:</b> Authentication credentials.",
        "Topic": "Junior DBA Playbook",
        "Tags": "dba networking connection_string basics"
    },
    {
        "Question": "Why do web applications use Connection Pooling (like PgBouncer)?",
        "Answer": "<b>ANSWER:</b> Reusing a small pool of database connections for thousands of web users.<br><br>Creating a database connection takes 50–100ms and consumes 5–10MB RAM per process. If 3,000 web users hit the site, connection pooling channels those 3,000 requests through just 50 reusable, warm connections, preventing server crashes.",
        "Topic": "Junior DBA Playbook",
        "Tags": "dba networking connection_pooling pgbouncer"
    },
    {
        "Question": "What is `pg_hba.conf` in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> The host-based authentication firewall file for PostgreSQL.<br><br>It controls: (1) What IP addresses or subnets can connect, (2) To which databases, (3) Under which usernames, and (4) What authentication method (e.g. `scram-sha-256`, `md5`, `peer`) must be used.",
        "Topic": "Postgres Security",
        "Tags": "dba postgres security pg_hba authentication"
    },
    {
        "Question": "How do you create a read-only reporting user in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Use `CREATE ROLE` and `GRANT SELECT`.<br><br><b>The SQL:</b><br><code>CREATE ROLE analyst_user WITH LOGIN PASSWORD 'SecurePass123';</code><br><code>GRANT CONNECT ON DATABASE proddb TO analyst_user;</code><br><code>GRANT USAGE ON SCHEMA public TO analyst_user;</code><br><code>GRANT SELECT ON ALL TABLES IN SCHEMA public TO analyst_user;</code>",
        "Topic": "Postgres Security",
        "Tags": "dba postgres security grant roles"
    },

    # --- ESSENTIAL LINUX SKILLS FOR POSTGRES DBAs ---
    {
        "Question": "What Linux command checks disk space utilization across filesystems?",
        "Answer": "<b>ANSWER:</b> `df -h`<br><br><b>Usage:</b><br>Displays mounted disks, total sizes, used space, and percentage full in human-readable format (GB/TB). If `/var/lib/postgresql` or `/` is at 95%, immediate action is required.",
        "Topic": "Linux for DBAs",
        "Tags": "dba linux storage df commands"
    },
    {
        "Question": "What Linux command checks RAM and Swap memory usage?",
        "Answer": "<b>ANSWER:</b> `free -m` (or `free -h`)<br><br><b>Usage:</b><br>Displays total, used, and free RAM in Megabytes. If the `Swap: used` number is rapidly increasing, the server is running out of physical RAM and swapping to slow disk.",
        "Topic": "Linux for DBAs",
        "Tags": "dba linux memory free swap"
    },
    {
        "Question": "How do you check if PostgreSQL is currently running on a Linux server?",
        "Answer": "<b>ANSWER:</b> Using `systemctl status postgresql` or checking process table.<br><br><b>The Command:</b><br><code>systemctl status postgresql</code><br>Or inspect process list:<br><code>ps aux | grep postgres</code><br>Shows whether the postmaster daemon is active, its PID, and running backends.",
        "Topic": "Linux for DBAs",
        "Tags": "dba linux systemctl process status"
    },
    {
        "Question": "What is the difference between `kill -15` (SIGTERM) and `kill -9` (SIGKILL)?",
        "Answer": "<b>ANSWER:</b> Graceful shutdown vs. Forceful process termination.<br><br>• <b>`kill -15 <pid>` (SIGTERM):</b> Polite request. Tells Postgres to finish active writes, flush dirty buffers, release locks, and exit cleanly.<br>• <b>`kill -9 <pid>` (SIGKILL):</b> Sudden execution by OS kernel. Process dies instantly. Never flushes buffers, forcing the database to enter crash recovery on restart.",
        "Topic": "Linux for DBAs",
        "Tags": "dba linux kill processes administration"
    },
    {
        "Question": "How do you follow the live PostgreSQL server error log in real-time on Linux?",
        "Answer": "<b>ANSWER:</b> Use the `tail -f` command.<br><br><b>The Command:</b><br><code>tail -f /var/log/postgresql/postgresql-16-main.log</code><br><br>Continuously displays new log entries as they happen, allowing you to watch connection attempts, syntax errors, and checkpoint messages live.",
        "Topic": "Linux for DBAs",
        "Tags": "dba linux logs tail troubleshooting"
    },
    {
        "Question": "Why should you NEVER run PostgreSQL as the `root` Linux user?",
        "Answer": "<b>ANSWER:</b> Security and protection against accidental operating system destruction.<br><br>Postgres has built-in code functions that read and write files. If run as `root`, a bug or malicious SQL injection could overwrite critical Linux system files (`/etc/passwd`). Postgres refuses to start if invoked as root.",
        "Topic": "Linux for DBAs",
        "Tags": "dba linux security root permissions"
    },

    # --- DATABASE TYPES: WHERE THEY FIT ---
    {
        "Question": "What is the difference between RDBMS (Relational) and NoSQL databases?",
        "Answer": "<b>ANSWER:</b> Structured tables with ACID guarantees vs. Flexible semi-structured documents.<br><br>• <b>RDBMS (Postgres/MySQL):</b> Strict schemas, tables with rows/columns, relational foreign keys, strong ACID consistency. Ideal for finance, orders, and user profiles.<br>• <b>NoSQL (MongoDB/Cassandra):</b> JSON-like documents, dynamic schema, high write throughput at the expense of complex relational joins.",
        "Topic": "Database Landscape",
        "Tags": "dba databases rdbms nosql mongodb"
    },
    {
        "Question": "What is the difference between OLTP and OLAP databases?",
        "Answer": "<b>ANSWER:</b> Fast row transactions vs. Massive analytical aggregations.<br><br>• <b>OLTP (Online Transaction Processing - e.g. Postgres):</b> Thousands of fast, small queries per second (e.g. ATM withdrawal, e-commerce checkout).<br>• <b>OLAP (Online Analytical Processing - e.g. Vertica/Snowflake):</b> Scanning billions of rows across years to compute financial reports and business intelligence trends.",
        "Topic": "Database Landscape",
        "Tags": "dba databases oltp olap architecture"
    },
    {
        "Question": "What is Database Normalization (1NF, 2NF, 3NF) in plain English?",
        "Answer": "<b>ANSWER:</b> Organizing tables to eliminate duplicate redundant data and prevent inconsistencies.<br><br><b>Example:</b> Instead of storing the customer's full address on every single order row, you store the address once in a `Customers` table and reference it with a `customer_id` in `Orders`. If the customer moves, you update 1 row, not 1,000 orders.",
        "Topic": "Database Landscape",
        "Tags": "dba database normalization design"
    }
]

# 3. Combine kept cards + new cards
all_fresher_cards = kept_cards + new_postgres_cards

# Write to decks/dba_fresher_deck.csv
with open('decks/dba_fresher_deck.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    writer.writeheader()
    for card in all_fresher_cards:
        writer.writerow(card)

print(f"Successfully overhauled dba_fresher_deck.csv! Total cards: {len(all_fresher_cards)}")
