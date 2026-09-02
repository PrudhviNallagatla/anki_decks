import csv

batch4_cards = [
    {
        "Question": "What is `DISTINCT ON (col)` in PostgreSQL and why is it superior to window functions for 'Top 1 per group'?",
        "Answer": "<b>ANSWER:</b> An optimized, single-pass syntax to retrieve the top row for each distinct group.<br><br><b>The SQL:</b><br><code>SELECT DISTINCT ON (user_id) user_id, order_date, total_amount <br>FROM orders <br>ORDER BY user_id, order_date DESC;</code><br>Returns the single most recent order per user in a single index scan without CTEs or `ROW_NUMBER()`.",
        "Topic": "Analytical SQL",
        "Tags": "sql postgres distinct_on top_1 performance"
    },
    {
        "Question": "How do you calculate Day-over-Day growth percentage using `LAG()`?",
        "Answer": "<b>ANSWER:</b> Compare current day revenue with previous day revenue.<br><br><b>The SQL:</b><br><code>SELECT day, revenue, <br>       ROUND((revenue - LAG(revenue) OVER (ORDER BY day)) / <br>             LAG(revenue) OVER (ORDER BY day) * 100, 2) AS dod_growth_pct <br>FROM daily_revenue;</code>",
        "Topic": "Window Functions",
        "Tags": "sql window_functions lag growth analytics"
    },
    {
        "Question": "When should you use a Temporary Table (`CREATE TEMP TABLE`) instead of a CTE?",
        "Answer": "<b>ANSWER:</b> When intermediate data is reused multiple times and needs indexing.<br><br>• <b>CTE:</b> Best for clean single-query logic.<br>• <b>Temp Table:</b> Best when processing multi-million row subsets in complex ETL pipelines where you need to run `CREATE INDEX` or `ANALYZE` on the intermediate data.",
        "Topic": "CTEs & Subqueries",
        "Tags": "sql temp_table cte performance etl"
    },
    {
        "Question": "How do you unnest a JSON or array column while preserving parent row columns?",
        "Answer": "<b>ANSWER:</b> Use a `CROSS JOIN LATERAL` or comma unnest in PostgreSQL.<br><br><b>The SQL:</b><br><code>SELECT u.id, u.name, tag <br>FROM users u, UNNEST(u.tags) AS tag;</code><br>Produces a normalized relational row for every individual tag in each user's array.",
        "Topic": "Analytical SQL",
        "Tags": "sql postgres unnest lateral arrays"
    },
    {
        "Question": "Can PostgreSQL B-Tree indexes index `NULL` values?",
        "Answer": "<b>ANSWER:</b> YES ✅ (Unlike Oracle, where standard B-Trees ignore all-null rows).<br><br>In PostgreSQL, `WHERE col IS NULL` is fully SARGable and can execute as an instant B-Tree index scan.",
        "Topic": "Query Optimization",
        "Tags": "sql postgres indexes null sargable"
    },
    {
        "Question": "What is a Backward Index Scan (`Index Scan Backward`) in an EXPLAIN plan?",
        "Answer": "<b>ANSWER:</b> Traversing a B-Tree index in reverse direction.<br><br>If an index is built in `ASC` order and you query `ORDER BY col DESC`, Postgres simply reads the B-Tree leaf pages in reverse, avoiding an in-memory sort.",
        "Topic": "Query Optimization",
        "Tags": "sql explain index_scan backward order_by"
    },
    {
        "Question": "Why should `random_page_cost` be reduced from 4.0 to 1.1 on SSD / NVMe drives in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> The default `4.0` was designed for spinning magnetic hard disks where random seeks were 4x slower.<br><br>On fast NVMe/SSDs, random reads have near-zero seek penalty. Setting `random_page_cost = 1.1` convinces the query planner to choose fast Index Scans over slow Sequential Scans.",
        "Topic": "Query Optimization",
        "Tags": "sql postgres tuning random_page_cost ssd"
    },
    {
        "Question": "What parameter controls temporary disk spills during sorting and hash joins?",
        "Answer": "<b>ANSWER:</b> `work_mem`<br><br>You can safely increase it temporarily for a single heavy analytical query:<br><code>SET LOCAL work_mem = '512MB';</code><br><code>SELECT customer_id, SUM(amount) FROM orders GROUP BY 1;</code><br>Eliminates `external merge Disk` spills.",
        "Topic": "Query Optimization",
        "Tags": "sql tuning work_mem sort spill"
    },
    {
        "Question": "How do you log queries that spill temporary files to disk in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Set `log_temp_files = 0` in `postgresql.conf`.<br><br>Postgres writes a warning to the server log whenever a query spills sorting or hash operations to disk, recording the exact query and size of temporary disk files created.",
        "Topic": "Query Optimization",
        "Tags": "sql postgres tuning log_temp_files monitoring"
    },
    {
        "Question": "How do you count distinct pairs of columns in SQL?",
        "Answer": "<b>ANSWER:</b> `COUNT(DISTINCT (col1, col2))` or using a subquery.<br><br><b>PostgreSQL Syntax:</b><br><code>SELECT COUNT(DISTINCT (user_id, product_id)) FROM user_events;</code><br><b>Standard SQL:</b><br><code>SELECT COUNT(*) FROM (SELECT DISTINCT user_id, product_id FROM user_events) sub;</code>",
        "Topic": "Analytical SQL",
        "Tags": "sql count distinct combinations"
    },
    {
        "Question": "What is the `citext` extension in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Case-insensitive text data type.<br><br>Automatically treats `'Alice'` and `'alice'` as identical in `WHERE` and `UNIQUE` constraints without requiring `LOWER()` function wrappers, making all searches natively SARGable on standard B-Tree indexes.",
        "Topic": "JSONB & Modern Types",
        "Tags": "sql postgres citext case_insensitive types"
    },
    {
        "Question": "What does the `OVERLAPS` operator do in SQL?",
        "Answer": "<b>ANSWER:</b> Evaluates whether two time intervals overlap.<br><br><b>The SQL:</b><br><code>SELECT (DATE '2024-01-01', DATE '2024-01-15') OVERLAPS <br>       (DATE '2024-01-10', DATE '2024-01-20');</code><br>Returns `TRUE` in microseconds without writing complex multi-part `AND/OR` date comparison logic.",
        "Topic": "Analytical SQL",
        "Tags": "sql dates overlaps intervals"
    },
    {
        "Question": "What is the difference between `NOW()` and `CLOCK_TIMESTAMP()` in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Transaction start time vs. Real-time wall clock.<br><br>• <b>`NOW()` / `CURRENT_TIMESTAMP`:</b> Returns the timestamp when the *transaction* began. Remains identical across all statements in the transaction.<br>• <b>`CLOCK_TIMESTAMP()`:</b> Returns the actual current wall-clock time as the statement executes. Changes between rows.",
        "Topic": "SQL Gotchas",
        "Tags": "sql postgres dates now clock_timestamp"
    },
    {
        "Question": "What is `EXPLAIN (BUFFERS, ANALYZE)` and why is it the gold standard of query tuning?",
        "Answer": "<b>ANSWER:</b> Displays actual execution time AND memory buffer cache page hits vs disk reads.<br><br>Tells you exactly how many 8KB blocks were read from RAM (`Shared Hit`) vs slow disk (`Shared Read`), and if any dirty blocks were written, exposing the true I/O bottleneck.",
        "Topic": "Query Optimization",
        "Tags": "sql explain buffers analyze tuning"
    },
    {
        "Question": "How do you clean an EXPLAIN plan for sharing without cluttered cost numbers?",
        "Answer": "<b>ANSWER:</b> Use `EXPLAIN (COSTS OFF)`.<br><br><b>Syntax:</b><br><code>EXPLAIN (COSTS OFF) SELECT * FROM users WHERE id = 5;</code><br>Produces a clean, human-readable outline of the execution tree (Index Scan on users_pkey).",
        "Topic": "Query Optimization",
        "Tags": "sql explain costs_off documentation"
    },
    {
        "Question": "What is the 'Parameter Sniffing / Prepared Statement' plan caching problem in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Postgres generating a generic execution plan after 5 executions of a prepared statement.<br><br>If an input parameter is skewed (e.g. status 'PENDING' has 5 rows, but 'COMPLETED' has 10 million rows), the generic plan may pick a Seq Scan for 'PENDING', destroying performance for small queries.",
        "Topic": "Query Optimization",
        "Tags": "sql postgres prepared_statements parameter_sniffing"
    },
    {
        "Question": "What is `GREATEST()` and `LEAST()` in SQL?",
        "Answer": "<b>ANSWER:</b> Row-level comparison functions that return the maximum or minimum value among a list of expressions.<br><br><b>The SQL:</b><br><code>SELECT student_id, GREATEST(math_score, english_score, science_score) AS best_score <br>FROM report_cards;</code><br>(Distinct from columnar aggregate `MAX()` / `MIN()`).",
        "Topic": "SQL Gotchas",
        "Tags": "sql functions greatest least row_level"
    },
    {
        "Question": "How do you calculate the 90th percentile of response times in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Use `PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY latency)`.<br><br><b>The SQL:</b><br><code>SELECT endpoint, <br>       PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY response_ms) AS p90_latency <br>FROM api_logs GROUP BY endpoint;</code>",
        "Topic": "Analytical SQL",
        "Tags": "sql analytics percentiles p90 percentile_cont"
    },
    {
        "Question": "What is the difference between `ARRAY_AGG()` and `STRING_AGG()` in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Native SQL array vs. Formatted text string.<br><br>• <b>`ARRAY_AGG(id)`:</b> Collects values into a native PostgreSQL array (`{1, 2, 3}`), which can be queried using array subscripting and operators.<br>• <b>`STRING_AGG(name, ', ')`:</b> Produces a single formatted `TEXT` string (`'Alice, Bob, Charlie'`).",
        "Topic": "Analytical SQL",
        "Tags": "sql postgres array_agg string_agg arrays"
    },
    {
        "Question": "Why should you avoid `ORDER BY random() LIMIT 1` on large tables?",
        "Answer": "<b>ANSWER:</b> It forces a Full Table Scan and in-memory sort of the ENTIRE table.<br><br>On 10 million rows, the database must generate a random number for all 10 million rows and sort them just to return 1 row. Use index-based sampling or `TABLESAMPLE BERNOULLI / SYSTEM` instead.",
        "Topic": "Query Optimization",
        "Tags": "sql optimization random tablesample performance"
    },
    {
        "Question": "What does `TABLESAMPLE SYSTEM (1)` do in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Fast physical 1% block sampling of a table.<br><br><b>The SQL:</b><br><code>SELECT * FROM large_transactions TABLESAMPLE SYSTEM (1);</code><br>Directly reads 1% of random 8KB disk pages off disk in milliseconds without scanning the rest of the table.",
        "Topic": "Query Optimization",
        "Tags": "sql postgres tablesample sampling"
    },
    {
        "Question": "What is the difference between `SIMILAR TO` and POSIX Regex `~` in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> SQL standard hybrid syntax vs. Powerful POSIX regular expressions.<br><br>• <b>`SIMILAR TO`:</b> Blends SQL wildcards (`%`, `_`) with regex syntax. Rarely used and difficult to index.<br>• <b>`~` (POSIX Regex):</b> Standard regex matching (e.g. `col ~ '^[A-Z][0-9]{3}'`). Can be accelerated with `pg_trgm` GIN indexes.",
        "Topic": "SQL Gotchas",
        "Tags": "sql postgres regex similar_to posix"
    },
    {
        "Question": "How do you extract the Epoch (Unix timestamp in seconds) from a timestamp in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> `EXTRACT(EPOCH FROM timestamp)`<br><br><b>The SQL:</b><br><code>SELECT EXTRACT(EPOCH FROM NOW())::bigint AS current_epoch_seconds;</code><br>And reverse it using: <code>SELECT TO_TIMESTAMP(1700000000);</code>.",
        "Topic": "Analytical SQL",
        "Tags": "sql postgres dates epoch timestamps"
    },
    {
        "Question": "What is the difference between `DELETE` and `TRUNCATE` regarding transaction rollbacks in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> BOTH can be rolled back in PostgreSQL!<br><br>Unlike MySQL or Oracle where `TRUNCATE` commits immediately, PostgreSQL supports transactional DDL. If you run `TRUNCATE my_table;` inside a `BEGIN ... ROLLBACK;` block, all rows are safely restored!",
        "Topic": "SQL Gotchas",
        "Tags": "sql postgres truncate rollback transactions"
    },
    {
        "Question": "What does `EXPLAIN (ANALYZE, TIMING OFF)` do in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Runs the query to collect actual row counts and buffer usage without timing overhead.<br><br>Collecting microsecond CPU timestamps on every node can introduce 10–20% overhead on high-throughput systems. `TIMING OFF` minimizes measurement bias while preserving actual row counts and I/O buffer stats.",
        "Topic": "Query Optimization",
        "Tags": "sql explain timing_off profiling tuning"
    },
    {
        "Question": "What is a 'Correlated Lateral Subquery'?",
        "Answer": "<b>ANSWER:</b> A lateral join where the subquery evaluates dynamically based on values from the current outer row.<br><br>Combines the power of a correlated subquery with the flexibility of returning multiple columns and rows in the `FROM` clause.",
        "Topic": "Joins & Set Operations",
        "Tags": "sql joins lateral subqueries correlated"
    },
    {
        "Question": "What is the difference between `ANY` and `ALL` in SQL subqueries?",
        "Answer": "<b>ANSWER:</b> Match at least one vs. Match every single one.<br><br>• <b>`salary > ANY (SELECT salary FROM engineers)`:</b> True if your salary is greater than the *lowest* engineer salary.<br>• <b>`salary > ALL (SELECT salary FROM engineers)`:</b> True only if your salary is greater than the *highest* engineer salary.",
        "Topic": "SQL Gotchas",
        "Tags": "sql subqueries any all operators"
    },
    {
        "Question": "How do you write a query to detect duplicate rows in a table?",
        "Answer": "<b>ANSWER:</b> Use `GROUP BY` with `HAVING COUNT(*) > 1`.<br><br><b>The SQL:</b><br><code>SELECT email, COUNT(*) <br>FROM users <br>GROUP BY email <br>HAVING COUNT(*) > 1;</code>",
        "Topic": "Analytical SQL",
        "Tags": "sql duplicates groupby having"
    }
]

with open('decks/sql_tuning_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in batch4_cards:
        writer.writerow(card)

print(f"Batch 4 complete: appended {len(batch4_cards)} cards.")
