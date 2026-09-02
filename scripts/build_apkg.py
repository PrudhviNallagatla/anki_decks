import genanki
import csv
import os

# Define a nice looking Anki model
model_id = 1607392319
my_model = genanki.Model(
  model_id,
  'CS Fundamentals Model',
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
        <div style="font-family: Arial; font-size: 24px; text-align: center; color: #333; margin-bottom: 20px; font-weight: bold;">
          {{Question}}
        </div>
        <div style="font-family: Arial; font-size: 14px; text-align: center; color: #777;">
          <i>Topic: {{Topic}}</i>
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
            
            tags = tags_str.split(" ") if tags_str else []
            
            note = genanki.Note(
                model=my_model,
                fields=[question, answer, topic, tags_str],
                tags=tags
            )
            deck.add_note(note)

# 1. DSA
dsa_deck = genanki.Deck(2059400110, 'DSA Mastery')
add_csv_to_deck(dsa_deck, 'fundamentals_dsa.csv')
genanki.Package(dsa_deck).write_to_file('DSA_Mastery.apkg')
print("Generated DSA_Mastery.apkg")

# 2. DBMS + Excel
dbms_excel_deck = genanki.Deck(2059400111, 'DBMS & Excel Mastery')
add_csv_to_deck(dbms_excel_deck, 'fundamentals_dbms.csv')
add_csv_to_deck(dbms_excel_deck, 'fundamentals_excel.csv')
genanki.Package(dbms_excel_deck).write_to_file('DBMS_Excel_Mastery.apkg')
print("Generated DBMS_Excel_Mastery.apkg")

# 3. Net + OOPs
net_oops_deck = genanki.Deck(2059400112, 'Networking & OOPs Mastery')
add_csv_to_deck(net_oops_deck, 'fundamentals_networking.csv')
add_csv_to_deck(net_oops_deck, 'fundamentals_oops.csv')
genanki.Package(net_oops_deck).write_to_file('Networking_OOPs_Mastery.apkg')
print("Generated Networking_OOPs_Mastery.apkg")

# 4. OS + System Design
os_sysdesign_deck = genanki.Deck(2059400113, 'OS & System Design Mastery')
add_csv_to_deck(os_sysdesign_deck, 'fundamentals_os.csv')
add_csv_to_deck(os_sysdesign_deck, 'fundamentals_system_design.csv')
genanki.Package(os_sysdesign_deck).write_to_file('OS_SysDesign_Mastery.apkg')
print("Generated OS_SysDesign_Mastery.apkg")
