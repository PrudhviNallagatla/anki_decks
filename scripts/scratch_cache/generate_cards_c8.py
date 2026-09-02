import csv

cards = [
    {
        "Question": "What is the primary difference between PostgreSQL and EDB Postgres Advanced Server (EPAS)?",
        "Answer": "<b>ANSWER:</b> EDB Postgres Advanced Server (EPAS) adds enterprise-level features on top of open-source PostgreSQL.<br><br><b>Key Additions:</b><br>• <b>Oracle Compatibility:</b> Native support for Oracle PL/SQL, packages, and data types.<br>• <b>Additional Security:</b> SQL injection protection, data redaction, password policies.<br>• <b>DBA Productivity:</b> Wait diagnostics, CPU/IO throttling at the process level.",
        "Topic": "EDB Postgres Essentials",
        "Tags": "edb_postgres intro architecture"
    },
    {
        "Question": "What are the General Database Limits in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> The absolute maximum sizes for database objects.<br><br>• <b>Maximum Database Size:</b> Unlimited<br>• <b>Maximum Table Size:</b> 32 TB<br>• <b>Maximum Row Size:</b> 1.6 TB<br>• <b>Maximum Field Size:</b> 1 GB<br>• <b>Maximum Rows/Indexes per Table:</b> Unlimited",
        "Topic": "EDB Postgres Essentials",
        "Tags": "edb_postgres limits architecture"
    },
    {
        "Question": "Translate these common Industry Database Terms into Postgres Terminology: Table, Row, Column, Data Block.",
        "Answer": "<b>ANSWER:</b> Postgres uses academic terminology from its early development.<br><br>• <b>Table</b> = Relation<br>• <b>Row</b> = Tuple<br>• <b>Column</b> = Attribute<br>• <b>Data Block</b> = Page (when on disk) or Buffer (when in memory)",
        "Topic": "EDB Postgres Essentials",
        "Tags": "edb_postgres terminology basics"
    },
    {
        "Question": "What is the role of the 'Postmaster' process in Postgres?",
        "Answer": "<b>ANSWER:</b> It is the master supervisor process.<br><br><b>Key Roles:</b><br>1. Listens on a single TCP port (default 5432, EDB default 5444) for incoming client connections.<br>2. Spawns a dedicated 'user backend process' for each new client session.<br>3. Starts and restarts utility/background processes if they crash.",
        "Topic": "Postgres Architecture",
        "Tags": "edb_postgres architecture postmaster"
    },
    {
        "Question": "What is a 'User Backend Process' in Postgres?",
        "Answer": "<b>ANSWER:</b> A dedicated process spawned by the Postmaster for a single client connection.<br><br>Because Postgres uses a <b>Process per connection</b> model (not threads), every active connection gets its own dedicated OS process that handles query parsing, planning, and execution, utilizing its own `work_mem`.",
        "Topic": "Postgres Architecture",
        "Tags": "edb_postgres architecture process"
    },
    {
        "Question": "Name the 4 primary Postgres Utility Processes and their functions.",
        "Answer": "<b>ANSWER:</b> The core background workers that keep the database running.<br><br>1. <b>Background Writer (BGWRITER):</b> Slowly writes dirty data blocks to disk to ensure adequate supply of clean buffers.<br>2. <b>WAL Writer:</b> Flushes Write-Ahead Log buffers to disk (crucial for durability).<br>3. <b>Checkpointer:</b> Performs full checkpoints, syncing all dirty buffers to disk.<br>4. <b>Autovacuum:</b> Recovers free space from dead tuples (rows) for reuse.",
        "Topic": "Postgres Architecture",
        "Tags": "edb_postgres architecture utility"
    },
    {
        "Question": "What happens during a COMMIT versus a CHECKPOINT in Postgres?",
        "Answer": "<b>ANSWER:</b> Logging vs Syncing Data.<br><br>• <b>COMMIT:</b> Only the <b>WAL buffers</b> are written to the disk (Write-Ahead Log file) so the transaction is permanent. The actual data pages remain in Shared Buffers (memory).<br>• <b>CHECKPOINT:</b> The <b>Modified Data Pages</b> are physically written from Shared Buffers to the actual database data files on disk.",
        "Topic": "Postgres Architecture",
        "Tags": "edb_postgres architecture checkpoint commit"
    },
    {
        "Question": "How does Postgres structure physical files on disk for Tables and Indexes?",
        "Answer": "<b>ANSWER:</b> File-per-table structure.<br><br>Each relation (table or index) gets one or more files in the data directory. When a file reaches <b>1 GB</b>, a new file segment is created. The filename corresponds to the table's `pg_class.relfilenode` ID.",
        "Topic": "Postgres Architecture",
        "Tags": "edb_postgres architecture storage files"
    },
    {
        "Question": "Explain the default Page Layout structure in Postgres.",
        "Answer": "<b>ANSWER:</b> The anatomy of an 8KB Data Page.<br><br>1. <b>Page Header:</b> 24 bytes of general info and free space pointers.<br>2. <b>Item Pointers (Row/Index pointers):</b> Array of offset/length pairs pointing to tuples. Grows from the <b>front</b>.<br>3. <b>Free Space:</b> Empty space in the middle.<br>4. <b>Tuples (Actual Data):</b> The physical row data. Grows from the <b>rear</b>.",
        "Topic": "Postgres Architecture",
        "Tags": "edb_postgres architecture storage page"
    },
    {
        "Question": "What is the default OS user for installing EDB Postgres Advanced Server on Linux?",
        "Answer": "<b>ANSWER:</b> `enterprisedb`<br><br>Unlike community PostgreSQL which uses the `postgres` user, EDB Advanced Server creates and uses the `enterprisedb` user account. This user must own the data directory.",
        "Topic": "EDB Postgres Installation",
        "Tags": "edb_postgres installation linux"
    }
]

with open('d:/all_codes/anki_cs_it_decks/edb_postgres_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in cards:
        writer.writerow(card)

print(f"Appended {len(cards)} cards from Chunk 08 to the deck.")
