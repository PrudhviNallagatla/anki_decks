import csv

batchA = [
    # --- LEETCODE HARD & REAL INTERVIEW PUZZLES ---
    {
        "Question": "How do you find numbers that appear at least 3 times consecutively in a table?",
        "Answer": "<b>ANSWER:</b> Use `LEAD()` and `LAG()` inside a CTE or subquery.<br><br><b>The SQL:</b><br><code>WITH consecutive AS ( <br>    SELECT num, <br>           LAG(num, 1) OVER (ORDER BY id) AS prev_num, <br>           LEAD(num, 1) OVER (ORDER BY id) AS next_num <br>    FROM logs <br>) <br>SELECT DISTINCT num FROM consecutive <br>WHERE num = prev_num AND num = next_num;</code>",
        "Topic": "Interview SQL",
        "Tags": "sql interview consecutive lead lag leetcode"
    },
    {
        "Question": "How do you solve the classic 'Human Traffic of Stadium' (3+ consecutive rows with condition) problem?",
        "Answer": "<b>ANSWER:</b> Use the `id - ROW_NUMBER()` island grouping technique.<br><br><b>The SQL:</b><br><code>WITH high_traffic AS ( <br>    SELECT id, visit_date, people, <br>           id - ROW_NUMBER() OVER (ORDER BY id) AS island_id <br>    FROM stadium WHERE people >= 100 <br>), grouped AS ( <br>    SELECT *, COUNT(*) OVER (PARTITION BY island_id) AS streak_len <br>    FROM high_traffic <br>) <br>SELECT id, visit_date, people FROM grouped WHERE streak_len >= 3 ORDER BY visit_date;</code>",
        "Topic": "Interview SQL",
        "Tags": "sql interview gaps_and_islands window_functions leetcode"
    },
    {
        "Question": "How do you calculate the Second Highest Salary in SQL without using LIMIT / OFFSET?",
        "Answer": "<b>ANSWER:</b> Use a subquery with `MAX()`.<br><br><b>The SQL:</b><br><code>SELECT MAX(salary) AS second_highest_salary <br>FROM employees <br>WHERE salary < (SELECT MAX(salary) FROM employees);</code><br>Returns `NULL` cleanly if no second highest salary exists (whereas `LIMIT 1 OFFSET 1` returns 0 rows).",
        "Topic": "Interview SQL",
        "Tags": "sql interview max subquery second_highest"
    },
    {
        "Question": "How do you calculate the Day-1 User Retention Rate in SQL?",
        "Answer": "<b>ANSWER:</b> Join users' install date with their login activity on `install_date + 1 day`.<br><br><b>The SQL:</b><br><code>WITH installs AS ( <br>    SELECT user_id, MIN(event_date) AS install_date <br>    FROM activity GROUP BY user_id <br>) <br>SELECT ROUND(COUNT(a.user_id)::numeric / COUNT(i.user_id), 4) AS day1_retention_rate <br>FROM installs i <br>LEFT JOIN activity a ON i.user_id = a.user_id AND a.event_date = i.install_date + INTERVAL '1 day';</code>",
        "Topic": "Interview SQL",
        "Tags": "sql interview retention cohort analytics"
    },
    {
        "Question": "How do you swap seats for every two adjacent students in a classroom seating table?",
        "Answer": "<b>ANSWER:</b> Use `CASE` with odd/even ID arithmetic and `COALESCE(LEAD())`.<br><br><b>The SQL:</b><br><code>SELECT CASE <br>    WHEN id % 2 = 1 AND id = (SELECT MAX(id) FROM seat) THEN id <br>    WHEN id % 2 = 1 THEN id + 1 <br>    ELSE id - 1 <br>END AS id, student <br>FROM seat ORDER BY id;</code>",
        "Topic": "Interview SQL",
        "Tags": "sql interview case arithmetic leetcode"
    },
    {
        "Question": "How do you find customers who have bought ALL products available in the store?",
        "Answer": "<b>ANSWER:</b> `GROUP BY customer_id` with `HAVING COUNT(DISTINCT product_id)` equal to total product count.<br><br><b>The SQL:</b><br><code>SELECT customer_id FROM customer_purchases <br>GROUP BY customer_id <br>HAVING COUNT(DISTINCT product_id) = (SELECT COUNT(*) FROM products);</code>",
        "Topic": "Interview SQL",
        "Tags": "sql interview having count distinct division"
    },
    {
        "Question": "How do you find managers who have at least 5 direct reports?",
        "Answer": "<b>ANSWER:</b> Group reports by `manager_id` and join back to the Employee table.<br><br><b>The SQL:</b><br><code>SELECT m.name FROM employees m <br>JOIN employees e ON m.id = e.manager_id <br>GROUP BY m.id, m.name <br>HAVING COUNT(e.id) >= 5;</code>",
        "Topic": "Interview SQL",
        "Tags": "sql interview joins groupby having"
    },
    {
        "Question": "How do you delete duplicate rows from a table while preserving the row with the smallest ID?",
        "Answer": "<b>ANSWER:</b> Use `DELETE ... WHERE id NOT IN (SELECT MIN(id) ...)`.<br><br><b>The SQL:</b><br><code>DELETE FROM users <br>WHERE id NOT IN ( <br>    SELECT MIN(id) FROM users GROUP BY email <br>);</code><br>Or in PostgreSQL using `ctid`: <code>DELETE FROM users a USING users b WHERE a.email = b.email AND a.ctid > b.ctid;</code>.",
        "Topic": "Interview SQL",
        "Tags": "sql interview delete duplicates ctid dml"
    },
    {
        "Question": "How do you build a Pivot Table in standard SQL without using proprietary vendor extensions?",
        "Answer": "<b>ANSWER:</b> Use Conditional Aggregation with `MAX(CASE WHEN ...)`.<br><br><b>The SQL:</b><br><code>SELECT year, <br>       SUM(CASE WHEN quarter = 'Q1' THEN revenue ELSE 0 END) AS q1_rev, <br>       SUM(CASE WHEN quarter = 'Q2' THEN revenue ELSE 0 END) AS q2_rev, <br>       SUM(CASE WHEN quarter = 'Q3' THEN revenue ELSE 0 END) AS q3_rev, <br>       SUM(CASE WHEN quarter = 'Q4' THEN revenue ELSE 0 END) AS q4_rev <br>FROM sales GROUP BY year;</code>",
        "Topic": "Analytical SQL",
        "Tags": "sql pivot conditional_aggregation case"
    },
    {
        "Question": "How do you Unpivot columns into rows in modern PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Use `CROSS JOIN LATERAL (VALUES ...)`.<br><br><b>The SQL:</b><br><code>SELECT id, metric_name, metric_value <br>FROM quarterly_results <br>CROSS JOIN LATERAL (VALUES <br>    ('Q1', q1_revenue), <br>    ('Q2', q2_revenue), <br>    ('Q3', q3_revenue), <br>    ('Q4', q4_revenue) <br>) AS v(metric_name, metric_value);</code>",
        "Topic": "Analytical SQL",
        "Tags": "sql unpivot lateral values postgres"
    },
    {
        "Question": "How do you calculate a 7-day Rolling Average of daily sales per customer?",
        "Answer": "<b>ANSWER:</b> Use `AVG()` with `PARTITION BY customer_id` and a 6-preceding row frame.<br><br><b>The SQL:</b><br><code>SELECT customer_id, sale_date, amount, <br>       ROUND(AVG(amount) OVER ( <br>           PARTITION BY customer_id <br>           ORDER BY sale_date <br>           ROWS BETWEEN 6 PRECEDING AND CURRENT ROW <br>       ), 2) AS rolling_7day_avg <br>FROM customer_sales;</code>",
        "Topic": "Window Functions",
        "Tags": "sql window_functions rolling_avg moving_window"
    },

    # --- ADVANCED QUERY REWRITING & OPTIMIZATION ---
    {
        "Question": "Why does `WHERE a = 1 OR b = 2` frequently cause slow Sequential Scans, and how do you optimize it?",
        "Answer": "<b>ANSWER:</b> B-Tree indexes cannot be used simultaneously across two different columns joined by `OR`.<br><br>Postgres must scan the entire table to evaluate both conditions.<br><b>The `UNION ALL` Rewrite:</b><br><code>SELECT * FROM orders WHERE a = 1 <br>UNION <br>SELECT * FROM orders WHERE b = 2;</code><br>Postgres executes two separate, blazing-fast Index Seeks and combines the results!",
        "Topic": "Query Optimization",
        "Tags": "sql optimization or_to_union sargable index"
    },
    {
        "Question": "How do you update a table based on values from another table using `UPDATE ... FROM`?",
        "Answer": "<b>ANSWER:</b> Use the `UPDATE ... FROM ... WHERE` join syntax.<br><br><b>The SQL:</b><br><code>UPDATE accounts a <br>SET balance = a.balance + b.bonus <br>FROM yearly_bonuses b <br>WHERE a.employee_id = b.employee_id;</code><br>100x faster than writing a correlated subquery in the `SET` clause.",
        "Topic": "Advanced DML",
        "Tags": "sql dml update_from join optimization"
    },
    {
        "Question": "How do you optimize a query with a correlated subquery in the `SELECT` clause?",
        "Answer": "<b>ANSWER:</b> Rewrite it as a `LEFT JOIN` with `GROUP BY`.<br><br><b>Slow ($O(N \\times M)$):</b><br><code>SELECT c.name, (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) FROM customers c;</code><br><b>Fast ($O(N + M)$):</b><br><code>SELECT c.name, COUNT(o.id) FROM customers c <br>LEFT JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.name;</code>",
        "Topic": "Query Optimization",
        "Tags": "sql optimization correlated_subquery left_join"
    },
    {
        "Question": "What is the Equality-Sort-Range (ESR) Rule for designing multi-column composite indexes?",
        "Answer": "<b>ANSWER:</b> The optimal column order in `CREATE INDEX (col1, col2, col3)`:<br><br>1. <b>Equality (E):</b> Columns filtered by `=` come FIRST.<br>2. <b>Sort (S):</b> Columns used in `ORDER BY` come SECOND.<br>3. <b>Range (R):</b> Columns filtered by `<`, `>`, `BETWEEN` come LAST.<br>Guarantees an index seek, zero-cost sorting, and immediate range bounds.",
        "Topic": "Query Optimization",
        "Tags": "sql indexes esr composite design tuning"
    },
    {
        "Question": "What is `SELECT ... FOR UPDATE SKIP LOCKED` and why is it used for high-concurrency job queues?",
        "Answer": "<b>ANSWER:</b> Locks available rows while automatically skipping rows locked by other concurrent workers.<br><br><b>The SQL:</b><br><code>SELECT * FROM job_queue <br>WHERE status = 'PENDING' <br>ORDER BY priority DESC LIMIT 1 <br>FOR UPDATE SKIP LOCKED;</code><br>Allows 100 worker processes to pop jobs simultaneously without waiting on locks or deadlocking!",
        "Topic": "Concurrency & Locking",
        "Tags": "sql concurrency skip_locked queue locks"
    },
    {
        "Question": "How do you optimize `LIKE '%term%'` substring searches in PostgreSQL using Trigram GIN indexes?",
        "Answer": "<b>ANSWER:</b> Install `pg_trgm` and build a GIN index.<br><br><b>The SQL:</b><br><code>CREATE EXTENSION IF NOT EXISTS pg_trgm;</code><br><code>CREATE INDEX idx_products_name_trgm ON products USING gin (name gin_trgm_ops);</code><br>Now wildcard searches like <code>WHERE name ILIKE '%laptop%'</code> execute as an instant index scan instead of a 30-second sequential scan.",
        "Topic": "Query Optimization",
        "Tags": "sql postgres trigram gin wildcard like"
    },
    {
        "Question": "What is Full-Text Search in PostgreSQL and why is it superior to `LIKE '%term%'`?",
        "Answer": "<b>ANSWER:</b> Stemming, stop-word elimination, and inverted index lookups.<br><br><b>The SQL:</b><br><code>SELECT * FROM articles WHERE to_tsvector('english', body) @@ to_tsquery('english', 'database & tuning');</code><br>Matches variations like 'databases', 'tuned', 'tuning' in milliseconds across millions of large documents using a GIN index.",
        "Topic": "Query Optimization",
        "Tags": "sql postgres fts full_text_search gin"
    },
    {
        "Question": "How do you implement Keyset Pagination using a Composite Key `(created_at, id)`?",
        "Answer": "<b>ANSWER:</b> Use tuple comparison syntax.<br><br><b>The SQL:</b><br><code>SELECT * FROM orders <br>WHERE (created_at, id) < (:last_date, :last_id) <br>ORDER BY created_at DESC, id DESC LIMIT 20;</code><br>Ensures stable, deterministic pagination with zero missed rows even if multiple orders share the identical `created_at` timestamp.",
        "Topic": "Query Optimization",
        "Tags": "sql pagination keyset composite performance"
    },
    {
        "Question": "Why should you pass arrays using `= ANY(:ids)` instead of generating `WHERE id IN (1, 2, ... 10000)`?",
        "Answer": "<b>ANSWER:</b> Query parsing overhead and plan cache pollution.<br><br>Generating massive SQL strings with 10,000 literal numbers forces the database parser to allocate megabytes of memory to parse the AST. Passing an array: <code>WHERE id = ANY($1::int[])</code> uses a single static prepared plan with instant execution.",
        "Topic": "Query Optimization",
        "Tags": "sql optimization any array in prepared_statements"
    }
]

with open('decks/sql_tuning_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in batchA:
        writer.writerow(card)

print(f"Batch A complete: appended {len(batchA)} cards.")
