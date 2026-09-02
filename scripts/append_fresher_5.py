import csv

last_5 = [
    {
        "Question": "What does `listen_addresses = '*'` do in `postgresql.conf`?",
        "Answer": "<b>ANSWER:</b> Configures PostgreSQL to listen for client connections on ALL available network interfaces.<br><br>By default, Postgres only listens on `localhost` (127.0.0.1), rejecting any remote connection. Setting `*` is mandatory before remote application servers can connect.",
        "Topic": "Postgres Configuration",
        "Tags": "dba postgres listen_addresses networking"
    },
    {
        "Question": "What happens if a database generates WAL faster than `max_wal_size` in `postgresql.conf`?",
        "Answer": "<b>ANSWER:</b> Forces an unplanned, emergency checkpoint ahead of schedule.<br><br><b>The Warning in Logs:</b> <code>LOG: checkpoints are occurring too frequently</code>.<br>Flushing dirty buffers too frequently burns disk I/O and spikes client latency. Sizing `max_wal_size` to 16GB or 64GB provides headroom for heavy write bursts.",
        "Topic": "Postgres Configuration",
        "Tags": "dba postgres max_wal_size checkpoint tuning"
    },
    {
        "Question": "What is `checkpoint_timeout` in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> The maximum elapsed time between automatic checkpoints (default 5 minutes).<br><br>On production servers, setting this to <b>15 to 30 minutes</b> reduces write amplification and smooths disk I/O, at the minor cost of slightly longer crash recovery time.",
        "Topic": "Postgres Configuration",
        "Tags": "dba postgres checkpoint_timeout tuning"
    },
    {
        "Question": "How do you check the total disk space consumed by an entire PostgreSQL database?",
        "Answer": "<b>ANSWER:</b> Use `pg_size_pretty(pg_database_size('dbname'))`.<br><br><b>The SQL:</b><br><code>SELECT pg_database.datname, <br>       pg_size_pretty(pg_database_size(pg_database.datname)) AS db_size <br>FROM pg_database ORDER BY pg_database_size(pg_database.datname) DESC;</code>",
        "Topic": "Routine Maintenance",
        "Tags": "dba postgres storage database_size size"
    },
    {
        "Question": "What is the difference between `pg_tables` and `pg_views` system catalogs?",
        "Answer": "<b>ANSWER:</b> Base table metadata vs. Virtual view definitions.<br><br>• <code>pg_tables</code>: Lists all physical base tables, their schemas, and table owners.<br>• <code>pg_views</code>: Lists all views and stores the exact SQL definition string used to create them.",
        "Topic": "System Catalogs",
        "Tags": "dba postgres catalogs pg_tables pg_views"
    }
]

with open('decks/dba_fresher_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in last_5:
        writer.writerow(card)

print("Added final 5 cards to dba_fresher_deck.csv!")
