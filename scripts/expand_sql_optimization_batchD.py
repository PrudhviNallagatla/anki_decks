import csv

batchD = [
    {
        "Question": "What is the difference between `ROLLUP`, `CUBE`, and `GROUPING SETS`?",
        "Answer": "<b>ANSWER:</b> Hierarchical vs. Cartesian vs. Custom subtotal aggregations.<br><br>• <b>`GROUPING SETS`:</b> Computes only the explicitly requested group combinations.<br>• <b>`ROLLUP (year, month, day)`:</b> Hierarchical subtotals (day -> month -> year -> grand total).<br>• <b>`CUBE (region, product)`:</b> Computes ALL possible $2^N$ cross-tabulation subtotal combinations.",
        "Topic": "Analytical SQL",
        "Tags": "sql grouping_sets rollup cube aggregation"
    },
    {
        "Question": "What does the `GROUPING()` function do in `ROLLUP` / `CUBE` queries?",
        "Answer": "<b>ANSWER:</b> Distinguishes between a real `NULL` stored in a table and a generated `NULL` representing a Subtotal.<br><br>Returns `1` if the column is currently aggregated away into a super-aggregate subtotal, and returns `0` if it represents actual row data.",
        "Topic": "Analytical SQL",
        "Tags": "sql grouping rollup cube subtotals"
    },
    {
        "Question": "What is the difference between `ROWS` and `RANGE` in window function frame specifications?",
        "Answer": "<b>ANSWER:</b> Physical row counts vs. Logical value matches.<br><br>• <b>`ROWS BETWEEN 1 PRECEDING AND CURRENT ROW`:</b> Exactly 1 physical row above, regardless of duplicate values.<br>• <b>`RANGE BETWEEN 1 PRECEDING AND CURRENT ROW`:</b> Includes all rows whose values fall within the range, treating duplicate ties identically.",
        "Topic": "Window Functions",
        "Tags": "sql window_functions rows range frame"
    },
    {
        "Question": "Why does `ORDER BY LOWER(email)` fail to use a standard B-Tree index on `email`?",
        "Answer": "<b>ANSWER:</b> Wrapping a column in a function prevents standard B-Tree index traversal.<br><br>The index stores raw `email` strings, not lowercase conversions.<br><b>The Fix:</b> Build an Expression / Functional Index: <code>CREATE INDEX idx_users_lower_email ON users (LOWER(email));</code>.",
        "Topic": "Query Optimization",
        "Tags": "sql indexes functional_index lower sargable"
    },
    {
        "Question": "What are Extended Statistics (`CREATE STATISTICS`) in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Captures multi-column correlations across dependent columns.<br><br><b>The Problem:</b> Postgres assumes `city` and `zip_code` are statistically independent. If filtering `WHERE city = 'Chicago' AND zip_code = '60601'`, the planner underestimates row counts by 100x.<br><b>The Fix:</b> <code>CREATE STATISTICS s_geo ON city, zip_code FROM addresses; ANALYZE addresses;</code>.",
        "Topic": "EXPLAIN Forensics",
        "Tags": "sql explain statistics create_statistics correlation"
    },
    {
        "Question": "What is Partition-Wise Join in PostgreSQL (`enable_partitionwise_join`)?",
        "Answer": "<b>ANSWER:</b> Joining matching partition tables directly instead of joining giant consolidated tables.<br><br>If joining `orders` and `order_items` both partitioned by month, Postgres pairs `orders_jan` with `items_jan`, drastically reducing memory usage and enabling parallel execution per partition.",
        "Topic": "Query Optimization",
        "Tags": "sql partitioning partition_wise_join optimization"
    },
    {
        "Question": "Compare the 3 Core SQL Join Algorithms: Nested Loop, Hash Join, and Merge Join.",
        "Answer": "<b>ANSWER:</b> The Big 3 join algorithms in database engines:<br><br>• <b>Nested Loop:</b> Ideal for small outer table with inner index seek ($O(N \\log M)$).<br>• <b>Hash Join:</b> Hashes smaller table in RAM (`work_mem`) and streams larger table through it ($O(N + M)$). Ideal for large unsorted datasets.<br>• <b>Merge Join:</b> Zips two presorted streams together ($O(N + M)$). Ideal when both inputs are already sorted by an index.",
        "Topic": "EXPLAIN Forensics",
        "Tags": "sql explain joins nested_loop hash_join merge_join"
    },
    {
        "Question": "Why is a Semi-Join (`WHERE EXISTS`) preferred over an `INNER JOIN` when querying 1-to-many relationships?",
        "Answer": "<b>ANSWER:</b> Avoids duplicate row inflation and eliminates the need for expensive `DISTINCT`.<br><br>Joining Customers to Orders (where customers have 50 orders) duplicates each customer 50 times. Using <code>WHERE EXISTS (SELECT 1 FROM orders o WHERE o.cust_id = c.id)</code> returns each matching customer exactly once, stopping evaluation as soon as the first order is found.",
        "Topic": "Query Optimization",
        "Tags": "sql optimization semi_join exists distinct"
    },
    {
        "Question": "Why is an Anti-Join (`WHERE NOT EXISTS`) superior to `LEFT JOIN ... WHERE col IS NULL`?",
        "Answer": "<b>ANSWER:</b> Semantic clarity and immediate short-circuiting.<br><br>`NOT EXISTS` clearly expresses intent to the planner and short-circuits evaluation as soon as a single matching row is encountered, avoiding allocating memory to construct full null-padded outer join rows.",
        "Topic": "Query Optimization",
        "Tags": "sql optimization anti_join not_exists left_join"
    },
    {
        "Question": "What is `GREATEST()` and `LEAST()` across columns in a single row?",
        "Answer": "<b>ANSWER:</b> Computes horizontal min/max across columns.<br><br><b>The SQL:</b><br><code>SELECT id, GREATEST(math_score, science_score, english_score) AS best_subject <br>FROM report_cards;</code><br>Different from aggregate `MAX()` which operates vertically across multiple rows.",
        "Topic": "Analytical SQL",
        "Tags": "sql greatest least columns horizontal"
    },
    {
        "Question": "How do you calculate the difference between two timestamps in days, hours, and minutes in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Use the `AGE()` function or interval subtraction.<br><br>• <code>SELECT AGE(completed_at, started_at) AS elapsed_time FROM jobs;</code><br>• Or extract total seconds: <code>EXTRACT(EPOCH FROM (completed_at - started_at)) / 3600 AS elapsed_hours;</code>.",
        "Topic": "Date Functions",
        "Tags": "sql dates age interval epoch"
    },
    {
        "Question": "How do you safely benchmark queries using EXPLAIN without incurring client network rendering delays?",
        "Answer": "<b>ANSWER:</b> Use `EXPLAIN (ANALYZE, TIMING OFF, BUFFERS)`.<br><br>Disabling microsecond CPU timing (`TIMING OFF`) eliminates measurement overhead on high-frequency queries while retaining exact buffer hits and row counts.",
        "Topic": "EXPLAIN Forensics",
        "Tags": "sql explain analyze timing_off buffers"
    },
    {
        "Question": "What is `pg_hint_plan` in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> An extension that allows overriding the query optimizer with comment hints.<br><br><b>Example:</b><br><code>/*+ HashJoin(a b) SeqScan(a) */ SELECT * FROM a JOIN b ON a.id = b.id;</code><br>Allows developers to force specific join algorithms or index paths similar to Oracle hints.",
        "Topic": "Query Optimization",
        "Tags": "sql postgres pg_hint_plan optimizer hints"
    },
    {
        "Question": "What is the danger of writing `SELECT DISTINCT` as a band-aid fix for duplicate rows?",
        "Answer": "<b>ANSWER:</b> Masks underlying cartesian join bugs and adds massive CPU sort overhead.<br><br>`DISTINCT` forces the database to sort millions of rows or construct an enormous hash table in RAM. Always fix the underlying join logic rather than slapping `DISTINCT` on top.",
        "Topic": "Query Optimization",
        "Tags": "sql optimization distinct anti_pattern"
    },
    {
        "Question": "How do you calculate running totals that reset back to zero every time a specific flag changes?",
        "Answer": "<b>ANSWER:</b> Two-tier window function: build an island group ID, then partition by that group ID.<br><br><b>The SQL:</b><br><code>WITH groups AS ( <br>    SELECT *, SUM(CASE WHEN reset_flag THEN 1 ELSE 0 END) OVER (ORDER BY id) AS grp <br>    FROM transactions <br>) <br>SELECT id, amount, SUM(amount) OVER (PARTITION BY grp ORDER BY id) AS running_total <br>FROM groups;</code>",
        "Topic": "Window Functions",
        "Tags": "sql window_functions running_total reset gaps_and_islands"
    },
    {
        "Question": "What is `CUME_DIST()` and `PERCENT_RANK()` in SQL window analytics?",
        "Answer": "<b>ANSWER:</b> Cumulative distribution vs. Relative percentile ranking.<br><br>• <b>`CUME_DIST()`:</b> Proportion of rows with values $\\le$ current row's value ($0.0$ to $1.0$).<br>• <b>`PERCENT_RANK()`:</b> Relative rank calculation $\\frac{\\text{rank} - 1}{\\text{total rows} - 1}$ (0.0 to 1.0).",
        "Topic": "Window Functions",
        "Tags": "sql window_functions cume_dist percent_rank analytics"
    },
    {
        "Question": "How do you implement a Top-N Per Group query without window functions in legacy databases?",
        "Answer": "<b>ANSWER:</b> Correlated subquery or self-join counting rows with greater values.<br><br><b>The SQL:</b><br><code>SELECT * FROM employees e <br>WHERE ( <br>    SELECT COUNT(*) FROM employees e2 <br>    WHERE e2.department_id = e.department_id AND e2.salary > e.salary <br>) < 3;</code><br>Returns top 3 earners per department.",
        "Topic": "Interview SQL",
        "Tags": "sql interview top_n correlated_subquery legacy"
    },
    {
        "Question": "Why does `WHERE status != 'DELETED'` fail to match rows where `status IS NULL`?",
        "Answer": "<b>ANSWER:</b> Three-Valued Logic: comparing anything to `NULL` yields `UNKNOWN`.<br><br>In SQL, `NULL != 'DELETED'` is neither true nor false—it is `UNKNOWN`. Postgres filters out `UNKNOWN` rows.<br><b>The Fix:</b> <code>WHERE status IS DISTINCT FROM 'DELETED';</code>.",
        "Topic": "Query Optimization",
        "Tags": "sql null three_valued_logic is_distinct_from gotcha"
    },
    {
        "Question": "What does `IS DISTINCT FROM` do in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Null-safe equality comparison operator.<br><br>Treats two `NULL` values as equal to each other, and treats a `NULL` and a non-null value as distinct. <code>a IS DISTINCT FROM b</code> returns `FALSE` if both are NULL, and returns `TRUE` if one is NULL and the other is 'Active'.",
        "Topic": "Query Optimization",
        "Tags": "sql null is_distinct_from comparison safety"
    },
    {
        "Question": "How do you calculate the Median of a column in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Use `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY column)`.<br><br><b>The SQL:</b><br><code>SELECT department_id, <br>       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median_salary <br>FROM employees GROUP BY department_id;</code><br>Interpolates the continuous 50th percentile (exact statistical median).",
        "Topic": "Analytical SQL",
        "Tags": "sql median percentile_cont analytics statistics"
    }
]

with open('decks/sql_tuning_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in batchD:
        writer.writerow(card)

print(f"Batch D complete: appended {len(batchD)} cards.")
