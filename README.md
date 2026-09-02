# Anki CS & IT Mastery Decks

A comprehensive, production-grade collection of Anki flashcard decks covering Computer Science, Database Administration, Systems Engineering, and Analytics.

---

## 📁 Repository Structure

```
anki_cs_it_decks/
├── decks/                   # Raw CSV source decks (editable)
│   ├── linux_mastery_deck.csv
│   ├── dba_fresher_deck.csv
│   ├── sql_tuning_deck.csv
│   ├── edb_postgres_deck.csv
│   ├── vertica_deck.csv
│   ├── fundamental_analyst_deck.csv
│   ├── fundamentals_dbms.csv
│   ├── fundamentals_dsa.csv
│   ├── fundamentals_excel.csv
│   ├── fundamentals_networking.csv
│   ├── fundamentals_oops.csv
│   ├── fundamentals_os.csv
│   └── fundamentals_system_design.csv
├── packages/                # Compiled Anki .apkg packages (ready to import)
│   ├── Linux_Mastery.apkg
│   ├── DBA_Fresher_Mastery.apkg
│   ├── SQL_Optimization_Mastery.apkg
│   ├── EDB_Postgres_Mastery.apkg
│   ├── Vertica_Mastery.apkg
│   ├── Analyst_Mastery.apkg
│   ├── DBMS_Excel_Mastery.apkg
│   ├── DSA_Mastery.apkg
│   ├── Networking_OOPs_Mastery.apkg
│   └── OS_SysDesign_Mastery.apkg
├── sources/                 # Original reference documentation & course PDFs
│   ├── edb_postgres/        # EDB v17 Essentials, Advanced & Answer Key PDFs
│   └── vertica/             # Vertica Complete Reference Documentation
├── scripts/                 # Individual builders & PDF extraction tools
│   ├── build_edb_apkg.py
│   ├── build_analyst_apkg.py
│   ├── build_apkg.py
│   └── scratch_cache/       # Cached text extractions
├── build.py                 # Master build tool (builds all or single decks)
└── README.md
```

---

## 🎴 Deck Catalog

| Deck Name | Package File (`packages/`) | Source CSV (`decks/`) | Card Count | Key Domains |
| :--- | :--- | :--- | :---: | :--- |
| **Linux Mastery** | `Linux_Mastery.apkg` | `linux_mastery_deck.csv` | **185** | Practical CLI, Deep Search, Systemd, Bash Scripting strict mode, SSH Tunnels, Git CLI, Triage (`vmstat`/`iostat`/`lsof`), Storage, LVM & Kernel Tuning |
| **DBA Fresher Foundations** | `DBA_Fresher_Mastery.apkg` | `dba_fresher_deck.csv` | **120** | Engine Internals (8KB pages, Shared Buffers, WAL, Checkpoints), ACID, Lock trees, Outage Playbooks, Extensions (`pg_stat_statements`/`pg_repack`), Replication |
| **SQL & Query Optimization** | `SQL_Optimization_Mastery.apkg` | `sql_tuning_deck.csv` | **170** | Window Functions, Recursive CTEs, LeetCode Hard Patterns, Joins/Anti-Patterns, JSONB Path, SARGability, EXPLAIN Forensics, Index Tuning |
| **EDB Postgres Mastery** | `EDB_Postgres_Mastery.apkg` | `edb_postgres_deck.csv` | **250** | Architecture, Memory Sizing, TDE, PEM, HA, PITR, HOT Updates, `pg_upgrade --link`, EDB SPL & Security |
| **Vertica 80/20 Mastery** | `Vertica_Mastery.apkg` | `vertica_deck.csv` | **120** | Columnar Architecture, Projections, Hash vs Unsegmented, Eon Mode & Depots, Tuple Mover, K-Safety, Resource Pools |
| **Data Analyst Mastery** | `Analyst_Mastery.apkg` | `fundamental_analyst_deck.csv` | **140** | PostgreSQL for Analytics, Python Core, ML Validation, Dialect Differences |
| **DSA Mastery** | `DSA_Mastery.apkg` | `fundamentals_dsa.csv` | **55** | Core Data Structures, Two-Pointers, Sliding Window, Monotonic Stacks, DP |
| **DBMS & Excel Mastery** | `DBMS_Excel_Mastery.apkg` | `fundamentals_dbms.csv`<br>`fundamentals_excel.csv` | **117** | Relational Theory, ACID, Normalization, SQL Joins, Excel Formulas & Lookups |
| **Networking & OOPs Mastery** | `Networking_OOPs_Mastery.apkg` | `fundamentals_networking.csv`<br>`fundamentals_oops.csv` | **120** | TCP/IP, DNS, HTTP/S, Subnetting, Polymorphism, Design Patterns, SOLID |
| **OS & System Design Mastery** | `OS_SysDesign_Mastery.apkg` | `fundamentals_os.csv`<br>`fundamentals_system_design.csv` | **120** | Linux Kernel, Process Scheduling, Virtual Memory, CAP Theorem, Sharding, Caches |

**Total Cards Across All Decks:** **1,397 Cards** (Golden Trio: **475 Cards**)

---

## 🚀 Building the Decks

Use the master `build.py` script to compile any or all decks into `.apkg` files:

### Build All Decks
```bash
python build.py
```

### Build a Specific Deck
```bash
python build.py linux         # Builds Linux Mastery (185 cards)
python build.py dba_fresher   # Builds DBA Fresher Foundations (120 cards)
python build.py sql_tuning    # Builds SQL & Query Optimization Mastery (170 cards)
python build.py edb           # Builds EDB Postgres Mastery (250 cards)
python build.py vertica       # Builds Vertica 80/20 Mastery (120 cards)
python build.py analyst       # Builds Data Analyst Mastery
python build.py dsa           # Builds DSA Mastery
python build.py dbms_excel    # Builds DBMS & Excel Mastery
python build.py networking_oops # Builds Networking & OOPs
python build.py os_sysdesign  # Builds OS & System Design
```

### List Available Deck Targets
```bash
python build.py list
```

---

## 📲 How to Import into Anki

1. Open **Anki** on your desktop or mobile device.
2. Go to **File** -> **Import...** (or double-click any `.apkg` file in `packages/`).
3. Select any `.apkg` file inside the `packages/` directory.
4. Cards are automatically styled with modern typography, dark code blocks, and topic tags.
