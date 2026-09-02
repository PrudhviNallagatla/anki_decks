import csv

batchB = [
    # --- DEEP POSTGRESQL JSONB & ARRAY MASTERY ---
    {
        "Question": "What is `jsonb_path_query()` in PostgreSQL 12+?",
        "Answer": "<b>ANSWER:</b> Executes SQL/JSON path language expressions across nested JSON documents.<br><br><b>The SQL:</b><br><code>SELECT jsonb_path_query(payload, '$.items[*] ? (@.price > 100).name') <br>FROM invoices;</code><br>Directly extracts matching inner element properties without unnesting or writing complex nested loops.",
        "Topic": "JSONB Mastery",
        "Tags": "sql postgres jsonb json_path query"
    },
    {
        "Question": "How do you navigate deeply nested JSONB paths using the `#>` and `#>>` operators?",
        "Answer": "<b>ANSWER:</b> Path array extraction operators.<br><br>• <code>payload #> '{user, address, city}'</code>: Extracts the nested JSON object.<br>• <code>payload #>> '{user, address, city}'</code>: Extracts the final nested value as plain `TEXT`.",
        "Topic": "JSONB Mastery",
        "Tags": "sql postgres jsonb path operators"
    },
    {
        "Question": "What do the `?`, `?|`, and `?&` operators do in PostgreSQL JSONB?",
        "Answer": "<b>ANSWER:</b> Key existence check operators.<br><br>• <code>data ? 'email'</code>: Checks if key 'email' exists.<br>• <code>data ?| array['mobile', 'landline']</code>: Checks if ANY of the keys exist (OR).<br>• <code>data ?& array['first_name', 'last_name']</code>: Checks if ALL keys exist (AND).",
        "Topic": "JSONB Mastery",
        "Tags": "sql postgres jsonb key_existence operators"
    },
    {
        "Question": "How do you update a deeply nested attribute inside a JSONB column using `jsonb_set()`?",
        "Answer": "<b>ANSWER:</b> Use `jsonb_set(target, path, new_value, create_missing)`.<br><br><b>The SQL:</b><br><code>UPDATE profiles <br>SET settings = jsonb_set(settings, '{notifications, email}', 'false'::jsonb, true) <br>WHERE user_id = 101;</code>",
        "Topic": "JSONB Mastery",
        "Tags": "sql postgres jsonb jsonb_set update"
    },
    {
        "Question": "How do you delete a specific key from a JSONB document in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Use the `-` operator.<br><br><b>The SQL:</b><br><code>UPDATE users SET profile = profile - 'temporary_password';</code><br>Or delete deep nested keys with `# -`: <code>UPDATE users SET profile = profile #- '{metadata, session_id}';</code>.",
        "Topic": "JSONB Mastery",
        "Tags": "sql postgres jsonb delete_key operators"
    },
    {
        "Question": "How do you merge two JSONB objects together in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Use the `||` concatenation operator.<br><br><b>The SQL:</b><br><code>SELECT '{\"a\": 1, \"b\": 2}'::jsonb || '{\"b\": 99, \"c\": 3}'::jsonb;</code><br>Returns: `{\"a\": 1, \"b\": 99, \"c\": 3}` (keys in the right object overwrite keys in the left).",
        "Topic": "JSONB Mastery",
        "Tags": "sql postgres jsonb merge concatenation"
    },
    {
        "Question": "What is the difference between `jsonb_ops` and `jsonb_path_ops` GIN indexes?",
        "Answer": "<b>ANSWER:</b> Flexibility vs. Storage size and speed.<br><br>• <b>`jsonb_ops` (Default):</b> Indexes every key, value, and path. Supports `?`, `?|`, `?&`, and `@>`. Larger index.<br>• <b>`jsonb_path_ops`:</b> Indexes only complete key-value hashes. Supports ONLY `@>`. Takes up to 70% less disk space and executes containment queries faster.",
        "Topic": "JSONB Mastery",
        "Tags": "sql postgres jsonb gin jsonb_path_ops indexes"
    },
    {
        "Question": "How do you convert relational query rows into a structured JSON array of objects?",
        "Answer": "<b>ANSWER:</b> Combine `jsonb_agg()` and `jsonb_build_object()`.<br><br><b>The SQL:</b><br><code>SELECT c.id, c.name, <br>       jsonb_agg(jsonb_build_object('order_id', o.id, 'amount', o.total)) AS orders <br>FROM customers c <br>JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.name;</code>",
        "Topic": "JSONB Mastery",
        "Tags": "sql postgres jsonb jsonb_agg jsonb_build_object"
    },
    {
        "Question": "How do you explode a JSON array of objects into standard relational columns?",
        "Answer": "<b>ANSWER:</b> Use `jsonb_to_recordset()`.<br><br><b>The SQL:</b><br><code>SELECT item_id, price <br>FROM jsonb_to_recordset('[{\"item_id\": 101, \"price\": 19.99}, {\"item_id\": 102, \"price\": 5.50}]') <br>AS x(item_id INT, price NUMERIC);</code>",
        "Topic": "JSONB Mastery",
        "Tags": "sql postgres jsonb jsonb_to_recordset relational"
    },
    {
        "Question": "What is the `&&` overlap operator in PostgreSQL arrays?",
        "Answer": "<b>ANSWER:</b> Checks whether two arrays share any common elements.<br><br><b>The SQL:</b><br><code>SELECT * FROM articles <br>WHERE tags && ARRAY['database', 'sql', 'performance'];</code><br>Returns `TRUE` if the article has at least one matching tag. Can be accelerated with a standard GIN index.",
        "Topic": "Array Mastery",
        "Tags": "sql postgres arrays overlap operators gin"
    },
    {
        "Question": "How do you check the number of elements in a PostgreSQL array?",
        "Answer": "<b>ANSWER:</b> Use `cardinality(array_column)`.<br><br><b>Example:</b><br><code>SELECT user_id, cardinality(roles) AS role_count <br>FROM user_accounts;</code><br>(Cleaner and faster than legacy `array_length(roles, 1)` which returns NULL on empty `ARRAY[]`).",
        "Topic": "Array Mastery",
        "Tags": "sql postgres arrays cardinality length"
    },
    {
        "Question": "How do you format integer IDs with leading zeros (e.g. `000042`) in SQL?",
        "Answer": "<b>ANSWER:</b> Use `LPAD()`.<br><br><b>The SQL:</b><br><code>SELECT LPAD(id::text, 6, '0') AS invoice_code <br>FROM invoices;</code><br>Prepends '0' until total length equals 6 characters.",
        "Topic": "String Manipulation",
        "Tags": "sql strings lpad formatting"
    },
    {
        "Question": "How do you extract a clean numeric phone number from dirty text using `REGEXP_REPLACE`?",
        "Answer": "<b>ANSWER:</b> Strip all non-digit characters with `[^0-9]`.<br><br><b>The SQL:</b><br><code>SELECT REGEXP_REPLACE('+1 (555) 123-4567', '[^0-9]', '', 'g') AS clean_phone;</code><br>Returns: `'15551234567'`.",
        "Topic": "String Manipulation",
        "Tags": "sql strings regex regexp_replace cleaning"
    },
    {
        "Question": "What is `BOOL_AND()` and `BOOL_OR()` in PostgreSQL?",
        "Answer": "<b>ANSWER:</b> Aggregate functions for boolean columns.<br><br>• <b>`BOOL_AND(passed)`:</b> Returns `TRUE` only if ALL rows in the group are true (equivalent to boolean AND).<br>• <b>`BOOL_OR(passed)`:</b> Returns `TRUE` if AT LEAST ONE row in the group is true (equivalent to boolean OR).",
        "Topic": "Analytical SQL",
        "Tags": "sql postgres bool_and bool_or aggregation"
    },
    {
        "Question": "What is an Exclusion Constraint (`EXCLUDE USING gist`) and how does it prevent double bookings?",
        "Answer": "<b>ANSWER:</b> A constraint that prevents overlapping ranges across rows sharing a key.<br><br><b>The SQL:</b><br><code>CREATE TABLE hotel_reservations ( <br>    room_id INT, <br>    stay_dates DATERANGE, <br>    EXCLUDE USING gist (room_id WITH =, stay_dates WITH &&) <br>);</code><br>Postgres rejects any insert where the same room has overlapping dates (`&&`) at the database engine level with zero race conditions!",
        "Topic": "Advanced DDL",
        "Tags": "sql postgres constraints exclude gist daterange"
    }
]

with open('decks/sql_tuning_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in batchB:
        writer.writerow(card)

print(f"Batch B complete: appended {len(batchB)} cards.")
