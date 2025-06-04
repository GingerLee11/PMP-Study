import genanki
import pandas as pd
import os

# Config
CSV_DIR = r'PMBOK6\PMBOK6_cleaned_decks'
OUTPUT_PACKAGE = r'PMBOK6\PMBOK6_Deck.apkg'
MODEL_ID_BASIC = 1607392319
MODEL_ID_CLOZE = 1782910741

# Define models
basic_model = genanki.Model(
    MODEL_ID_BASIC,
    'Basic Model',
    fields=[
        {'name': 'Front'},
        {'name': 'Back'},
        {'name': 'UID'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Front}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
        },
    ],
    css="""
    .card {
      font-family: arial;
      font-size: 20px;
      text-align: left;
      color: black;
      background-color: white;
    }
    """
)

cloze_model = genanki.Model(
    MODEL_ID_CLOZE,
    'Cloze Model',
    fields=[
        {'name': 'Text'},
        {'name': 'BackExtra'},
        {'name': 'UID'},
    ],
    templates=[
        {
            'name': 'Cloze Card',
            'qfmt': '{{cloze:Text}}',
            'afmt': '{{cloze:Text}}<br>{{BackExtra}}',
        },
    ],
    css=basic_model.css,
    model_type=genanki.Model.CLOZE,
)

# Create top-level package
package = genanki.Package([])

# Process each CSV file
for filename in os.listdir(CSV_DIR):
    if not filename.endswith('.csv'):
        continue

    filepath = os.path.join(CSV_DIR, filename)
    df = pd.read_csv(filepath).fillna('')

    deck_name = df.iloc[0]['deck']
    deck_id = abs(hash(deck_name)) % (10 ** 10)
    deck = genanki.Deck(deck_id, deck_name)

    for _, row in df.iterrows():
        if row['note_type'].lower() == 'cloze':
            note = genanki.Note(
                model=cloze_model,
                fields=[row['back'], '', str(row['ID'])],
                tags=row['tags'].split() if row['tags'] else []
            )
        else:
            note = genanki.Note(
                model=basic_model,
                fields=[row['front'], row['back'], str(row['ID'])],
                tags=row['tags'].split() if row['tags'] else []
            )
        deck.add_note(note)

    package.decks.append(deck)

# Write output package
package.write_to_file(OUTPUT_PACKAGE)
print(f"Anki package created: {OUTPUT_PACKAGE}")
