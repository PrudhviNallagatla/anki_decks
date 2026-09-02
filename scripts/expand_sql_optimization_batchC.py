import csv

batchC = [
    # --- DEEP EXPLAIN PLAN & PLANNER FORENSICS ---
    {
        "Question": "What does a massive discrepancy between 'rows' and 'actual rows' in EXPLAIN ANALYZE indicate?",
        "Answer": "<b>ANSWER:</b> Stale or missing database statistics.<br><br><b>Example:</b> `rows=10` vs `actual rows=100000`.<br>The query planner estimated 10 rows and chose a slow Nested Loop; in reality, 100,000 rows were processed, grinding the query to a halt.<br><b>Fix:</b> Run <code>ANALYZE table_name;</code> or increase statistics target: <code>ALTER TABLE t ALTER col SET STATISTICS 1000;</code>.",
        "Topic": "EXPLAIN Forensics",
        "Tags": "sql explain analyze rows statistics stale"
    },
    {
        "Question": "What is a 'Nested Loop' in an EXPLAIN plan and when does it become a performance disaster?",
        "Answer": "<b>ANSWER:</b> For every row in the outer table, it scans the inner table.<br><br>• <b>Fast:</b> When outer table has 5 rows and inner table uses a B-Tree index lookup ($5 \\times 1\\text{ms} = 5\\text{ms}$).<br>• <b>Disaster:</b> When outer table has 500,000 rows (`loops=500000`). Executing an inner loop 500,000 times will freeze the CPU for hours. Planner should have chosen a Hash Join.",
        "Topic": "EXPLAIN Forensics",
        "Tags": "sql explain nested_loop joins loops disaster"
    },
    {
        "Question": "What is the difference between HashAggregate and GroupAggregate in an EXPLAIN plan?",
        "Answer": "<b>ANSWER:</b> In-memory hash table vs. Stream aggregation on presorted data.<br><br>• <b>HashAggregate:</b> Builds a hash table of group keys in RAM (`work_mem`). Extremely fast for unsorted inputs.<br>• <b>GroupAggregate:</b> Requires input to be already sorted by group keys. Minimal RAM usage, but incurs sort overhead if not backed by an index.",
        "Topic": "EXPLAIN Forensics",
        "Tags": "sql explain hashaggregate groupaggregate aggregation"
    },
    {
        "Question": "What is Parallel Query Execution in PostgreSQL and what do Gather nodes represent?",
        "Answer": "<b>ANSWER:</b> Dividing table scans across multiple background CPU worker processes.<br><br>• <b>`Gather`:</b> Master backend process collecting rows computed in parallel by background worker processes.<br>• <b>`Gather Merge`:</b> Master process combining presorted streams from parallel workers while preserving overall sort order.",
        "Topic": "EXPLAIN Forensics",
        "Tags": "sql explain parallel gather workers performance"
    },
    {
        "Question": "Why might a large query refuse to execute in parallel in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Functions marked `VOLATILE` or non-parallel-safe operations.<br><br>If a query calls a user-defined function not marked `PARALLEL SAFE`, writes data, uses cursors, or runs in a serializable transaction, Postgres immediately forces single-threaded execution.",
        "Topic": "EXPLAIN Forensics",
        "Tags": "sql explain parallel volatile parallel_safe functions"
    },
    {
        "Question": "What is the difference between an Exact and Lossy Bitmap Heap Scan in an EXPLAIN plan?",
        "Answer": "<b>ANSWER:</b> Memory limit (`work_mem`) exhaustion during bitmap index construction.<br><br>• <b>Exact Pages:</b> The bitmap held exact physical row pointers (`ctid`). Fast direct retrieval.<br>• <b>Lossy Pages:</b> Insufficient `work_mem` forced the bitmap to track only page numbers, requiring Postgres to re-check all row visibility conditions on disk. Raise `work_mem` to fix.",
        "Topic": "EXPLAIN Forensics",
        "Tags": "sql explain bitmap_scan lossy exact work_mem"
    },
    {
        "Question": "What is an 'External merge Disk' sort in an EXPLAIN plan and how do you eliminate it?",
        "Answer": "<b>ANSWER:</b> Sort dataset exceeded `work_mem` and spilled to slow temporary disk files.<br><br><b>The Warning:</b> <code>Sort Method: external merge  Disk: 45280kB</code>.<br><b>Fix:</b> Raise `work_mem` for the query session: <code>SET work_mem = '128MB';</code> so the sort executes in ultra-fast CPU cache using `quicksort`.",
        "Topic": "EXPLAIN Forensics",
        "Tags": "sql explain sort external_merge work_mem disk_spill"
    },
    {
        "Question": "What is a 'Memoize' node in PostgreSQL 14+ EXPLAIN plans?",
        "Answer": "<b>ANSWER:</b> An in-memory cache for parameterized inner index scans.<br><br>When an outer loop supplies the same parameter value multiple times to an inner join, the `Memoize` node serves the result instantly from cache instead of re-executing the index seek.",
        "Topic": "EXPLAIN Forensics",
        "Tags": "sql explain memoize postgres14 cache joins"
    },
    {
        "Question": "What happens when a Hash Join reports `Batches: 4` in an EXPLAIN plan?",
        "Answer": "<b>ANSWER:</b> The inner hash table was too large to fit in `work_mem`, forcing disk spills.<br><br>When `Batches = 1`, the entire hash table fits in RAM. When `Batches > 1`, Postgres splits the dataset into batches, writing overflow to temporary disk files. Increasing `work_mem` restores 1-batch RAM execution.",
        "Topic": "EXPLAIN Forensics",
        "Tags": "sql explain hash_join batches work_mem disk"
    },
    {
        "Question": "Why should you set `random_page_cost = 1.1` on modern SSD / NVMe database servers?",
        "Answer": "<b>ANSWER:</b> Default `random_page_cost = 4.0` was designed for 1990s spinning hard drives.<br><br>Spinning magnetic disks penalize random seeks by 4x. NVMe SSDs have near-zero seek latency ($1.1\\times$). Lowering `random_page_cost` stops the planner from mistakenly choosing slow sequential scans over fast index scans.",
        "Topic": "EXPLAIN Forensics",
        "Tags": "sql explain random_page_cost ssds planner tuning"
    },
    {
        "Question": "How do you control whether a CTE is inlined or materialized in PostgreSQL 12+?",
        "Answer": "<b>ANSWER:</b> Use `AS MATERIALIZED` or `AS NOT MATERIALIZED`.<br><br>• <code>WITH cte AS NOT MATERIALIZED (...)</code>: Forces inlining (folds CTE into main query to allow predicate pushdown and index scans).<br>• <code>WITH cte AS MATERIALIZED (...)</code>: Forces evaluation as an isolated temporary table.",
        "Topic": "Query Optimization",
        "Tags": "sql ctes materialized inlining postgres12"
    },
    {
        "Question": "What is an `InitPlan` in an EXPLAIN plan?",
        "Answer": "<b>ANSWER:</b> An uncorrelated subquery executed once before the main query begins.<br><br><b>Example:</b> `WHERE salary > (SELECT AVG(salary) FROM employees)`.<br>The subquery does not depend on outer rows; Postgres executes it once as an `InitPlan`, caches the result, and reuses it for all outer comparisons.",
        "Topic": "EXPLAIN Forensics",
        "Tags": "sql explain initplan subquery caching"
    },

    # --- ADVANCED SQL FUNCTIONS & GOTCHAS ---
    {
        "Question": "How do you prevent 'division by zero' errors in SQL without writing messy CASE statements?",
        "Answer": "<b>ANSWER:</b> Use `NULLIF(divisor, 0)`.<br><br><b>The SQL:</b><br><code>SELECT revenue / NULLIF(total_users, 0) AS arpu <br>FROM metrics;</code><br>If `total_users` is 0, `NULLIF` turns it into `NULL`. Any number divided by `NULL` safely yields `NULL` instead of crashing with a fatal error.",
        "Topic": "Analytical SQL",
        "Tags": "sql division_by_zero nullif math safety"
    },
    {
        "Question": "How do you truncate a timestamp to the beginning of the month, week, or hour in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Use `DATE_TRUNC()`.<br><br><b>The SQL:</b><br><code>SELECT DATE_TRUNC('month', created_at) AS month_start, <br>       COUNT(*) AS total_signups <br>FROM users GROUP BY DATE_TRUNC('month', created_at);</code>",
        "Topic": "Date Functions",
        "Tags": "sql dates date_trunc grouping analytics"
    },
    {
        "Question": "How do you generate a continuous date spine for every day of January 2024?",
        "Answer": "<b>ANSWER:</b> Use `generate_series()` with date casting.<br><br><b>The SQL:</b><br><code>SELECT day::date FROM generate_series( <br>    '2024-01-01'::timestamp, <br>    '2024-01-31'::timestamp, <br>    '1 day'::interval <br>) AS day;</code><br>Essential for left-joining sales data so days with zero sales still show up as 0 instead of missing.",
        "Topic": "Analytical SQL",
        "Tags": "sql generate_series date_spine dates reporting"
    },
    {
        "Question": "How do you find missing ID numbers in a sequence using `generate_series()`?",
        "Answer": "<b>ANSWER:</b> Left join expected sequence against table and filter `IS NULL`.<br><br><b>The SQL:</b><br><code>SELECT s.id FROM generate_series(1, 1000) AS s(id) <br>LEFT JOIN orders o ON s.id = o.id <br>WHERE o.id IS NULL;</code><br>Instantly reveals gaps in auto-incrementing voucher or invoice numbers.",
        "Topic": "Analytical SQL",
        "Tags": "sql generate_series gaps anti_join debugging"
    },
    {
        "Question": "How do you aggregate strings in a specific sorted order in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Use `STRING_AGG()` with an internal `ORDER BY`.<br><br><b>The SQL:</b><br><code>SELECT department_id, <br>       STRING_AGG(name, ', ' ORDER BY salary DESC) AS top_earners <br>FROM employees GROUP BY department_id;</code>",
        "Topic": "String Manipulation",
        "Tags": "sql string_agg aggregate strings order"
    },
    {
        "Question": "What is the classic frame trap with `LAST_VALUE()` in window functions?",
        "Answer": "<b>ANSWER:</b> By default, the window frame ends at the `CURRENT ROW`, returning the current row instead of the true last value!<br><br><b>The Bug:</b> `LAST_VALUE(val) OVER (ORDER BY id)` returns `val` itself!<br><b>The Fix:</b> Explicitly extend the frame to the end of partition: <code>LAST_VALUE(val) OVER (ORDER BY id ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING)</code>.",
        "Topic": "Window Functions",
        "Tags": "sql window_functions last_value frame gotcha"
    },
    {
        "Question": "What is `NTILE(n)` and how do you divide users into 4 spending quartiles?",
        "Answer": "<b>ANSWER:</b> Divides sorted rows into `n` equal-sized buckets (1 to n).<br><br><b>The SQL:</b><br><code>SELECT user_id, spend, <br>       NTILE(4) OVER (ORDER BY spend DESC) AS quartile <br>FROM customer_spend;</code><br>Quartile 1 = Top 25% spenders; Quartile 4 = Bottom 25%.",
        "Topic": "Window Functions",
        "Tags": "sql window_functions ntile quartiles analytics"
    },
    {
        "Question": "What is the critical difference between `COUNT(column)` and `COUNT(*)`?",
        "Answer": "<b>ANSWER:</b> Non-NULL counting vs. Total row counting.<br><br>• <b>`COUNT(*)`:</b> Counts every row regardless of column contents (fastest, optimized by planner).<br>• <b>`COUNT(column)`:</b> Evaluates every row and excludes rows where `column IS NULL`. If 10 rows have NULL, it returns `Total - 10`.",
        "Topic": "Analytical SQL",
        "Tags": "sql count null gotcha basics"
    }
]

with open('decks/sql_tuning_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in batchC:
        writer.writerow(card)

print(f"Batch C complete: appended {len(batchC)} cards.")
