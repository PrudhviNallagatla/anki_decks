import csv
import os

os.makedirs('decks', exist_ok=True)

batch1_cards = [
    # --- MODULE 1: COLUMNAR STORAGE & PROJECTION ARCHITECTURE ---
    {
        "Question": "What is the core architectural difference between Columnar Storage (Vertica) and Row-Oriented Storage (Postgres/MySQL)?",
        "Answer": "<b>ANSWER:</b> Storing data by column on disk rather than by row.<br><br>• <b>Row-Store:</b> Reads all 50 columns of a row even if the query only needs 2 (wasting 95% of disk I/O).<br>• <b>Column-Store (Vertica):</b> Each column is stored in its own separate set of disk files. If a query selects only `revenue` and `date`, Vertica reads ONLY those two columns off disk, slashing I/O by up to 90%.",
        "Topic": "Columnar Architecture",
        "Tags": "vertica architecture columnar row_store"
    },
    {
        "Question": "Why does Vertica have NO secondary indexes, and what replaces them?",
        "Answer": "<b>ANSWER:</b> Projections ARE the index.<br><br>Traditional databases maintain auxiliary B-Tree index structures that duplicate data and create random I/O overhead. Vertica eliminates indexes entirely by physically storing the actual table data in sorted, compressed collections of columns called <b>Projections</b>.",
        "Topic": "Columnar Architecture",
        "Tags": "vertica projections indexes architecture"
    },
    {
        "Question": "Explain the difference between a Logical Table and a Physical Projection in Vertica.",
        "Answer": "<b>ANSWER:</b> Logical schema definition vs. physical disk storage format.<br><br>• <b>Table (Logical):</b> What developers and SQL queries interact with (standard relational tables, columns, rows). Tables store ZERO bytes of data directly.<br>• <b>Projection (Physical):</b> What actually stores the data on disk, specifying exact column subsets, physical sort order, compression encodings, and node distribution.",
        "Topic": "Columnar Architecture",
        "Tags": "vertica architecture table projection"
    },
    {
        "Question": "What is a Superprojection?",
        "Answer": "<b>ANSWER:</b> A projection that contains EVERY column defined in the logical table.<br><br>Every table in Vertica must have at least one superprojection (or a set of buddy superprojections) to ensure any `SELECT *` query can be fulfilled without missing columns.",
        "Topic": "Columnar Architecture",
        "Tags": "vertica projections superprojection"
    },
    {
        "Question": "What is an Aggregate Projection, and when should you design one?",
        "Answer": "<b>ANSWER:</b> A pre-aggregated physical projection that precomputes summary metrics.<br><br>Instead of scanning 1 billion transaction rows on every query, an aggregate projection pre-calculates sums, averages, and counts grouped by specific dimensions, returning dashboard metrics in milliseconds.",
        "Topic": "Columnar Architecture",
        "Tags": "vertica projections aggregate optimization"
    },
    {
        "Question": "What is Vectorized Query Execution in Vertica?",
        "Answer": "<b>ANSWER:</b> Operating on batches of column values in CPU L1/L2 cache rather than row-by-row.<br><br>Instead of iterating row-by-row through an interpreter loop, Vertica's engine passes contiguous arrays (vectors) of column values directly into modern CPU SIMD registers, achieving near hardware-speed execution.",
        "Topic": "Columnar Architecture",
        "Tags": "vertica execution vectorized simd"
    },
    {
        "Question": "What is Run-Length Encoding (RLE) and when is it optimal in Vertica?",
        "Answer": "<b>ANSWER:</b> Compressing consecutive repeated values into a (value, count) pair.<br><br>• <b>Example:</b> `USA, USA, USA, USA, USA` becomes `(USA, 5)`.<br>• <b>Rule:</b> Optimal ONLY for <b>low-cardinality columns that appear early in the projection sort order</b>. Sorting makes identical values contiguous, yielding massive compression.",
        "Topic": "Column Encodings",
        "Tags": "vertica encoding rle compression"
    },
    {
        "Question": "Why is it catastrophic to apply RLE encoding to high-cardinality or unsorted columns?",
        "Answer": "<b>ANSWER:</b> It actually causes data expansion rather than compression.<br><br>If values do not repeat consecutively, storing a count for every single unique value doubles the storage requirement (`(value, 1)` for every row), degrading both disk footprint and scan performance.",
        "Topic": "Column Encodings",
        "Tags": "vertica encoding rle gotcha"
    },
    {
        "Question": "What are the `DELTAVAL` and `DELTA4BYTE` compression encodings?",
        "Answer": "<b>ANSWER:</b> Storing only the mathematical difference between consecutive values.<br><br>Ideal for monotonically increasing sequences, integer IDs, and timestamps. Instead of storing 8-byte timestamps, Vertica stores small 1- or 2-byte offsets from the previous row.",
        "Topic": "Column Encodings",
        "Tags": "vertica encoding deltaval compression"
    },
    {
        "Question": "What is the `BLOCK_DICT` (Block Dictionary) encoding?",
        "Answer": "<b>ANSWER:</b> Dictionary compression within each data block.<br><br>Stores an array of unique string values once per block, replacing individual row values with compact 1- or 2-byte integer dictionary indexes. Ideal for text columns with moderate cardinality.",
        "Topic": "Column Encodings",
        "Tags": "vertica encoding block_dict strings"
    },
    {
        "Question": "What is `AUTO` encoding in Vertica?",
        "Answer": "<b>ANSWER:</b> Vertica's automated heuristic encoding selection.<br><br>When no explicit encoding is declared, Vertica evaluates column data types during loading and Database Designer passes to select default encodings (e.g. LZO for arbitrary text, AUTO for integers).",
        "Topic": "Column Encodings",
        "Tags": "vertica encoding auto defaults"
    },
    {
        "Question": "How does Vertica evaluate filter predicates on compressed columnar data without decompressing it?",
        "Answer": "<b>ANSWER:</b> Direct execution on encoded bytes.<br><br>For algorithms like RLE, if evaluating `WHERE country = 'USA'`, Vertica checks the dictionary/encoded value directly without decompressing the individual rows, instantly counting matching tuples in CPU cache.",
        "Topic": "Column Encodings",
        "Tags": "vertica execution compression evaluation"
    },
    {
        "Question": "What system view displays all projections, their owners, and whether they are up-to-date?",
        "Answer": "<b>ANSWER:</b> `V_CATALOG.PROJECTIONS`<br><br><b>The SQL:</b><br><code>SELECT projection_name, anchor_table_name, is_up_to_date, is_segmented <br>FROM v_catalog.projections;</code><br><br>If `is_up_to_date = false`, the projection is not yet safe for the query planner to use.",
        "Topic": "System Catalogs",
        "Tags": "vertica catalogs projections v_catalog"
    },
    {
        "Question": "How does Vertica implement Multi-Version Concurrency Control (MVCC) without Rollback/Undo segments?",
        "Answer": "<b>ANSWER:</b> Using Epochs and Deletion Vectors.<br><br>Every transaction is assigned a monotonically increasing Epoch number. Inserted tuples record their creation epoch; deleted tuples are recorded in a separate deletion vector with the deletion epoch. No rollback segments or table locking required.",
        "Topic": "Columnar Architecture",
        "Tags": "vertica architecture mvcc epochs"
    },

    # --- MODULE 2: SEGMENTATION & SORT ORDER (THE 100X SPEED KNOBS) ---
    {
        "Question": "What is Hash Segmentation (`SEGMENTED BY HASH(...) ALL NODES`) in Vertica?",
        "Answer": "<b>ANSWER:</b> Distributing rows evenly across all cluster nodes based on a hash of specific key columns.<br><br><b>The SQL:</b><br><code>CREATE PROJECTION sales_proj AS SELECT * FROM sales <br>SEGMENTED BY HASH(order_id) ALL NODES;</code><br><br>Used for massive fact tables to distribute storage and parallelize CPU/disk workload across all nodes equally.",
        "Topic": "Projection Design",
        "Tags": "vertica segmentation hash mpp"
    },
    {
        "Question": "What is Unsegmented Replication (`UNSEGMENTED ALL NODES`) and when should you use it?",
        "Answer": "<b>ANSWER:</b> Duplicating an exact copy of the table on EVERY node in the cluster.<br><br><b>The SQL:</b><br><code>CREATE PROJECTION dim_store_proj AS SELECT * FROM dim_store <br>UNSEGMENTED ALL NODES;</code><br><br><b>Rule:</b> Essential for small-to-medium dimension tables (under 5M rows). Ensures every node can perform joins locally with zero network data transfer.",
        "Topic": "Projection Design",
        "Tags": "vertica segmentation unsegmented replication"
    },
    {
        "Question": "What is Data Skew in Vertica, and how do you prevent it?",
        "Answer": "<b>ANSWER:</b> Uneven row distribution where one node holds vastly more data than others.<br><br>• <b>Cause:</b> Choosing a segmentation column with poor cardinality (e.g. `gender` or `status`).<br>• <b>Prevention:</b> Always segment on high-cardinality, uniformly distributed columns (e.g., `customer_id`, UUID, primary keys). Check with <code>SELECT node_name, count(*) FROM projection_name GROUP BY 1;</code>.",
        "Topic": "Projection Design",
        "Tags": "vertica segmentation data_skew tuning"
    },
    {
        "Question": "Why does segmenting two tables on their join key produce 100x faster joins?",
        "Answer": "<b>ANSWER:</b> It produces a Local Co-located Join with ZERO network data redistribution.<br><br>If `Orders` and `Order_Items` are both segmented on `order_id`, row pairs with matching IDs reside on the exact same physical node. Vertica joins them in local memory without transmitting gigabytes of data across the network.",
        "Topic": "Projection Design",
        "Tags": "vertica segmentation joins performance"
    },
    {
        "Question": "What are the two major performance benefits of Projection Sort Order (`ORDER BY`)?",
        "Answer": "<b>ANSWER:</b> Merge Joins and Pipelined Aggregations.<br><br>1. <b>Merge Joins:</b> If inputs are pre-sorted on join keys, Vertica executes a streaming Merge Join (zero memory overhead, instant execution).<br>2. <b>Pipelined Group-By:</b> If data is pre-sorted on `GROUP BY` columns, Vertica streams aggregation results immediately without in-memory hash tables.",
        "Topic": "Projection Design",
        "Tags": "vertica sort_order merge_join pipelined_groupby"
    },
    {
        "Question": "What is the general Rule of Thumb for ordering columns in a Projection's `ORDER BY` clause?",
        "Answer": "<b>ANSWER:</b> Order from Lowest Cardinality to Highest Cardinality.<br><br><b>Example:</b> `ORDER BY country, region, department, employee_id`.<br>Putting low-cardinality columns first maximizes consecutive repeated values, enabling extreme RLE compression and efficient index-like block skipping.",
        "Topic": "Projection Design",
        "Tags": "vertica sort_order cardinality rle"
    },
    {
        "Question": "Can a single logical table have multiple projections with different sort orders?",
        "Answer": "<b>ANSWER:</b> Yes, and this is a core Vertica best practice.<br><br>• Projection 1 sorted by `(customer_id, date)` accelerates customer lookup queries.<br>• Projection 2 sorted by `(date, product_id)` accelerates financial date-range reporting.<br>Vertica's query optimizer automatically picks the projection with the lowest cost for each query.",
        "Topic": "Projection Design",
        "Tags": "vertica projections optimizer best_practice"
    },
    {
        "Question": "What command makes newly created projections active and populated with table data?",
        "Answer": "<b>ANSWER:</b> `START_REFRESH()`<br><br><b>The SQL:</b><br><code>SELECT START_REFRESH();</code><br><br>Builds new projections in the background from existing table data. Queries continue running against old projections until refresh completes.",
        "Topic": "Projection Design",
        "Tags": "vertica projections start_refresh maintenance"
    },
    {
        "Question": "What is `MAKE_AHM_NOW()` used for in Vertica administration?",
        "Answer": "<b>ANSWER:</b> Forces the Ancient History Mark (AHM) to advance to the latest safe epoch.<br><br><b>The SQL:</b><br><code>SELECT MAKE_AHM_NOW();</code><br><br>Advancing AHM allows deleted rows to be permanently purged from disk via `PURGE`, freeing storage and unblocking background mergeout operations.",
        "Topic": "Storage Management",
        "Tags": "vertica ahm purge epochs"
    },
    {
        "Question": "How do you check if data is evenly segmented across all cluster nodes?",
        "Answer": "<b>ANSWER:</b> Query `V_MONITOR.PROJECTION_STORAGE`.<br><br><b>The SQL:</b><br><code>SELECT node_name, projection_name, row_count, used_bytes <br>FROM v_monitor.projection_storage <br>WHERE anchor_table_name = 'sales';</code><br><br>Identifies skew where individual nodes hold disproportionate row counts or bytes.",
        "Topic": "System Catalogs",
        "Tags": "vertica catalogs storage data_skew"
    },
    {
        "Question": "What is a Projection Baseline Query in Vertica?",
        "Answer": "<b>ANSWER:</b> The query that defines which columns are pulled from the anchor table.<br><br><b>Syntax:</b><br><code>CREATE PROJECTION emp_proj AS SELECT id, name, salary FROM emp ...</code><br>The `SELECT` clause represents the baseline query defining the projection's physical contents.",
        "Topic": "Projection Design",
        "Tags": "vertica projections syntax"
    },
    {
        "Question": "What happens if a query joins on columns where neither projection is segmented or sorted by the join key?",
        "Answer": "<b>ANSWER:</b> Vertica is forced to perform a Dynamic Resegment Join.<br><br>The query planner must dynamically hash and transmit millions of rows across the network between nodes at runtime, causing heavy network traffic and spilling to temporary disk space.",
        "Topic": "Query Tuning",
        "Tags": "vertica tuning resegment network"
    },

    # --- MODULE 3: EON MODE VS. ENTERPRISE MODE ARCHITECTURE ---
    {
        "Question": "Explain the architectural difference between Vertica Enterprise Mode and Eon Mode.",
        "Answer": "<b>ANSWER:</b> Shared-Nothing vs. Separation of Compute and Storage.<br><br>• <b>Enterprise Mode:</b> Local disk on each physical node holds the primary data. Adding storage requires adding compute nodes.<br>• <b>Eon Mode:</b> Communal Cloud Object Storage (S3, GCS, Azure Blob, MinIO) holds all primary data. Compute nodes act as stateless execution workers with local caching (Depots).",
        "Topic": "Eon Mode Architecture",
        "Tags": "vertica eon_mode enterprise_mode architecture"
    },
    {
        "Question": "What is Communal Storage in Vertica Eon Mode?",
        "Answer": "<b>ANSWER:</b> The single centralized, highly durable cloud object storage repository.<br><br>All ROS data containers, transaction logs, and metadata are permanently persisted here. Because storage is external, any compute node can crash or be terminated without risk of data loss.",
        "Topic": "Eon Mode Architecture",
        "Tags": "vertica eon_mode communal_storage s3"
    },
    {
        "Question": "What is a 'Depot' in Vertica Eon Mode?",
        "Answer": "<b>ANSWER:</b> A high-speed local disk cache (NVMe/SSD) residing on each compute node.<br><br>Caches frequently accessed data blocks locally from Communal Storage. When queries run, they read from the fast local Depot rather than incurring slow cloud network latency.",
        "Topic": "Eon Mode Architecture",
        "Tags": "vertica eon_mode depot cache"
    },
    {
        "Question": "How does Depot Eviction work when the local depot disk fills up?",
        "Answer": "<b>ANSWER:</b> Least Recently Used (LRU) eviction algorithm.<br><br>When free space drops below threshold, Vertica evicts unpinned, cold data blocks to make room for newly requested blocks. Critical tables can be pinned to prevent eviction via <code>ALTER TABLE ... SET DEPOT PIN;</code>.",
        "Topic": "Eon Mode Architecture",
        "Tags": "vertica eon_mode depot eviction lru"
    },
    {
        "Question": "What is 'Depot Warming' in Vertica Eon Mode?",
        "Answer": "<b>ANSWER:</b> Proactively pre-loading data blocks from Communal Storage into the local Depot.<br><br>Used when spinning up new subclusters or after scaling compute, ensuring initial analytical queries experience warm cache speeds without waiting for lazy read misses.",
        "Topic": "Eon Mode Architecture",
        "Tags": "vertica eon_mode depot warming performance"
    },
    {
        "Question": "What are Subclusters in Eon Mode and why are they revolutionary for workload isolation?",
        "Answer": "<b>ANSWER:</b> Independent groups of compute nodes operating on the same communal data.<br><br><b>Architecture:</b><br>• <b>ETL Subcluster (3 nodes):</b> Runs heavy continuous batch data loading.<br>• <b>BI Subcluster (6 nodes):</b> Runs executive dashboards and user queries.<br>Zero CPU or memory contention between ETL and analytics!",
        "Topic": "Eon Mode Architecture",
        "Tags": "vertica eon_mode subclusters workload_isolation"
    },
    {
        "Question": "What is the difference between a Primary Subcluster and a Secondary Subcluster in Eon Mode?",
        "Answer": "<b>ANSWER:</b> Quorum participation and state control.<br><br>• <b>Primary Subcluster:</b> Participates in cluster quorum and cluster state decisions. Required to keep database online.<br>• <b>Secondary Subcluster:</b> Pure compute workers. Can be dynamically scaled to 0 nodes during off-hours to save cloud infrastructure cost without affecting database availability.",
        "Topic": "Eon Mode Architecture",
        "Tags": "vertica eon_mode subclusters primary secondary"
    },
    {
        "Question": "What is a Shard in Vertica Eon Mode, and how does Shard Subscription work?",
        "Answer": "<b>ANSWER:</b> Fixed logical partitions of the total communal dataset.<br><br>The communal dataset is divided into a fixed count of Shards (e.g. 12 or 24). When nodes join a subcluster, Vertica assigns them as <b>Primary Subscribers</b> for specific shards. Each node is responsible for caching and processing its subscribed shards.",
        "Topic": "Eon Mode Architecture",
        "Tags": "vertica eon_mode shards subscriptions"
    },
    {
        "Question": "How does Eon Mode scale compute up or down dynamically?",
        "Answer": "<b>ANSWER:</b> Adding or terminating nodes without physical data movement.<br><br>In Enterprise Mode, adding nodes requires hours of cluster rebalancing (`rebalance_cluster`). In Eon Mode, new nodes attach to communal storage in seconds and immediately begin processing queries using subclusters.",
        "Topic": "Eon Mode Architecture",
        "Tags": "vertica eon_mode scaling elasticity"
    },
    {
        "Question": "What is the `ALTER SUBCLUSTER ... RESIZE` command in Eon Mode?",
        "Answer": "<b>ANSWER:</b> Dynamically scaling the number of active compute nodes in a subcluster.<br><br><b>Syntax:</b><br><code>ALTER SUBCLUSTER bi_subcluster RESIZE 12;</code><br><br>Instantly scales the compute tier to handle peak query traffic and scales back down during off-peak hours.",
        "Topic": "Eon Mode Architecture",
        "Tags": "vertica eon_mode subclusters scaling"
    },
    {
        "Question": "What system view displays Depot sizing, hit ratios, and free space per node?",
        "Answer": "<b>ANSWER:</b> `V_MONITOR.DEPOT_SIZES` and `V_MONITOR.DEPOT_STATUS`<br><br><b>The SQL:</b><br><code>SELECT node_name, total_size_bytes, used_size_bytes, free_size_bytes <br>FROM v_monitor.depot_sizes;</code><br><br>Monitors cache utilization to detect whether depot sizing is adequate for working data sets.",
        "Topic": "System Catalogs",
        "Tags": "vertica catalogs depot monitoring"
    },
    {
        "Question": "Can an existing Vertica Enterprise Mode database be migrated to Eon Mode?",
        "Answer": "<b>ANSWER:</b> Yes, using the Vertica replication/migration utility.<br><br>You spin up an Eon Mode cluster and replicate data from Enterprise Mode to Eon Mode using <code>vbr --task replicate</code>, copying data directly into Communal Storage.",
        "Topic": "Eon Mode Architecture",
        "Tags": "vertica eon_mode migration enterprise_mode"
    }
]

# Write to decks/vertica_deck.csv
with open('decks/vertica_deck.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    writer.writeheader()
    for card in batch1_cards:
        writer.writerow(card)

print(f"Batch 1 complete: wrote {len(batch1_cards)} cards to decks/vertica_deck.csv.")
