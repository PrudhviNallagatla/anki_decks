import glob, csv
from collections import Counter

print('CSV Summary:')
for f in glob.glob('*.csv'):
    with open(f, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            continue
        rows = list(reader)
        topics = Counter(row.get('Topic', 'Unknown') for row in rows)
        print(f'\n--- {f} ---')
        print(f'Total cards: {len(rows)}')
        print(f'Topics: {dict(topics)}')
        if rows:
            q_field = next((fn for fn in reader.fieldnames if 'question' in fn.lower()), reader.fieldnames[0])
            print(f'Sample Q: {rows[0].get(q_field, list(rows[0].values())[0])}')
