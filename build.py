#!/usr/bin/env python3
"""
Master Anki APKG Build System for CS & IT Mastery Decks.
Builds all CSV decks in decks/ into ready-to-import Anki .apkg packages in packages/.
"""

import os
import csv
import sys
import genanki

DECKS_DIR = "decks"
PACKAGES_DIR = "packages"

os.makedirs(PACKAGES_DIR, exist_ok=True)

# Common Modern Card Styling
STANDARD_CSS = '''
.card {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 18px;
    text-align: left;
    color: #1e293b;
    background-color: #ffffff;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    max-width: 680px;
    margin: 0 auto;
}
code {
    background-color: #f1f5f9;
    color: #0f172a;
    padding: 3px 6px;
    border-radius: 6px;
    font-family: Consolas, "Courier New", monospace;
    font-size: 15px;
    display: inline-block;
    margin: 4px 0;
    border: 1px solid #cbd5e1;
}
b {
    color: #0284c7;
}
ul, ol {
    padding-left: 20px;
}
li {
    margin-bottom: 6px;
}
'''

def create_model(model_id, name, has_card_type=False):
    fields = [
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'Topic'},
        {'name': 'Tags'}
    ]
    if has_card_type:
        fields.append({'name': 'CardType'})

    type_html = '<br><span style="font-size: 12px; color: #94a3b8;">Type: {{CardType}}</span>' if has_card_type else ''

    qfmt = f'''
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 22px; text-align: center; color: #0f172a; margin-bottom: 20px; font-weight: 600; line-height: 1.4;">
          {{{{Question}}}}
        </div>
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 13px; text-align: center; color: #64748b; text-transform: uppercase; letter-spacing: 1px;">
          <b>{{{{Topic}}}}</b>{type_html}
        </div>
    '''
    afmt = '''
        {{FrontSide}}
        <hr id="answer" style="border: 0; height: 1px; background: #e2e8f0; margin: 20px 0;">
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 17px; text-align: left; color: #334155; line-height: 1.6;">
          {{Answer}}
        </div>
    '''

    return genanki.Model(
        model_id,
        name,
        fields=fields,
        templates=[{'name': 'Card 1', 'qfmt': qfmt, 'afmt': afmt}],
        css=STANDARD_CSS
    )

def add_csv_to_deck(deck, model, csv_filename, has_card_type=False):
    path = os.path.join(DECKS_DIR, csv_filename)
    if not os.path.exists(path):
        print(f"  [!] Warning: CSV file not found: {path}")
        return 0

    with open(path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        count = 0
        for row in reader:
            if len(row) < 2:
                continue
            question = row[0]
            answer = row[1]
            topic = row[2] if len(row) > 2 else ""
            tags_str = row[3] if len(row) > 3 else ""
            tags = [t.strip() for t in tags_str.split(" ") if t.strip()]

            fields = [question, answer, topic, tags_str]
            if has_card_type:
                ctype = row[4] if len(row) > 4 else ""
                fields.append(ctype)

            note = genanki.Note(model=model, fields=fields, tags=tags)
            deck.add_note(note)
            count += 1
    return count

DECK_CONFIGS = {
    'linux': {
        'id': 2059400120,
        'name': 'Linux Mastery',
        'output': 'Linux_Mastery.apkg',
        'model_id': 1607392328,
        'model_name': 'Linux Mastery Model',
        'files': [('linux_mastery_deck.csv', False)],
        'desc': 'Practical CLI, Systemd, Bash Scripting, SSH Tunnels, Git CLI & Performance Triage (185 Cards)'
    },
    'vertica': {
        'id': 2059400118,
        'name': 'Vertica 80/20 Mastery',
        'output': 'Vertica_Mastery.apkg',
        'model_id': 1607392326,
        'model_name': 'Vertica Model',
        'files': [('vertica_deck.csv', False)],
        'desc': 'Core Architecture, Projections, Eon Mode, & Admin (120 Cards)'
    },
    'edb': {
        'id': 2059400116,
        'name': 'EDB Postgres Mastery',
        'output': 'EDB_Postgres_Mastery.apkg',
        'model_id': 1607392321,
        'model_name': 'EDB Postgres Model',
        'files': [('edb_postgres_deck.csv', False)],
        'desc': 'Complete EDB & PostgreSQL DBA Mastery (250 Cards)'
    },
    'dba_fresher': {
        'id': 2059400117,
        'name': 'DBA Fresher Foundations',
        'output': 'DBA_Fresher_Mastery.apkg',
        'model_id': 1607392322,
        'model_name': 'DBA Fresher Model',
        'files': [('dba_fresher_deck.csv', False)],
        'desc': 'PostgreSQL & RDBMS Junior DBA Foundations, Outages, Extensions & Playbook (120 Cards)'
    },
    'sql_tuning': {
        'id': 2059400119,
        'name': 'SQL & Query Optimization Mastery',
        'output': 'SQL_Optimization_Mastery.apkg',
        'model_id': 1607392327,
        'model_name': 'SQL Optimization Model',
        'files': [('sql_tuning_deck.csv', False)],
        'desc': 'Advanced Window Functions, CTEs, SARGability, JSONB, LeetCode Hard & EXPLAIN Forensics (170 Cards)'
    },
    'analyst': {
        'id': 2059400115,
        'name': 'Data Analyst Mastery',
        'output': 'Analyst_Mastery.apkg',
        'model_id': 1607392320,
        'model_name': 'Data Analyst Model',
        'files': [('fundamental_analyst_deck.csv', True)],
        'desc': 'SQL, Python, ML, and Data Analysis for Analysts'
    },
    'dsa': {
        'id': 2059400110,
        'name': 'DSA Mastery',
        'output': 'DSA_Mastery.apkg',
        'model_id': 1607392319,
        'model_name': 'DSA Model',
        'files': [('fundamentals_dsa.csv', False)],
        'desc': 'Data Structures & Algorithms Patterns'
    },
    'dbms_excel': {
        'id': 2059400111,
        'name': 'DBMS & Excel Mastery',
        'output': 'DBMS_Excel_Mastery.apkg',
        'model_id': 1607392323,
        'model_name': 'DBMS Excel Model',
        'files': [('fundamentals_dbms.csv', False), ('fundamentals_excel.csv', False)],
        'desc': 'Relational Database Fundamentals & Excel Formulas'
    },
    'networking_oops': {
        'id': 2059400112,
        'name': 'Networking & OOPs Mastery',
        'output': 'Networking_OOPs_Mastery.apkg',
        'model_id': 1607392324,
        'model_name': 'Networking OOPs Model',
        'files': [('fundamentals_networking.csv', False), ('fundamentals_oops.csv', False)],
        'desc': 'Networking Protocols & Object-Oriented Design'
    },
    'os_sysdesign': {
        'id': 2059400113,
        'name': 'OS & System Design Mastery',
        'output': 'OS_SysDesign_Mastery.apkg',
        'model_id': 1607392325,
        'model_name': 'OS System Design Model',
        'files': [('fundamentals_os.csv', False), ('fundamentals_system_design.csv', False)],
        'desc': 'Operating Systems Internals & Distributed System Design'
    }
}

def build_single_deck(key):
    cfg = DECK_CONFIGS[key]
    print(f"\nBuilding {cfg['name']}...")
    deck = genanki.Deck(cfg['id'], cfg['name'])
    total_cards = 0

    for csv_file, has_type in cfg['files']:
        model = create_model(cfg['model_id'], cfg['model_name'], has_card_type=has_type)
        count = add_csv_to_deck(deck, model, csv_file, has_card_type=has_type)
        print(f"  -> Added {count} cards from {csv_file}")
        total_cards += count

    out_path = os.path.join(PACKAGES_DIR, cfg['output'])
    genanki.Package(deck).write_to_file(out_path)
    print(f"  [OK] Saved {out_path} ({total_cards} total cards)")

def build_all():
    print("=" * 60)
    print("Building all Anki decks into packages/...")
    print("=" * 60)
    for key in DECK_CONFIGS:
        build_single_deck(key)
    print("\n[SUCCESS] All Anki packages built successfully.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1].lower()
        if target in ["list", "-l", "--list"]:
            print("Available deck targets:")
            for k, v in DECK_CONFIGS.items():
                print(f"  - {k:<18} : {v['desc']}")
        elif target in DECK_CONFIGS:
            build_single_deck(target)
        else:
            print(f"Unknown target '{target}'. Use 'python build.py list' to see available decks.")
    else:
        build_all()
