import genanki
import csv
import os

model_id = 1607392321
edb_model = genanki.Model(
    model_id,
    'EDB Postgres Mastery Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'Topic'},
        {'name': 'Tags'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '''
                <div style="font-family: 'Segoe UI', Arial, sans-serif; font-size: 22px; text-align: center; color: #1e293b; margin-bottom: 20px; font-weight: 600; line-height: 1.4;">
                  {{Question}}
                </div>
                <div style="font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; text-align: center; color: #64748b; text-transform: uppercase; letter-spacing: 1px;">
                  <b>{{Topic}}</b>
                </div>
            ''',
            'afmt': '''
                {{FrontSide}}
                <hr id="answer" style="border: 0; height: 1px; background: #e2e8f0; margin: 20px 0;">
                <div style="font-family: 'Segoe UI', Arial, sans-serif; font-size: 17px; text-align: left; color: #334155; line-height: 1.6;">
                  {{Answer}}
                </div>
            ''',
        },
    ],
    css='''
        .card {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 18px;
            text-align: left;
            color: #1e293b;
            background-color: #ffffff;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
            max-width: 650px;
            margin: 0 auto;
        }
        code {
            background-color: #f1f5f9;
            color: #0f172a;
            padding: 3px 6px;
            border-radius: 6px;
            font-family: Consolas, 'Courier New', monospace;
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
)

deck = genanki.Deck(2059400116, 'EDB Postgres Mastery (250 Cards)')

csv_path = 'edb_postgres_deck.csv'
if not os.path.exists(csv_path):
    csv_path = os.path.join('decks', 'edb_postgres_deck.csv')

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader, None)
    card_count = 0
    for row in reader:
        if len(row) < 2:
            continue
        q = row[0]
        a = row[1]
        topic = row[2] if len(row) > 2 else ""
        tags_str = row[3] if len(row) > 3 else ""
        tags = [t.strip() for t in tags_str.split(" ") if t.strip()]
        
        note = genanki.Note(
            model=edb_model,
            fields=[q, a, topic, tags_str],
            tags=tags
        )
        deck.add_note(note)
        card_count += 1

output_pkg = 'EDB_Postgres_Mastery.apkg'
genanki.Package(deck).write_to_file(output_pkg)
print(f"Successfully generated {output_pkg} containing {card_count} cards.")
