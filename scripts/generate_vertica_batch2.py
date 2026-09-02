import csv

batch2_cards = [
    # --- MODULE 4: INGESTION, ROS & THE TUPLE MOVER ---
    {
        "Question": "What is the difference between `COPY` with and without the `DIRECT` hint?",
        "Answer": "<b>ANSWER:</b> Writing directly to disk (ROS) vs. writing to memory (WOS).<br><br>• <code>COPY ... DIRECT</code>: Bypasses memory buffers and writes bulk data directly to compressed ROS storage containers on disk. Standard for all production batch ETL.<br>• Without `DIRECT`: Historically loaded into in-memory WOS (Write-Optimized Store), requiring Tuple Mover moveout passes later.",
        "Topic": "Data Ingestion",
        "Tags": "vertica ingestion copy direct wos ros"
    },
    {
        "Question": "What is a ROS (Read-Optimized Store) Container?",
        "Answer": "<b>ANSWER:</b> An immutable, compressed, sorted physical collection of column files on disk.<br><br>Every bulk `COPY` or `INSERT` creates one or more new ROS containers. They are read-only once written, and multiple ROS containers are periodically coalesced by the Tuple Mover.",
        "Topic": "Storage Management",
        "Tags": "vertica storage ros containers architecture"
    },
    {
        "Question": "What is the 'ROS Container Sprawl' problem and what error does it produce?",
        "Answer": "<b>ANSWER:</b> Exceeding the maximum allowed ROS containers per projection.<br><br>• <b>Limit:</b> By default, Vertica caps each projection at <b>1024 ROS containers per node</b>.<br>• <b>Error:</b> <code>ERROR: Too many ROS containers</code>.<br>• <b>Cause:</b> Doing thousands of tiny trickle INSERTs or frequent small COPY loads without allowing the Tuple Mover to merge them.",
        "Topic": "Storage Management",
        "Tags": "vertica storage ros sprawl error"
    },
    {
        "Question": "What is the Tuple Mover (TM) in Vertica?",
        "Answer": "<b>ANSWER:</b> The background compaction and maintenance engine.<br><br>It continuously executes two critical background tasks:<br>1. <b>Moveout:</b> Flushes historical data from in-memory WOS to on-disk ROS containers.<br>2. <b>Mergeout:</b> Merges dozens of small fragmented ROS containers into single large, optimized ROS containers.",
        "Topic": "Storage Management",
        "Tags": "vertica tuple_mover moveout mergeout maintenance"
    },
    {
        "Question": "How do you manually force Mergeout on a projection using SQL?",
        "Answer": "<b>ANSWER:</b> Use the `DO_TM_TASK()` function.<br><br><b>The SQL:</b><br><code>SELECT DO_TM_TASK('mergeout', 'my_projection_name');</code><br><br>Manually compacts fragmented ROS containers when preparing tables for high-performance reporting.",
        "Topic": "Storage Management",
        "Tags": "vertica tuple_mover mergeout do_tm_task"
    },
    {
        "Question": "What is the Ancient History Mark (AHM) in Vertica?",
        "Answer": "<b>ANSWER:</b> The epoch boundary before which historical data can be permanently destroyed.<br><br>Queries can use historical queries (`AT EPOCH`) up to the AHM. Transactions prior to AHM are eligible for physical purging from disk during mergeout operations.",
        "Topic": "Storage Management",
        "Tags": "vertica ahm epochs mvcc purge"
    },
    {
        "Question": "Why does running `DELETE FROM my_table` NOT free up any physical disk space immediately?",
        "Answer": "<b>ANSWER:</b> Vertica marks deletions in Deletion Vectors rather than deleting data files.<br><br>Deleted rows remain on disk so queries running in older epochs can still read them. Disk space is ONLY reclaimed when: (1) AHM advances past the delete transaction, and (2) you run `PURGE` or wait for mergeout.",
        "Topic": "Storage Management",
        "Tags": "vertica storage delete purge deletion_vectors"
    },
    {
        "Question": "How do you permanently reclaim disk space from deleted rows in a table?",
        "Answer": "<b>ANSWER:</b> Run `PURGE_TABLE()` after advancing AHM.<br><br><b>The SQL:</b><br><code>SELECT MAKE_AHM_NOW();</code><br><code>SELECT PURGE_TABLE('sales_fact');</code><br><br>Physically removes deleted records and rebuilds ROS containers without dead tuples.",
        "Topic": "Storage Management",
        "Tags": "vertica maintenance purge_table disk_space"
    },
    {
        "Question": "What does `REBALANCE_CLUSTER()` do when a new node is added to an Enterprise cluster?",
        "Answer": "<b>ANSWER:</b> Redistributes segmented projection data across the expanded node cluster.<br><br><b>The SQL:</b><br><code>SELECT REBALANCE_CLUSTER();</code><br><br>Calculates new hash bucket boundaries and streams data blocks to the new node so all nodes share an equal fraction of the total dataset.",
        "Topic": "Cluster Administration",
        "Tags": "vertica administration rebalance_cluster nodes"
    },
    {
        "Question": "What system view tracks ROS container counts, row counts, and delete vectors per projection?",
        "Answer": "<b>ANSWER:</b> `V_MONITOR.STORAGE_CONTAINERS`<br><br><b>The SQL:</b><br><code>SELECT node_name, projection_name, count(*) AS ros_count <br>FROM v_monitor.storage_containers <br>GROUP BY 1, 2 HAVING count(*) > 500;</code><br><br>Primary view for monitoring ROS sprawl before hitting the 1024 limit.",
        "Topic": "System Catalogs",
        "Tags": "vertica catalogs storage_containers ros_count"
    },
    {
        "Question": "What are Current Epoch (CE) and Last Good Epoch (LGE)?",
        "Answer": "<b>ANSWER:</b> Milestones tracking transaction commit state.<br><br>• <b>Current Epoch (CE):</b> The epoch assigned to the current active transaction.<br>• <b>Last Good Epoch (LGE):</b> The most recent epoch for which all participating nodes have confirmed permanent write to disk. Used as the recovery baseline after a crash.",
        "Topic": "Storage Management",
        "Tags": "vertica epochs ce lge recovery"
    },
    {
        "Question": "What is the `AUTOCOMMIT` setting during large batch ETL in Vertica, and why should it be ON?",
        "Answer": "<b>ANSWER:</b> Commit immediately upon statement completion.<br><br>Holding large transactions open without commit holds back the Ancient History Mark (AHM), preventing Tuple Mover mergeout passes and causing massive deletion vector and ROS container accumulation.",
        "Topic": "Data Ingestion",
        "Tags": "vertica ingestion autocommit ahm"
    },

    # --- MODULE 5: HIGH AVAILABILITY & K-SAFETY ---
    {
        "Question": "What is K-Safety in Vertica?",
        "Answer": "<b>ANSWER:</b> The measure of cluster fault tolerance indicating how many simultaneous node failures the cluster can survive.<br><br>• $K=0$: Zero fault tolerance. If 1 node fails, database shuts down.<br>• $K=1$: Survives the failure of any 1 node without downtime.<br>• $K=2$: Survives the failure of any 2 nodes simultaneously.",
        "Topic": "High Availability",
        "Tags": "vertica ha k_safety fault_tolerance"
    },
    {
        "Question": "What is the minimum physical node requirement for a $K=1$ Vertica cluster?",
        "Answer": "<b>ANSWER:</b> 3 physical nodes.<br><br>A 2-node cluster cannot be $K=1$ because if 1 node dies, the remaining node represents only 50% of the cluster, violating the Quorum requirement ($>50\\%$).",
        "Topic": "High Availability",
        "Tags": "vertica ha k_safety quorum nodes"
    },
    {
        "Question": "What is the minimum physical node requirement for a $K=2$ Vertica cluster?",
        "Answer": "<b>ANSWER:</b> 5 physical nodes.<br><br>If 2 nodes fail in a 5-node cluster, 3 nodes remain online, which is $3/5 = 60\\% > 50\\%$, satisfying cluster quorum.",
        "Topic": "High Availability",
        "Tags": "vertica ha k_safety nodes"
    },
    {
        "Question": "What are Buddy Projections in Vertica?",
        "Answer": "<b>ANSWER:</b> Identical projections segmented on the same key but assigned to different buddy nodes.<br><br><b>Naming:</b> `proj_name_b0` (Node 1) and `proj_name_b1` (Node 2).<br>If Node 1 crashes, Node 2 immediately serves the identical data slice from its buddy projection with zero interruption to active queries.",
        "Topic": "High Availability",
        "Tags": "vertica ha buddy_projections redundancy"
    },
    {
        "Question": "Why does Vertica require Cluster Quorum ($>50\\%$ nodes UP) to run?",
        "Answer": "<b>ANSWER:</b> To prevent Split-Brain corruption.<br><br>If a network partition divides a 10-node cluster into two isolated 5-node halves, neither half has quorum ($>5$). Both halves immediately halt, preventing two isolated clusters from accepting diverging writes and corrupting data.",
        "Topic": "High Availability",
        "Tags": "vertica ha quorum split_brain"
    },
    {
        "Question": "What are Fault Groups in Vertica?",
        "Answer": "<b>ANSWER:</b> Logical groupings of nodes sharing physical infrastructure (racks, power supplies, or switches).<br><br>When defined, Vertica ensures Buddy Projections are never placed on nodes within the same fault group, guaranteeing that a power loss to an entire server rack will not take down both buddy copies.",
        "Topic": "High Availability",
        "Tags": "vertica ha fault_groups rack_awareness"
    },
    {
        "Question": "What is a 'Critical Node' in a degraded Vertica cluster?",
        "Answer": "<b>ANSWER:</b> A node holding the ONLY remaining operational copy of a projection segment.<br><br>If Node 1 has already failed, its partner Node 2 becomes a Critical Node. If Node 2 subsequently fails, data loss would occur, so Vertica immediately shuts down the database to protect integrity.",
        "Topic": "High Availability",
        "Tags": "vertica ha critical_node failure"
    },
    {
        "Question": "What two recovery modes does a recovering Vertica node use to catch up?",
        "Answer": "<b>ANSWER:</b> Historical Recovery and Replay (Active) Recovery.<br><br>1. <b>Historical Recovery:</b> Pulls historical data blocks up to the Last Good Epoch from buddy nodes.<br>2. <b>Replay Recovery:</b> Replays transactions executed while historical recovery was running, transitioning the node to the `UP` state.",
        "Topic": "High Availability",
        "Tags": "vertica ha node_recovery lifecycle"
    },
    {
        "Question": "What command checks the current K-Safety value of a Vertica database?",
        "Answer": "<b>ANSWER:</b> Query `DESIGN_KSAFETY` in `V_MONITOR.SYSTEM`.<br><br><b>The SQL:</b><br><code>SELECT current_fault_tolerance, designed_fault_tolerance <br>FROM v_monitor.system;</code>",
        "Topic": "System Catalogs",
        "Tags": "vertica catalogs k_safety v_monitor"
    },

    # --- MODULE 6: WORKLOAD & RESOURCE MANAGEMENT ---
    {
        "Question": "What is a Resource Pool in Vertica?",
        "Answer": "<b>ANSWER:</b> A named container that allocates memory, CPU threads, and concurrency limits to queries.<br><br>Users or roles are assigned to specific pools, preventing a runaway analyst query from consuming 100% of cluster RAM and starving critical production ingestion pipelines.",
        "Topic": "Resource Management",
        "Tags": "vertica resource_pools workload_management memory"
    },
    {
        "Question": "What are the built-in system Resource Pools in Vertica?",
        "Answer": "<b>ANSWER:</b> Predefined pools for database operation.<br><br>• <code>GENERAL</code>: Default pool for user queries if no custom pool is assigned.<br>• <code>SYSQUERY</code>: Dedicated pool for internal catalog queries and system monitoring.<br>• <code>RECOVERY</code>: Memory reserved for recovering downed nodes.<br>• <code>TM</code>: Memory dedicated to Tuple Mover mergeout operations.",
        "Topic": "Resource Management",
        "Tags": "vertica resource_pools system_pools"
    },
    {
        "Question": "Explain the difference between `MEMORYSIZE` and `MAXMEMORYSIZE` in a Resource Pool.",
        "Answer": "<b>ANSWER:</b> Guaranteed memory reservation vs. Hard memory ceiling.<br><br>• <b>`MEMORYSIZE`:</b> Amount of RAM reserved exclusively for this pool. Even when idle, other pools cannot use this memory.<br>• <b>`MAXMEMORYSIZE`:</b> The absolute maximum RAM this pool can ever allocate. If higher than `MEMORYSIZE`, it borrows unreserved memory from the `GENERAL` pool when under load.",
        "Topic": "Resource Management",
        "Tags": "vertica resource_pools memorysize maxmemorysize"
    },
    {
        "Question": "What is `PLANNEDCONCURRENCY` and how does it calculate query memory budget?",
        "Answer": "<b>ANSWER:</b> The expected number of concurrent queries used to size individual query memory.<br><br><b>Formula:</b><br><code>Query Memory Budget = MEMORYSIZE / PLANNEDCONCURRENCY</code><br>If a pool has 40GB RAM and `PLANNEDCONCURRENCY = 4`, each query is assigned 10GB RAM. If set too high, queries receive tiny budgets and spill to disk.",
        "Topic": "Resource Management",
        "Tags": "vertica resource_pools plannedconcurrency tuning"
    },
    {
        "Question": "What is `RUNTIMECAP` in a Resource Pool?",
        "Answer": "<b>ANSWER:</b> A hard query execution timeout limit.<br><br><b>Syntax:</b><br><code>ALTER RESOURCE POOL adhoc_pool RUNTIMECAP '10 minutes';</code><br><br>Any query running in this pool that exceeds 10 minutes is automatically terminated by the engine, preventing runaway cartesian product queries.",
        "Topic": "Resource Management",
        "Tags": "vertica resource_pools runtimecap timeouts"
    },
    {
        "Question": "What is a Cascade Resource Pool (`CASCADE TO pool_name`)?",
        "Answer": "<b>ANSWER:</b> A fallback overflow pool for queued queries.<br><br>If a query cannot execute in the primary pool within `QUEUETIMEOUT` seconds, Vertica automatically cascades the query to execute in a designated secondary pool rather than failing with a queue error.",
        "Topic": "Resource Management",
        "Tags": "vertica resource_pools cascade queueing"
    },
    {
        "Question": "What parameter controls maximum queue wait time before a query errors out in a Resource Pool?",
        "Answer": "<b>ANSWER:</b> `QUEUETIMEOUT`<br><br><b>Setting:</b><br><code>ALTER RESOURCE POOL bi_pool QUEUETIMEOUT 30;</code><br><br>If all concurrency slots are full, queries wait up to 30 seconds in queue. If still unserviced, they fail with an error or cascade to an overflow pool.",
        "Topic": "Resource Management",
        "Tags": "vertica resource_pools queuetimeout"
    },
    {
        "Question": "How do you assign a user or role to a specific Resource Pool?",
        "Answer": "<b>ANSWER:</b> Using `ALTER USER` or `ALTER ROLE`.<br><br><b>The SQL:</b><br><code>ALTER USER etl_service RESOURCE POOL etl_pool;</code><br><code>ALTER ROLE analysts RESOURCE POOL bi_pool;</code>",
        "Topic": "Resource Management",
        "Tags": "vertica resource_pools users roles"
    },
    {
        "Question": "What system view displays real-time memory usage, active queries, and queued queries per Resource Pool?",
        "Answer": "<b>ANSWER:</b> `V_MONITOR.RESOURCE_POOL_STATUS`<br><br><b>The SQL:</b><br><code>SELECT pool_name, memory_size_actual_kb, memory_inuse_kb, <br>       running_query_count, queued_query_count <br>FROM v_monitor.resource_pool_status;</code>",
        "Topic": "System Catalogs",
        "Tags": "vertica catalogs resource_pool_status monitoring"
    }
]

# Append Batch 2 to decks/vertica_deck.csv
with open('decks/vertica_deck.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Question", "Answer", "Topic", "Tags"])
    for card in batch2_cards:
        writer.writerow(card)

print(f"Batch 2 complete: appended {len(batch2_cards)} cards.")
