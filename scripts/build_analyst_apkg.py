import genanki
import csv
import os

# Define a nice looking Anki model
model_id = 1607392320 # Using a slightly different model_id to avoid conflicts
my_model = genanki.Model(
  model_id,
  'CS Fundamentals Model - Analyst',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
    {'name': 'Topic'},
    {'name': 'Tags'},
    {'name': 'CardType'}
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '''
        <div style="font-family: Arial; font-size: 24px; text-align: center; color: #333; margin-bottom: 20px; font-weight: bold;">
          {{Question}}
        </div>
        <div style="font-family: Arial; font-size: 14px; text-align: center; color: #777;">
          <i>Topic: {{Topic}}</i><br>
          <span style="font-size: 12px; color: #999;">Type: {{CardType}}</span>
        </div>
      ''',
      'afmt': '''
        {{FrontSide}}
        <hr id="answer">
        <div style="font-family: Arial; font-size: 18px; text-align: left; color: #222; line-height: 1.5;">
          {{Answer}}
        </div>
      ''',
    },
  ],
  css='''
    .card {
      font-family: arial;
      font-size: 20px;
      text-align: left;
      color: black;
      background-color: #f9f9f9;
      padding: 20px;
      border-radius: 10px;
    }
    code {
      background-color: #eee;
      padding: 2px 4px;
      border-radius: 4px;
      font-family: monospace;
      font-size: 16px;
      display: block;
      margin-top: 5px;
      margin-bottom: 10px;
      white-space: pre-wrap;
    }
    b {
      color: #0056b3;
    }
  '''
)

def add_csv_to_deck(deck, csv_path):
    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        return
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader, None) # skip header
        for row in reader:
            if len(row) < 2:
                continue
            question = row[0]
            answer = row[1]
            topic = row[2] if len(row) > 2 else ""
            tags_str = row[3] if len(row) > 3 else ""
            ctype = row[4] if len(row) > 4 else ""
            
            tags = tags_str.split(" ") if tags_str else []
            
            note = genanki.Note(
                model=my_model,
                fields=[question, answer, topic, tags_str, ctype],
                tags=tags
            )
            deck.add_note(note)

analyst_deck = genanki.Deck(2059400115, 'Data Analyst Mastery')
add_csv_to_deck(analyst_deck, 'fundamental_analyst_deck.csv')
genanki.Package(analyst_deck).write_to_file('Analyst_Mastery.apkg')
print("Generated Analyst_Mastery.apkg")
