import csv

new_cards = [
    # --- TRANSACTION ISOLATION & SAVEPOINTS (Chunk 13) ---
    {
        "Question": "What are Savepoints in Postgres and how are they used?",
        "Answer": "<b>ANSWER:</b> Bookmarks inside a transaction allowing partial rollbacks.<br><br><b>The SQL:</b><br><code>BEGIN;</code><br><code>INSERT INTO orders VALUES (1);</code><br><code>SAVEPOINT sp1;</code><br><code>INSERT INTO orders VALUES (2); -- crashes!</code><br><code>ROLLBACK TO SAVEPOINT sp1; -- rolls back row 2 only</code><br><code>COMMIT; -- row 1 is safely committed</code>",
        "Topic": "SQL Primer",
        "Tags": "edb_postgres sql transactions savepoint"
    },
    {
        "Question": "Explain the three Transaction Isolation Levels supported by PostgreSQL.",
        "Answer": "<b>ANSWER:</b> Read Committed, Repeatable Read, and Serializable.<br><br>• <b>Read Committed (Default):</b> Each query sees only data committed before that *query* started. Prevents dirty reads.<br>• <b>Repeatable Read:</b> The transaction sees only data committed before the *transaction* started. Prevents non-repeatable reads and phantom reads.<br>• <b>Serializable:</b> Full strict serializability using SSI (Serializable Snapshot Isolation). Prevents serialization anomalies.",
        "Topic": "Architecture & Transactions",
        "Tags": "edb_postgres architecture isolation acid"
    },
    {
        "Question": "Can Dirty Reads occur in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> No, never.<br><br>Even if you explicitly request `SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;`, Postgres silently promotes it to `READ COMMITTED`. Due to MVCC implementation, Postgres fundamentally cannot read uncommitted dirty rows.",
        "Topic": "Architecture & Transactions",
        "Tags": "edb_postgres architecture mvcc dirty_read"
    },
    {
        "Question": "What is the difference between `ON DELETE CASCADE` and `ON DELETE RESTRICT` on Foreign Keys?",
        "Answer": "<b>ANSWER:</b> Automatic child deletion vs blocking parent deletion.<br><br>• <code>CASCADE</code>: Deleting the parent row automatically deletes all matching child rows in related tables.<br>• <code>RESTRICT</code> (or `NO ACTION`): Throws a foreign key violation error and prevents deleting the parent row if child rows exist.",
        "Topic": "SQL Primer",
        "Tags": "edb_postgres sql foreign_keys constraints"
    },
    {
        "Question": "What is `WITH CHECK OPTION` on a View?",
        "Answer": "<b>ANSWER:</b> Prevents inserts or updates that would produce rows not visible in the view.<br><br><b>Example:</b> If a view is defined as <code>WHERE department = 'IT' WITH CHECK OPTION;</code>, an attempt to `INSERT INTO view VALUES ('HR')` will throw an error, preventing data that violates the view definition from being inserted.",
        "Topic": "SQL Primer",
        "Tags": "edb_postgres sql views with_check_option"
    },

    # --- CLI UTILITIES & CLIENT CONFIG (Chunk 09) ---
    {
        "Question": "What is the format and required Linux permissions for the `.pgpass` file?",
        "Answer": "<b>ANSWER:</b> Format: `hostname:port:database:username:password`<br><br><b>Location:</b> `~/.pgpass` (or `%APPDATA%\\postgresql\\pgpass.conf` on Windows).<br><b>Required Permissions:</b> <code>chmod 0600 ~/.pgpass</code>.<br>If permissions allow group or world read access, Postgres client libraries will refuse to read the file for security reasons.",
        "Topic": "User Tools",
        "Tags": "edb_postgres tools pgpass authentication"
    },
    {
        "Question": "What is `pg_service.conf` used for?",
        "Answer": "<b>ANSWER:</b> Named connection profiles for Postgres clients.<br><br>Instead of specifying host, port, user, and dbname in connection strings, you define a named service in `pg_service.conf`:<br><code>[crm_prod]</code><br><code>host=10.0.0.5 port=5444 dbname=crm user=app</code><br>Clients connect simply via <code>psql service=crm_prod</code>.",
        "Topic": "User Tools",
        "Tags": "edb_postgres tools connection pg_service"
    },

    # --- ADVANCED MONITORING & DIAGNOSTICS (Chunks 10, 11) ---
    {
        "Question": "Why should a DBA enable `track_io_timing`?",
        "Answer": "<b>ANSWER:</b> Measures exact disk read and write time in milliseconds.<br><br><b>In postgresql.conf:</b><br><code>track_io_timing = on</code><br><br>Adds I/O timing breakdown to `EXPLAIN (BUFFERS)` and `pg_stat_database`. Essential for determining whether slow queries are bottlenecked by CPU processing or slow storage disk latency.",
        "Topic": "Database Monitoring",
        "Tags": "edb_postgres monitoring io track_io_timing"
    },
    {
        "Question": "What is `track_functions` in `postgresql.conf`?",
        "Answer": "<b>ANSWER:</b> Tracks execution count and time spent in PL/pgSQL stored procedures.<br><br>• <code>none</code> (default): Function calls are not timed.<br>• <code>pl</code>: Tracks execution times for procedural language functions.<br>• <code>all</code>: Tracks PL and SQL functions.<br>Data is visible in the <code>pg_stat_user_functions</code> system view.",
        "Topic": "Database Monitoring",
        "Tags": "edb_postgres monitoring track_functions plpgsql"
    },
    {
        "Question": "What does the `pg_database` system catalog contain?",
        "Answer": "<b>ANSWER:</b> Metadata for all databases in the cluster.<br><br>Key columns include:<br>• <code>datname</code>: Database name.<br>• <code>datdba</code>: Owner role OID.<br>• <code>encoding</code> & <code>datcollate</code>: Character set and collation rules.<br>• <code>datistemplate</code>: Whether it can be used as a template.<br>• <code>datallowconn</code>: If false, connections are rejected.",
        "Topic": "Storage & Catalogs",
        "Tags": "edb_postgres catalogs pg_database metadata"
    },
    {
        "Question": "How do you view the full DDL definition of an existing index in SQL?",
        "Answer": "<b>ANSWER:</b> Query the `indexdef` column in `pg_indexes`.<br><br><b>The SQL:</b><br><code>SELECT indexdef <br>FROM pg_indexes <br>WHERE schemaname = 'public' AND tablename = 'orders';</code><br><br>Returns the complete `CREATE INDEX ...` statement including expression columns and WHERE clauses.",
        "Topic": "Storage & Catalogs",
        "Tags": "edb_postgres catalogs pg_indexes ddl"
    },

    # --- HIGH AVAILABILITY & ARCHITECTURE DEEP DIVE (Chunk 16) ---
    {
        "Question": "What is synchronous replication's `FIRST num (standby_names)` setting?",
        "Answer": "<b>ANSWER:</b> Quorum-based synchronous commit across multiple standby nodes.<br><br><b>Example:</b><br><code>synchronous_standby_names = 'FIRST 2 (node1, node2, node3)'</code><br><br>Postgres waits for the first 2 standbys in priority order to confirm WAL write. Alternatively, `ANY 2 (node1, node2, node3)` uses a quorum model where ANY two confirmations unblock the commit.",
        "Topic": "Replication & HA",
        "Tags": "edb_postgres replication synchronous quorum"
    },
    {
        "Question": "What is the purpose of `wal_keep_size` (formerly `wal_keep_segments`)?",
        "Answer": "<b>ANSWER:</b> Minimum volume of WAL logs retained in `pg_wal` for standbys.<br><br>Prevents the primary from deleting or recycling WAL segments before a standby has streamed them. (Note: Replication Slots are preferred because they dynamically retain exact WAL needed without fixed size caps).",
        "Topic": "Replication & HA",
        "Tags": "edb_postgres replication wal_keep_size wal"
    },
    {
        "Question": "What is Logical Decoding in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Extracting database changes from WAL into a user-friendly format (JSON, SQL, Avro).<br><br>Underlies Logical Replication, CDC (Change Data Capture) systems (like Debezium), and zero-downtime database migrations without relying on physical block replication.",
        "Topic": "Replication & HA",
        "Tags": "edb_postgres replication logical_decoding cdc"
    },
    {
        "Question": "What is `hot_standby_feedback` in `postgresql.conf`?",
        "Answer": "<b>ANSWER:</b> Informs the Primary server about active queries running on a Standby.<br><br>When queries run on a standby, if the Primary runs VACUUM and deletes old tuples that the standby query still needs, the standby query is abruptly canceled with a conflict error. `hot_standby_feedback = on` delays Primary vacuuming until standby queries finish.",
        "Topic": "Replication & HA",
        "Tags": "edb_postgres replication hot_standby_feedback conflicts"
    },

    # --- ADVANCED SQL & DATA TYPES ---
    {
        "Question": "How do you extract a key value from a JSONB column in Postgres SQL?",
        "Answer": "<b>ANSWER:</b> Using the `->` and `->>` operators.<br><br>• <code>data -> 'name'</code>: Returns value as JSON object/type.<br>• <code>data ->> 'name'</code>: Returns value as plain TEXT (essential for WHERE filters and sorting).<br>• <code>data #>> '{address, city}'</code>: Extracts nested path.",
        "Topic": "Advanced SQL",
        "Tags": "edb_postgres sql jsonb operators"
    },
    {
        "Question": "What is the `GENERATE_SERIES()` function in Postgres?",
        "Answer": "<b>ANSWER:</b> A set-returning function that produces an array/table of sequential values.<br><br><b>The SQL:</b><br><code>SELECT generate_series(1, 100); -- numbers 1 to 100</code><br><code>SELECT generate_series('2024-01-01'::date, '2024-01-31'::date, '1 day'::interval);</code><br>Frequently used for generating mock test data, date ranges, and filling reporting gaps.",
        "Topic": "SQL Primer",
        "Tags": "edb_postgres sql generate_series functions"
    },
    {
        "Question": "What is the difference between `EXPLAIN` cost numbers `cost=0.00..45.00`?",
        "Answer": "<b>ANSWER:</b> Startup Cost vs Total Cost.<br><br>• <code>0.00</code> (Startup Cost): Estimated cost to fetch the very first row. (e.g. 0 for Seq Scan, high for Sort or Hash Join).<br>• <code>45.00</code> (Total Cost): Estimated cost to return ALL matching rows from that plan node.",
        "Topic": "SQL Tuning",
        "Tags": "edb_postgres tuning explain cost"
    },
    {
        "Question": "What is a Bitmap Index Scan in an EXPLAIN plan?",
        "Answer": "<b>ANSWER:</b> A two-phase scan: Bitmap Index Scan followed by Bitmap Heap Scan.<br><br>1. <b>Bitmap Index Scan:</b> Scans index and constructs an in-memory bitmap array of target physical block pages.<br>2. <b>Bitmap Heap Scan:</b> Visited disk blocks sequentially using the bitmap, eliminating random page I/O and allowing multiple indexes to be combined via BitmapAnd / BitmapOr.",
        "Topic": "SQL Tuning",
        "Tags": "edb_postgres tuning bitmap explain"
    },
    {
        "Question": "What is `statement_timeout` vs `idle_session_timeout` in Postgres 14+?",
        "Answer": "<b>ANSWER:</b> Active query duration vs completely idle connection duration.<br><br>• <code>statement_timeout</code>: Terminates any single statement that exceeds time limit while executing.<br>• <code>idle_session_timeout</code>: Closes any connection that sits idle (doing nothing) for longer than the threshold, automatically reaping orphaned connection leaks.",
        "Topic": "Configuration",
        "Tags": "edb_postgres config timeouts connections"
    }
]

# Append the new cards
with open('edb_postgres_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in new_cards:
        writer.writerow(card)

print(f"Successfully added {len(new_cards)} more genuine cards to edb_postgres_deck.csv.")
