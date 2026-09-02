import csv
import os

sql_cards = [
    # --- MODULE 1: WINDOW FUNCTIONS & ANALYTICAL SQL ---
    {
        "Question": "What is the fundamental difference between a Window Function and a `GROUP BY` aggregation?",
        "Answer": "<b>ANSWER:</b> Preserving individual rows vs. collapsing rows.<br><br>• <b>`GROUP BY`:</b> Collapses 100 rows into a single summary row per group.<br>• <b>Window Function:</b> Computes an aggregate (like a running total or rank) across a group of rows while <b>keeping every individual row distinct</b> in the output.",
        "Topic": "Window Functions",
        "Tags": "sql window_functions groupby analytics"
    },
    {
        "Question": "What is the difference between `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()`?",
        "Answer": "<b>ANSWER:</b> How they handle ties (identical values).<br><br><b>Example with scores [100, 100, 90]:</b><br>• <b>`ROW_NUMBER()`:</b> Sequential without ties -> `1, 2, 3`<br>• <b>`RANK()`:</b> Assigns same rank to ties, leaves gaps -> `1, 1, 3` (skips 2)<br>• <b>`DENSE_RANK()`:</b> Assigns same rank to ties, NO gaps -> `1, 1, 2`",
        "Topic": "Window Functions",
        "Tags": "sql window_functions row_number rank dense_rank"
    },
    {
        "Question": "How do `LEAD()` and `LAG()` work, and how do you handle missing edge values?",
        "Answer": "<b>ANSWER:</b> Accessing subsequent or preceding rows without a self-join.<br><br><b>Syntax:</b><br><code>LAG(salary, 1, 0) OVER (ORDER BY hire_date)</code><br>• 1st param: Column to inspect.<br>• 2nd param: Offset (1 = previous row).<br>• 3rd param: Default fallback if no row exists (avoids `NULL` for the first row).",
        "Topic": "Window Functions",
        "Tags": "sql window_functions lead lag analytics"
    },
    {
        "Question": "How do you calculate a Running Cumulative Total in SQL?",
        "Answer": "<b>ANSWER:</b> Use `SUM(...) OVER (ORDER BY date)`.<br><br><b>The SQL:</b><br><code>SELECT order_date, amount, <br>       SUM(amount) OVER (ORDER BY order_date) AS running_total <br>FROM orders;</code><br>Adding `ORDER BY` inside `OVER()` implicitly sets the window frame from the start of the table to the current row.",
        "Topic": "Window Functions",
        "Tags": "sql window_functions running_total sum"
    },
    {
        "Question": "What is the difference between `ROWS BETWEEN` and `RANGE BETWEEN` in window frames?",
        "Answer": "<b>ANSWER:</b> Physical row counts vs. Logical value ranges.<br><br>• <b>`ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING`:</b> Exactly 1 physical row before and 1 physical row after.<br>• <b>`RANGE BETWEEN`:</b> Evaluates values of the `ORDER BY` column (includes all rows with identical tie values in the calculation).",
        "Topic": "Window Functions",
        "Tags": "sql window_functions window_frames rows range"
    },
    {
        "Question": "How do you calculate a 3-Day Moving Average in SQL?",
        "Answer": "<b>ANSWER:</b> Use `AVG()` with an explicit `ROWS` frame.<br><br><b>The SQL:</b><br><code>SELECT sale_date, amount, <br>       AVG(amount) OVER ( <br>           ORDER BY sale_date <br>           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW <br>       ) AS moving_avg_3day <br>FROM daily_sales;</code>",
        "Topic": "Window Functions",
        "Tags": "sql window_functions moving_average frame"
    },
    {
        "Question": "Why can you NOT use a Window Function directly inside a `WHERE` or `HAVING` clause?",
        "Answer": "<b>ANSWER:</b> Logical Query Processing Order.<br><br>Window functions are evaluated in Step 5 (after `FROM`, `WHERE`, `GROUP BY`, and `HAVING`). The `WHERE` clause filters rows BEFORE window functions even exist. To filter by a window result (e.g. `WHERE rank = 1`), you must wrap it in a <b>CTE or Subquery</b>.",
        "Topic": "Window Functions",
        "Tags": "sql window_functions execution_order where gotcha"
    },
    {
        "Question": "What does `NTILE(4)` do in SQL?",
        "Answer": "<b>ANSWER:</b> Divides an ordered dataset into 4 roughly equal quartiles (buckets 1, 2, 3, 4).<br><br><b>Example:</b><br><code>SELECT employee_id, salary, NTILE(4) OVER (ORDER BY salary) AS quartile <br>FROM employees;</code><br>Identifies top 25% earners (quartile 4) vs lowest 25% (quartile 1).",
        "Topic": "Window Functions",
        "Tags": "sql window_functions ntile percentiles"
    },
    {
        "Question": "Why does `LAST_VALUE(col) OVER (ORDER BY date)` often return the current row instead of the true last row?",
        "Answer": "<b>ANSWER:</b> The default window frame stops at `CURRENT ROW`.<br><br>By default, `ORDER BY` creates a frame of <code>RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW</code>. The 'last value' up to the current row IS the current row! To get the true last value, specify: <code>ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING</code>.",
        "Topic": "Window Functions",
        "Tags": "sql window_functions last_value gotcha"
    },
    {
        "Question": "How do you find the Top 3 earners in EACH department using SQL?",
        "Answer": "<b>ANSWER:</b> Use `DENSE_RANK()` inside a CTE partitioned by department.<br><br><b>The SQL:</b><br><code>WITH ranked_emp AS ( <br>    SELECT name, dept_id, salary, <br>           DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) as rnk <br>    FROM employees <br>) <br>SELECT * FROM ranked_emp WHERE rnk <= 3;</code>",
        "Topic": "Window Functions",
        "Tags": "sql window_functions dense_rank top_n"
    },

    # --- MODULE 2: COMMON TABLE EXPRESSIONS (CTEs) & RECURSION ---
    {
        "Question": "What is a Common Table Expression (CTE) and why use it over nested subqueries?",
        "Answer": "<b>ANSWER:</b> A named, temporary result set defined with `WITH ... AS`.<br><br><b>Why use CTEs:</b><br>1. <b>Readability:</b> Replaces unreadable 5-level deep nested parentheses with top-to-bottom sequential logic.<br>2. <b>Reusability:</b> Can reference the same CTE multiple times within the query without repeating code.",
        "Topic": "CTEs & Subqueries",
        "Tags": "sql cte subqueries with syntax"
    },
    {
        "Question": "What are the two parts of a Recursive CTE?",
        "Answer": "<b>ANSWER:</b> The Anchor Member and the Recursive Member joined by `UNION ALL`.<br><br>1. <b>Anchor Member:</b> The base query that seeds the initial rows (e.g. finding the CEO where `manager_id IS NULL`).<br>2. <b>Recursive Member:</b> The query that joins to the CTE itself to fetch child rows until a termination condition is met.",
        "Topic": "CTEs & Subqueries",
        "Tags": "sql cte recursive anchor union_all"
    },
    {
        "Question": "Write a Recursive CTE to generate numbers from 1 to 10 in PostgreSQL.",
        "Answer": "<b>ANSWER:</b><br><code>WITH RECURSIVE nums AS ( <br>    SELECT 1 AS n -- Anchor <br>    UNION ALL <br>    SELECT n + 1 FROM nums WHERE n < 10 -- Recursive <br>) <br>SELECT * FROM nums;</code><br>Commonly used by data engineers to generate date ranges to fill missing calendar days.",
        "Topic": "CTEs & Subqueries",
        "Tags": "sql cte recursive sequence"
    },
    {
        "Question": "What is a Correlated Subquery and why is it often a performance killer?",
        "Answer": "<b>ANSWER:</b> An inner subquery that references a column from the outer query.<br><br><b>The Performance Trap:</b><br>The inner query cannot execute once. The database must re-execute the inner subquery <b>for every single row</b> evaluated in the outer query ($O(N \\times M)$ loop). Rewrite as a `LEFT JOIN` or Window Function whenever possible.",
        "Topic": "CTEs & Subqueries",
        "Tags": "sql subqueries correlated performance"
    },
    {
        "Question": "What is the difference between Materialized and Inlined CTEs in PostgreSQL 12+?",
        "Answer": "<b>ANSWER:</b> Optimization boundary vs. Planner inlining.<br><br>• <b>Inlined (Default):</b> Postgres folds the CTE into the main query, allowing the optimizer to push down predicates and indexes.<br>• <b>`AS MATERIALIZED`:</b> Forces Postgres to execute the CTE once into a temporary buffer, acting as an intentional optimization fence.",
        "Topic": "CTEs & Subqueries",
        "Tags": "sql cte materialized postgres optimization"
    },

    # --- MODULE 3: ADVANCED JOINS, SET OPERATIONS & ANTI-PATTERNS ---
    {
        "Question": "Explain the difference between `INNER JOIN`, `LEFT JOIN`, `FULL OUTER JOIN`, and `CROSS JOIN`.",
        "Answer": "<b>ANSWER:</b> Row retention behavior:<br><br>• <b>`INNER JOIN`:</b> Returns rows ONLY where the join key matches in BOTH tables.<br>• <b>`LEFT JOIN`:</b> Returns ALL rows from the left table; unmatched right table columns become `NULL`.<br>• <b>`FULL OUTER JOIN`:</b> Returns all rows from BOTH tables, filling `NULL` on either side where unmatched.<br>• <b>`CROSS JOIN`:</b> Cartesian product—joins every left row with every right row ($N \\times M$ rows).",
        "Topic": "Joins & Set Operations",
        "Tags": "sql joins inner left outer cross"
    },
    {
        "Question": "What is the catastrophic '`NOT IN` with `NULL`' trap?",
        "Answer": "<b>ANSWER:</b> If the subquery contains even ONE `NULL` value, `NOT IN` returns ZERO rows for the entire query!<br><br><b>Why:</b> In SQL, `x NOT IN (1, 2, NULL)` evaluates to: `x != 1 AND x != 2 AND x != NULL`. Because `x != NULL` evaluates to `UNKNOWN`, the whole `AND` condition evaluates to `UNKNOWN` (falsy) for every row.<br><b>Rule:</b> Always use <b>`NOT EXISTS`</b> instead!",
        "Topic": "Joins & Set Operations",
        "Tags": "sql joins not_in null trap gotcha"
    },
    {
        "Question": "Why is `WHERE NOT EXISTS (...)` superior to `WHERE id NOT IN (...)`?",
        "Answer": "<b>ANSWER:</b> (1) Safe against `NULL` values, and (2) Often significantly faster.<br><br>`NOT EXISTS` uses three-valued boolean logic safely. In the query planner, `EXISTS` stops scanning the instant it finds the first match (short-circuiting), whereas `NOT IN` may have to scan all values to verify no NULLs exist.",
        "Topic": "Joins & Set Operations",
        "Tags": "sql joins not_exists not_in optimization"
    },
    {
        "Question": "What is a `LATERAL` Join in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> A join that allows the right-side subquery to reference columns from previous tables in the `FROM` clause.<br><br><b>Example:</b><br><code>SELECT c.name, top_order.amount <br>FROM customers c <br>LEFT JOIN LATERAL ( <br>    SELECT amount FROM orders o <br>    WHERE o.customer_id = c.id <br>    ORDER BY amount DESC LIMIT 1 <br>) top_order ON true;</code><br>Solves 'Top 1 per category' cleanly without complex window partitions.",
        "Topic": "Joins & Set Operations",
        "Tags": "sql joins lateral postgres analytics"
    },
    {
        "Question": "What happens if you filter the right table of a `LEFT JOIN` inside the `WHERE` clause?",
        "Answer": "<b>ANSWER:</b> It accidentally converts the `LEFT JOIN` into an `INNER JOIN`!<br><br><b>The Bug:</b><br><code>SELECT * FROM customers c <br>LEFT JOIN orders o ON c.id = o.customer_id <br>WHERE o.status = 'shipped';</code><br>Because unmatched customers have `o.status = NULL`, the condition `NULL = 'shipped'` evaluates to FALSE, discarding all non-purchasing customers! Fix: move `AND o.status = 'shipped'` into the `ON` clause.",
        "Topic": "Joins & Set Operations",
        "Tags": "sql joins left_join where_clause bug gotcha"
    },
    {
        "Question": "What is the difference between `UNION` and `UNION ALL`?",
        "Answer": "<b>ANSWER:</b> Deduplication sort vs. Raw streaming append.<br><br>• <b>`UNION`:</b> Combines results and performs an expensive in-memory sort to remove duplicate rows.<br>• <b>`UNION ALL`:</b> Concatenates results directly with ZERO sorting or deduplication. Always use `UNION ALL` unless you explicitly require deduplication.",
        "Topic": "Joins & Set Operations",
        "Tags": "sql set_operations union union_all performance"
    },

    # --- MODULE 4: QUERY PERFORMANCE, SARGABILITY & INDEX USAGE ---
    {
        "Question": "What does 'SARGable' mean in SQL query optimization?",
        "Answer": "<b>ANSWER:</b> Search Argument Able.<br><br>A query predicate is SARGable if the database engine can utilize an index to find matching rows via an <b>Index Seek / Index Scan</b>. Non-SARGable predicates force the database to evaluate expressions row-by-row in a slow <b>Full Table Scan</b>.",
        "Topic": "Query Optimization",
        "Tags": "sql optimization sargable index_scan"
    },
    {
        "Question": "Why is `WHERE YEAR(created_at) = 2024` non-SARGable, and how do you rewrite it?",
        "Answer": "<b>ANSWER:</b> Wrapping a column in a function prevents B-Tree index lookups.<br><br>The B-Tree contains raw timestamps, not the output of `YEAR()`. Postgres must compute `YEAR()` on every single row in the table.<br><b>The SARGable Rewrite:</b><br><code>WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';</code><br>Now Postgres jumps directly to the matching index range in microseconds!",
        "Topic": "Query Optimization",
        "Tags": "sql optimization sargable functions date index"
    },
    {
        "Question": "Why is `WHERE name LIKE '%Smith'` non-SARGable?",
        "Answer": "<b>ANSWER:</b> Leading wildcards cannot use standard B-Tree indexes.<br><br><b>The Phone Book Analogy:</b><br>A phone book is sorted alphabetically by first letter. You can easily find names starting with 'Smi%' (SARGable). But finding names ending with '%mith' requires reading every single entry in the entire phone book. (Fix: use full-text search or trigram GIN indexes).",
        "Topic": "Query Optimization",
        "Tags": "sql optimization sargable like wildcard"
    },
    {
        "Question": "What is the hidden performance cost of writing `SELECT *` in production?",
        "Answer": "<b>ANSWER:</b> (1) Heavy disk and network I/O, (2) Buffer cache pollution, and (3) Blocking Index-Only Scans.<br><br>Reading all 40 columns forces the engine to read wide table heap blocks off disk, wasting RAM cache and preventing the query planner from answering the query purely from a compact index.",
        "Topic": "Query Optimization",
        "Tags": "sql optimization select_star performance"
    },
    {
        "Question": "Why is using `SELECT DISTINCT` to hide duplicate rows an anti-pattern?",
        "Answer": "<b>ANSWER:</b> It masks incorrect join logic and consumes massive CPU/memory.<br><br>If a query returns duplicates, it almost always means an `INNER JOIN` had a 1-to-many relationship that wasn't properly aggregated. Adding `DISTINCT` forces Postgres to sort millions of rows in memory to deduplicate data that should never have been duplicated.",
        "Topic": "Query Optimization",
        "Tags": "sql optimization distinct anti_pattern"
    },
    {
        "Question": "What is a Covering Index (Index with `INCLUDE`)?",
        "Answer": "<b>ANSWER:</b> An index that includes extra payload columns in the leaf nodes without sorting on them.<br><br><b>Syntax:</b><br><code>CREATE INDEX idx_orders ON orders (customer_id) INCLUDE (order_date, total_amount);</code><br>Allows queries selecting `order_date` and `total_amount` to execute as an <b>Index-Only Scan</b> with zero table heap lookups.",
        "Topic": "Query Optimization",
        "Tags": "sql indexes covering_index include"
    },
    {
        "Question": "What is the 'Leftmost Prefix Rule' in multi-column composite indexes?",
        "Answer": "<b>ANSWER:</b> Queries can only use a composite index `(A, B, C)` if they filter on the leftmost columns.<br><br>• Filtering on `(A)` -> Uses index ✅<br>• Filtering on `(A, B)` -> Uses index ✅<br>• Filtering on `(B, C)` without `(A)` -> CANNOT use index ❌",
        "Topic": "Query Optimization",
        "Tags": "sql indexes composite leftmost_prefix"
    },
    {
        "Question": "What is a Partial Index in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> An index built over a subset of rows defined by a `WHERE` condition.<br><br><b>The SQL:</b><br><code>CREATE INDEX idx_unprocessed ON orders (created_at) WHERE status = 'PENDING';</code><br>If 99% of orders are 'COMPLETED', indexing the whole table wastes gigabytes of RAM. A partial index on the 1% 'PENDING' rows is 100x smaller and lightning fast.",
        "Topic": "Query Optimization",
        "Tags": "sql indexes partial_index postgres"
    },

    # --- MODULE 5: SQL EDGE CASES, DATA TYPES & GOTCHAS ---
    {
        "Question": "What is Three-Valued Logic in SQL?",
        "Answer": "<b>ANSWER:</b> Boolean expressions can evaluate to `TRUE`, `FALSE`, or `UNKNOWN`.<br><br>Whenever an expression compares anything to `NULL` (e.g. `salary > 50000` where salary is NULL), the result is `UNKNOWN`. In a `WHERE` clause, only expressions evaluating to `TRUE` are returned (both `FALSE` and `UNKNOWN` are filtered out).",
        "Topic": "SQL Gotchas",
        "Tags": "sql logic three_valued null unknown"
    },
    {
        "Question": "Why does `WHERE status != 'active'` exclude rows where `status` is NULL?",
        "Answer": "<b>ANSWER:</b> `NULL != 'active'` evaluates to `UNKNOWN`, not `TRUE`.<br><br>If you want to include NULLs, you must write:<br><code>WHERE status != 'active' OR status IS NULL;</code><br>Or in PostgreSQL: <code>WHERE status IS DISTINCT FROM 'active';</code>.",
        "Topic": "SQL Gotchas",
        "Tags": "sql gotchas null comparison"
    },
    {
        "Question": "What is the difference between `COUNT(*)` and `COUNT(column_name)`?",
        "Answer": "<b>ANSWER:</b> Counting all rows vs. Counting non-null values.<br><br>• <b>`COUNT(*)`:</b> Counts every row that matches the criteria, including rows containing NULLs.<br>• <b>`COUNT(col)`:</b> Counts ONLY rows where `col IS NOT NULL`. If all values in `col` are NULL, it returns 0.",
        "Topic": "SQL Gotchas",
        "Tags": "sql gotchas count nulls"
    },
    {
        "Question": "What does `COALESCE(a, b, c)` do in SQL?",
        "Answer": "<b>ANSWER:</b> Returns the first non-null expression from the list.<br><br><b>Example:</b><br><code>SELECT COALESCE(phone_number, mobile_number, 'No Phone Available') <br>FROM contacts;</code>",
        "Topic": "SQL Gotchas",
        "Tags": "sql functions coalesce nulls"
    },
    {
        "Question": "What is the Integer Division Truncation gotcha in SQL?",
        "Answer": "<b>ANSWER:</b> Dividing two integers performs integer division, discarding the decimal remainder.<br><br>• <code>SELECT 5 / 2;</code> -> Returns <b>`2`</b> (not 2.5)!<br>• <b>Fix:</b> Cast at least one operand to float or decimal: <code>SELECT 5.0 / 2;</code> or <code>SELECT 5::numeric / 2;</code> -> Returns <b>`2.5`</b>.",
        "Topic": "SQL Gotchas",
        "Tags": "sql gotchas division integers types"
    },
    {
        "Question": "What is the difference between `WHERE` and `HAVING` in SQL?",
        "Answer": "<b>ANSWER:</b> Filtering rows before grouping vs. Filtering aggregated groups after grouping.<br><br>• <b>`WHERE`:</b> Filters individual rows before `GROUP BY` runs. Cannot use aggregate functions like `SUM()` or `COUNT()`.<br>• <b>`HAVING`:</b> Filters groups after aggregation. Example: <code>HAVING COUNT(*) > 5</code>.",
        "Topic": "SQL Gotchas",
        "Tags": "sql syntax where having groupby"
    },
    {
        "Question": "In `SELECT ... WHERE EXISTS (SELECT ...)` does the select list inside `EXISTS` matter?",
        "Answer": "<b>ANSWER:</b> No, it is completely ignored by the query planner.<br><br>Whether you write `EXISTS (SELECT 1 ...)`, `EXISTS (SELECT * ...)`, or `EXISTS (SELECT 1/0 ...)`, Postgres only checks whether a matching row exists. It never evaluates the select list, so writing `SELECT 1` is standard convention.",
        "Topic": "SQL Gotchas",
        "Tags": "sql syntax exists optimization"
    },
    {
        "Question": "How do you read `cost=0.00..45.20 rows=100 width=8` in a PostgreSQL EXPLAIN plan?",
        "Answer": "<b>ANSWER:</b> The optimizer's estimated effort to execute the node.<br><br>• <b>`0.00`:</b> Startup cost (cost before the first row can be returned).<br>• <b>`45.20`:</b> Total cost to process all rows in arbitrary disk-page I/O units.<br>• <b>`rows=100`:</b> Estimated number of rows output.<br>• <b>`width=8`:</b> Estimated average byte size of each row.",
        "Topic": "Query Optimization",
        "Tags": "sql explain cost planner optimization"
    }
]

# Write to decks/sql_tuning_deck.csv
os.makedirs('decks', exist_ok=True)
with open('decks/sql_tuning_deck.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    writer.writeheader()
    for card in sql_cards:
        writer.writerow(card)

print(f"Batch 1 of SQL Tuning Deck complete: wrote {len(sql_cards)} cards.")
