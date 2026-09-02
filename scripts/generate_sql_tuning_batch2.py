import csv

batch2_cards = [
    # --- ADVANCED ANALYTICAL SQL & PATTERNS ---
    {
        "Question": "What is the modern `FILTER (WHERE ...)` clause in PostgreSQL aggregations?",
        "Answer": "<b>ANSWER:</b> A cleaner, faster alternative to conditional `CASE WHEN` aggregations.<br><br><b>The SQL:</b><br><code>SELECT dept_id, <br>       COUNT(*) AS total_employees, <br>       COUNT(*) FILTER (WHERE salary > 100000) AS high_earners <br>FROM employees GROUP BY dept_id;</code><br>Eliminates verbose `COUNT(CASE WHEN salary > 100000 THEN 1 END)` statements.",
        "Topic": "Analytical SQL",
        "Tags": "sql postgres filter conditional_aggregation"
    },
    {
        "Question": "How do you concatenate multiple string rows into a single comma-separated list in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Use `STRING_AGG(column, delimiter [ORDER BY ...])`.<br><br><b>The SQL:</b><br><code>SELECT dept_id, <br>       STRING_AGG(name, ', ' ORDER BY name) AS employee_names <br>FROM employees GROUP BY dept_id;</code><br>(Equivalent to `GROUP_CONCAT` in MySQL or `LISTAGG` in Oracle).",
        "Topic": "Analytical SQL",
        "Tags": "sql postgres string_agg string_manipulation"
    },
    {
        "Question": "How do you calculate the Median value of a column in SQL?",
        "Answer": "<b>ANSWER:</b> Use `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY col)`.<br><br><b>The SQL:</b><br><code>SELECT dept_id, <br>       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median_salary <br>FROM employees GROUP BY dept_id;</code><br>More resilient to extreme outliers than `AVG()`.",
        "Topic": "Analytical SQL",
        "Tags": "sql analytics median percentile_cont"
    },
    {
        "Question": "What is the 'Gaps and Islands' problem in SQL?",
        "Answer": "<b>ANSWER:</b> Detecting continuous sequences ('islands') and missing breaks ('gaps') in sequential data.<br><br><b>Classic Interview Scenario:</b> Finding the longest consecutive streak of daily user logins. Solved by taking the difference between sequential dates and `ROW_NUMBER()`, which creates a constant group identifier for consecutive rows.",
        "Topic": "Analytical SQL",
        "Tags": "sql patterns gaps_and_islands interview"
    },
    {
        "Question": "How do you generate a continuous date sequence in PostgreSQL to fill reporting gaps?",
        "Answer": "<b>ANSWER:</b> Use `generate_series()`.<br><br><b>The SQL:</b><br><code>SELECT day::date FROM generate_series( <br>    '2024-01-01'::date, '2024-01-31'::date, '1 day'::interval <br>) AS day;</code><br>Perform a `LEFT JOIN` from this date spine to your sales table so days with zero sales still show up with `0`.",
        "Topic": "Analytical SQL",
        "Tags": "sql postgres generate_series date_spine"
    },
    {
        "Question": "What is `UNNEST()` in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Expands an array into a set of relational rows.<br><br><b>The SQL:</b><br><code>SELECT UNNEST(ARRAY['red', 'green', 'blue']) AS color;</code><br>Converts a 3-element array into 3 discrete rows, enabling standard `JOIN` and `GROUP BY` operations.",
        "Topic": "Analytical SQL",
        "Tags": "sql postgres unnest arrays"
    },
    {
        "Question": "How do you perform an Anti-Join to find all customers who have NEVER placed an order?",
        "Answer": "<b>ANSWER:</b> Using `NOT EXISTS` or `LEFT JOIN ... WHERE right.id IS NULL`.<br><br><b>Approach 1 (Recommended):</b><br><code>SELECT c.id, c.name FROM customers c <br>WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);</code><br><b>Approach 2:</b><br><code>SELECT c.id, c.name FROM customers c <br>LEFT JOIN orders o ON c.id = o.customer_id <br>WHERE o.id IS NULL;</code>",
        "Topic": "Joins & Set Operations",
        "Tags": "sql joins anti_join not_exists"
    },
    {
        "Question": "What is a Semi-Join and how does it differ from an Inner Join?",
        "Answer": "<b>ANSWER:</b> Filtering rows based on existence in another table WITHOUT duplicating rows.<br><br><b>The SQL:</b><br><code>SELECT * FROM departments d <br>WHERE EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.id);</code><br>If a department has 100 employees, an `INNER JOIN` duplicates the department 100 times. A Semi-Join (`EXISTS`) returns the department exactly ONCE.",
        "Topic": "Joins & Set Operations",
        "Tags": "sql joins semi_join exists"
    },

    # --- ADVANCED QUERY PERFORMANCE & SARGABILITY ---
    {
        "Question": "What is the 'Implicit Type Coercion Trap' in SQL query performance?",
        "Answer": "<b>ANSWER:</b> Comparing columns of mismatched data types forces a full table scan.<br><br><b>Scenario:</b> `phone_number` is `VARCHAR`, but you query: <code>WHERE phone_number = 1234567890;</code><br>Because integers have higher type precedence, Postgres casts the column: <code>WHERE phone_number::bigint = 1234567890</code>. The function call disables the B-Tree index! Always pass string literals for varchar columns.",
        "Topic": "Query Optimization",
        "Tags": "sql optimization type_coercion sargable index"
    },
    {
        "Question": "Why is `WHERE salary * 1.10 > 50000` non-SARGable, and how should it be written?",
        "Answer": "<b>ANSWER:</b> Performing arithmetic on the column prevents index lookups.<br><br><b>Non-SARGable:</b> <code>WHERE salary * 1.10 > 50000;</code> (Evaluated row-by-row).<br><b>SARGable Rewrite:</b> <code>WHERE salary > 50000 / 1.10;</code> (Evaluated once as a constant; enables B-Tree index scan).",
        "Topic": "Query Optimization",
        "Tags": "sql optimization sargable arithmetic"
    },
    {
        "Question": "Why are Half-Open Intervals `[start, end)` the gold standard for timestamp querying?",
        "Answer": "<b>ANSWER:</b> To prevent boundary precision errors and missed transactions.<br><br><b>The Bug:</b> <code>WHERE created_at BETWEEN '2024-01-01' AND '2024-01-02'</code> stops at `2024-01-02 00:00:00`, missing all transactions during the day on Jan 2nd.<br><b>The Fix:</b><br><code>WHERE created_at >= '2024-01-01' AND created_at < '2024-01-03';</code>",
        "Topic": "Query Optimization",
        "Tags": "sql optimization timestamps between intervals"
    },
    {
        "Question": "What is the optimal column order for a Composite Index: Equality vs. Range columns?",
        "Answer": "<b>ANSWER:</b> Equality columns FIRST, Range columns LAST.<br><br><b>Query:</b> <code>WHERE status = 'ACTIVE' AND created_at >= '2024-01-01'</code><br>• <b>Correct Index:</b> `(status, created_at)` -> Jumps directly to 'ACTIVE' and scans the date range.<br>• <b>Bad Index:</b> `(created_at, status)` -> Must scan the entire date range across all statuses, filtering row-by-row.",
        "Topic": "Query Optimization",
        "Tags": "sql indexes composite equality_first range"
    },
    {
        "Question": "Why is Keyset Pagination (Seek Method) vastly superior to `OFFSET / LIMIT` pagination?",
        "Answer": "<b>ANSWER:</b> $O(1)$ constant time vs. $O(N)$ linear degradation.<br><br>• <b>Offset Pagination (`LIMIT 20 OFFSET 500000`):</b> Postgres must scan and discard 500,000 rows off disk before returning 20 rows. Extremely slow on deep pages.<br>• <b>Keyset Pagination:</b> <code>WHERE id > 500000 ORDER BY id LIMIT 20;</code> uses a direct B-Tree seek to jump directly to ID 500,001 in microseconds.",
        "Topic": "Query Optimization",
        "Tags": "sql pagination offset keyset performance"
    },
    {
        "Question": "What is a Functional (Expression) Index in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> An index built on the computed output of an expression or function.<br><br><b>The SQL:</b><br><code>CREATE INDEX idx_lower_email ON users (LOWER(email));</code><br>Enables instant index lookups for case-insensitive queries like <code>WHERE LOWER(email) = 'test@abc.com'</code>.",
        "Topic": "Query Optimization",
        "Tags": "sql indexes functional expression postgres"
    },
    {
        "Question": "What is a GIN (Generalized Inverted Index) in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> An index designed for composite items with internal elements (JSONB, Arrays, Full-Text Search).<br><br><b>Usage:</b><br><code>CREATE INDEX idx_user_tags ON users USING gin (tags);</code><br>Enables lightning-fast searches like <code>WHERE tags @> ARRAY['sql', 'postgres']</code>.",
        "Topic": "Query Optimization",
        "Tags": "sql indexes gin jsonb postgres"
    },
    {
        "Question": "What is a BRIN (Block Range Index) in PostgreSQL and when is it ideal?",
        "Answer": "<b>ANSWER:</b> An ultra-compact index that stores only minimum and maximum values for 128-page ranges.<br><br>• <b>Size:</b> Takes 100x less RAM than a B-Tree.<br>• <b>Ideal Scenario:</b> Massive multi-billion row append-only tables (IoT sensors, audit logs) naturally ordered by timestamp or auto-incrementing ID on disk.",
        "Topic": "Query Optimization",
        "Tags": "sql indexes brin big_data postgres"
    },
    {
        "Question": "How does `NULLS FIRST` vs. `NULLS LAST` work in PostgreSQL `ORDER BY`?",
        "Answer": "<b>ANSWER:</b> Controls where NULL values appear in sorted results.<br><br>• <b>`ORDER BY col ASC`:</b> Defaults to `NULLS LAST`.<br>• <b>`ORDER BY col DESC`:</b> Defaults to `NULLS FIRST` (putting NULLs at the very top!).<br>If you want highest numbers first without NULLs at the top, write: <code>ORDER BY col DESC NULLS LAST;</code>.",
        "Topic": "SQL Gotchas",
        "Tags": "sql sort order_by nulls gotcha"
    },
    {
        "Question": "What are the 3 fundamental Join Algorithms used by the PostgreSQL Query Planner?",
        "Answer": "<b>ANSWER:</b> Nested Loop, Hash Join, and Merge Join.<br><br>1. <b>Nested Loop:</b> Ideal when the outer table is small and inner table has an index ($O(N \\log M)$).<br>2. <b>Hash Join:</b> Builds in-memory hash table of smaller relation; best for unsorted medium/large joins.<br>3. <b>Merge Join:</b> Streams two inputs pre-sorted on join keys with zero memory overhead.",
        "Topic": "Query Optimization",
        "Tags": "sql joins explain nested_loop hash_join merge_join"
    },
    {
        "Question": "What is the difference between `Shared Hit` and `Shared Read` in `EXPLAIN (ANALYZE, BUFFERS)`?",
        "Answer": "<b>ANSWER:</b> RAM Buffer Cache vs. Physical Disk I/O.<br><br>• <b>`Shared Hit`:</b> 8KB pages found immediately in fast RAM (0ms latency).<br>• <b>`Shared Read`:</b> 8KB pages that had to be read from slow physical storage disk.<br>High `Shared Read` numbers indicate a cold cache or queries reading too much data off disk.",
        "Topic": "Query Optimization",
        "Tags": "sql explain buffers shared_hit shared_read"
    },
    {
        "Question": "Why should you always run `ANALYZE tablename;` after bulk data loads in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> To update distribution statistics and data histograms for the query planner.<br><br>If the planner thinks a table has 10 rows when it actually has 10,000,000 rows, it will make disastrous choices (like choosing a Nested Loop Seq Scan that runs for 4 hours instead of a 2-second Hash Join).",
        "Topic": "Query Optimization",
        "Tags": "sql tuning analyze statistics planner"
    }
]

with open('decks/sql_tuning_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in batch2_cards:
        writer.writerow(card)

print(f"Batch 2 appended {len(batch2_cards)} cards to decks/sql_tuning_deck.csv.")
