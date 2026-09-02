import csv

extra_cards = [
    {
        "Question": "What are the 5 most essential `psql` meta-commands every beginner must know?",
        "Answer": "<b>ANSWER:</b> Navigation and inspection commands in `psql`:<br><br>• <code>\\c dbname</code>: Connect / switch to another database.<br>• <code>\\dt</code>: List all tables in current schema.<br>• <code>\\d tablename</code>: Describe table structure, columns, data types, and indexes.<br>• <code>\\du</code>: List all database users and roles.<br>• <code>\\l</code>: List all databases on the server.",
        "Topic": "psql Client",
        "Tags": "dba postgres psql meta_commands"
    },
    {
        "Question": "What is a Schema in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> A logical namespace within a database containing tables, views, and functions.<br><br><b>The Folder Analogy:</b><br>A database is like a hard drive; schemas are like folders on that drive (e.g. `public`, `sales`, `hr`). Tables with the same name can exist in different schemas (`sales.orders` vs `archive.orders`).",
        "Topic": "Postgres Architecture",
        "Tags": "dba postgres schemas namespaces"
    },
    {
        "Question": "What is the `search_path` in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> The list of schemas Postgres searches when you query a table without specifying a schema name.<br><br><b>Default:</b> `\"$user\", public`<br>If you type `SELECT * FROM orders;`, Postgres looks in the user's schema first, then in `public`. Check with: <code>SHOW search_path;</code>.",
        "Topic": "Postgres Architecture",
        "Tags": "dba postgres search_path schemas"
    },
    {
        "Question": "What is the difference between `SERIAL` and `IDENTITY` columns in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Legacy Postgres syntax vs. Modern SQL Standard syntax.<br><br>• <b>`SERIAL`:</b> Creates an implicit sequence behind the scenes. Does not prevent users from accidentally inserting manual duplicate IDs.<br>• <b>`GENERATED ALWAYS AS IDENTITY`:</b> SQL standard. Strictly enforced by Postgres, preventing accidental manual overrides.",
        "Topic": "SQL & DDL",
        "Tags": "dba postgres serial identity sequences"
    },
    {
        "Question": "What is the `~/.pgpass` file on Linux?",
        "Answer": "<b>ANSWER:</b> A password file allowing password-free automated script logins to PostgreSQL.<br><br><b>Format:</b><br><code>hostname:port:database:username:password</code><br><b>Security Rule:</b> Linux file permissions MUST be set to strict `0600` (`chmod 0600 ~/.pgpass`), or Postgres will ignore the file.",
        "Topic": "Postgres Security",
        "Tags": "dba postgres security pgpass linux"
    },
    {
        "Question": "What is `pg_stat_activity` and why is it a DBA's most queried system view?",
        "Answer": "<b>ANSWER:</b> The real-time view of every active client connection and running query.<br><br><b>The Inspection SQL:</b><br><code>SELECT pid, usename, client_addr, state, query <br>FROM pg_stat_activity;</code><br>Instantly reveals who is connected, what queries are actively executing, and which sessions are idle or hung.",
        "Topic": "Routine Maintenance",
        "Tags": "dba postgres pg_stat_activity monitoring"
    },
    {
        "Question": "How do you safely terminate a long-running or hung query in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Use `pg_cancel_backend(pid)` or `pg_terminate_backend(pid)`.<br><br>• <b>`SELECT pg_cancel_backend(12345);`:</b> Sends SIGINT. Cancels only the running query while keeping the user connected.<br>• <b>`SELECT pg_terminate_backend(12345);`:</b> Sends SIGTERM. Completely severs the entire client connection.",
        "Topic": "Routine Maintenance",
        "Tags": "dba postgres cancel terminate sessions"
    },
    {
        "Question": "What is `max_connections` in `postgresql.conf` and why is setting it too high dangerous?",
        "Answer": "<b>ANSWER:</b> The maximum number of concurrent client connections allowed by the server.<br><br><b>The Danger:</b> Each connection requires dedicated memory and internal lock structures. Setting `max_connections = 5000` causes CPU starvation on internal lock tables (`ProcArrayLock`) and leads to Out-Of-Memory crashes. Recommended max is typically 100–300, using PgBouncer for more.",
        "Topic": "Postgres Configuration",
        "Tags": "dba postgres max_connections tuning"
    },
    {
        "Question": "What is the recommended rule of thumb for setting `shared_buffers` in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> 25% of total system RAM on dedicated database servers.<br><br><b>Example:</b> If a server has 32GB RAM, set `shared_buffers = 8GB`.<br>Setting it higher than 40% usually degrades performance because it duplicates caching efforts with the Linux OS file cache (double caching).",
        "Topic": "Postgres Configuration",
        "Tags": "dba postgres shared_buffers memory tuning"
    },
    {
        "Question": "What is `work_mem` and what is the 'work_mem multiplier trap'?",
        "Answer": "<b>ANSWER:</b> The memory allocated for sorting, hash joins, and aggregations before spilling to disk.<br><br><b>The Multiplier Trap:</b> `work_mem` is NOT per-connection or per-query—it is <b>per-operation</b>.<br>A single complex query with 4 sorts and 2 hash joins can consume `6 * work_mem`. If 50 concurrent users run it, memory usage explodes: <code>50 users * 6 operations * 64MB = 19.2 GB RAM</code>!",
        "Topic": "Postgres Configuration",
        "Tags": "dba postgres work_mem memory trap"
    },
    {
        "Question": "What is `maintenance_work_mem` in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Dedicated memory used exclusively for maintenance operations: `VACUUM`, `CREATE INDEX`, and `ALTER TABLE ADD FOREIGN KEY`.<br><br>Since only one maintenance task runs at a time per session, this can safely be set much higher than `work_mem` (e.g. 512MB to 2GB) to speed up index builds.",
        "Topic": "Postgres Configuration",
        "Tags": "dba postgres maintenance_work_mem vacuum"
    },
    {
        "Question": "What does `archive_mode = on` and `archive_command` do in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Automatically copies completed 16MB WAL log segments to a safe backup repository.<br><br><b>Example:</b><br><code>archive_command = 'cp %p /mnt/wal_archive/%f'</code><br>This continuous stream of archived WAL files is what makes Point-In-Time Recovery (PITR) possible.",
        "Topic": "Backup & Recovery",
        "Tags": "dba postgres wal archiving pitr"
    },
    {
        "Question": "What is the `standby.signal` file in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> A marker file placed in the `$PGDATA` directory that commands PostgreSQL to start in Standby (read-only replica) mode.<br><br>When present on startup, Postgres connects to the primary server and begins continuously applying WAL streams rather than accepting write transactions.",
        "Topic": "Replication & HA",
        "Tags": "dba postgres replication standby_signal"
    },
    {
        "Question": "What is `primary_conninfo` in `postgresql.conf`?",
        "Answer": "<b>ANSWER:</b> The connection string a Standby replica uses to connect to its Primary upstream server.<br><br><b>Example:</b><br><code>primary_conninfo = 'host=192.168.1.50 port=5432 user=replicator password=secret'</code>",
        "Topic": "Replication & HA",
        "Tags": "dba postgres replication primary_conninfo"
    },
    {
        "Question": "What is the `pg_isready` command-line utility?",
        "Answer": "<b>ANSWER:</b> A lightweight tool that checks the connection status of a PostgreSQL server.<br><br><b>Usage:</b><br><code>pg_isready -h localhost -p 5432</code><br>Returns exit code 0 if accepting connections. Commonly used in monitoring scripts, Kubernetes health probes, and automated failover watchdogs.",
        "Topic": "Postgres Tools",
        "Tags": "dba postgres pg_isready monitoring"
    },
    {
        "Question": "What are the core commands in `pg_ctl`?",
        "Answer": "<b>ANSWER:</b> The low-level service control utility for PostgreSQL.<br><br>• <code>pg_ctl start -D /data/dir</code>: Start the database.<br>• <code>pg_ctl stop -m fast</code>: Fast graceful shutdown.<br>• <code>pg_ctl reload</code>: Reload configuration files (`postgresql.conf`, `pg_hba.conf`) without restarting or disconnecting users.<br>• <code>pg_ctl status</code>: Check if server is running.",
        "Topic": "Postgres Tools",
        "Tags": "dba postgres pg_ctl administration"
    },
    {
        "Question": "What are the `createdb` and `dropdb` command-line tools?",
        "Answer": "<b>ANSWER:</b> Convenient OS shell wrappers around SQL `CREATE DATABASE` and `DROP DATABASE`.<br><br><b>Usage:</b><br><code>createdb -U postgres my_new_db</code><br><code>dropdb -U postgres my_old_db</code><br>Allows creating or dropping databases directly from bash scripts without entering `psql`.",
        "Topic": "Postgres Tools",
        "Tags": "dba postgres createdb dropdb cli"
    },
    {
        "Question": "What is the difference between `pg_dump` plain text format (`-F p`) and custom directory/tar format (`-F c`)?",
        "Answer": "<b>ANSWER:</b> Plain SQL script vs. Compressed flexible binary archive.<br><br>• <b>`-F p` (Plain):</b> Creates a regular `.sql` script. Restored using `psql -f backup.sql`.<br>• <b>`-F c` (Custom):</b> Creates a compressed binary archive. Restored using `pg_restore`. Allows parallel multi-threaded restores (`-j 4`) and selective table restoration.",
        "Topic": "Backup & Recovery",
        "Tags": "dba postgres pg_dump pg_restore formats"
    },
    {
        "Question": "What is the difference between a Primary Key and a Unique constraint?",
        "Answer": "<b>ANSWER:</b> NULL allowance and identity significance.<br><br>• <b>Primary Key:</b> Uniquely identifies each row; strictly forbids `NULL` values. A table can have ONLY ONE primary key.<br>• <b>Unique Constraint:</b> Enforces uniqueness, but permits `NULL` values (in standard SQL, multiple rows can contain NULL). A table can have multiple unique constraints.",
        "Topic": "SQL & DDL",
        "Tags": "dba sql constraints primary_key unique"
    },
    {
        "Question": "What does `ON DELETE CASCADE` do in a Foreign Key constraint?",
        "Answer": "<b>ANSWER:</b> Automatically deletes child records when the referenced parent record is deleted.<br><br><b>Example:</b> If `Orders` has `ON DELETE CASCADE` referencing `Customers`, deleting Customer #5 will automatically delete all of Customer #5's orders from the database.",
        "Topic": "SQL & DDL",
        "Tags": "dba sql constraints cascade foreign_key"
    },
    {
        "Question": "What is the critical difference between `TRUNCATE` and `DELETE` in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Instant physical table reset vs. Row-by-row deletion.<br><br>• <b>`DELETE FROM table;`:</b> Scans every row, writes a WAL deletion record for each, and generates dead tuples. Slow on 10 million rows.<br>• <b>`TRUNCATE table;`:</b> Instant DDL command. Drops the entire physical disk file and creates a new empty file in milliseconds. Reclaims disk space immediately.",
        "Topic": "SQL & DDL",
        "Tags": "dba postgres truncate delete ddl dml"
    },
    {
        "Question": "What is the difference between DDL, DML, DCL, and TCL in SQL?",
        "Answer": "<b>ANSWER:</b> The 4 functional categories of SQL statements:<br><br>• <b>DDL (Data Definition):</b> `CREATE`, `ALTER`, `DROP`, `TRUNCATE` (schema structures).<br>• <b>DML (Data Manipulation):</b> `SELECT`, `INSERT`, `UPDATE`, `DELETE` (table rows).<br>• <b>DCL (Data Control):</b> `GRANT`, `REVOKE` (security permissions).<br>• <b>TCL (Transaction Control):</b> `BEGIN`, `COMMIT`, `ROLLBACK` (transaction boundaries).",
        "Topic": "SQL & DDL",
        "Tags": "dba sql categories ddl dml dcl tcl"
    },
    {
        "Question": "What is Database Connection Leaking and how does it affect a database?",
        "Answer": "<b>ANSWER:</b> An application bug where backend code opens database connections but forgets to close them.<br><br>Over time, all available connection slots (`max_connections`) are consumed by idle connections. Eventually, legitimate users receive the fatal error: <code>FATAL: sorry, too many clients already</code>.",
        "Topic": "Routine Maintenance",
        "Tags": "dba postgres connection_leak max_connections"
    },
    {
        "Question": "What does `SHOW config_file;` reveal in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> The exact filesystem path to the active `postgresql.conf` configuration file.<br><br><b>The SQL:</b><br><code>SHOW config_file;</code><br>Invaluable for DBAs when managing multiple Postgres clusters on the same Linux server to ensure they edit the correct file.",
        "Topic": "Postgres Configuration",
        "Tags": "dba postgres configuration postgresql_conf"
    }
]

with open('decks/dba_fresher_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in extra_cards:
        writer.writerow(card)

print(f"Successfully added {len(extra_cards)} cards to dba_fresher_deck.csv!")
