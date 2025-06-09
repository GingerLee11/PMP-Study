import genanki
import pandas as pd
import os

# Import custom models
from models import basic_model, cloze_model

# Config
CSV_DIR = r'PMBOK6\PMBOK6_cleaned_decks'
OUTPUT_PACKAGE = r'PMBOK6\PMBOK6_Deck.apkg'


# Create top-level package
package = genanki.Package([])

# Process each CSV file
for filename in os.listdir(CSV_DIR):
    if not filename.endswith('.csv'):
        continue

    filepath = os.path.join(CSV_DIR, filename)
    df = pd.read_csv(filepath).fillna('')

    if 'ID' not in df.columns:
        df.insert(0, 'ID', range(1, len(df) + 1))

    deck_name = df.iloc[0]['deck']
    deck_id = abs(hash(deck_name)) % (10 ** 10)
    deck = genanki.Deck(deck_id, deck_name)

    for _, row in df.iterrows():
        uid = str(row['ID'])
        if row['note_type'].lower() == 'cloze':
            note = genanki.Note(
                model=cloze_model,
                fields=[row['front'], row['back'], uid],
                tags=row['tags'].split() if row['tags'] else []
            )
        else:
            note = genanki.Note(
                model=basic_model,
                fields=[row['front'], row['back'], uid],
                tags=row['tags'].split() if row['tags'] else []
            )
        deck.add_note(note)

    package.decks.append(deck)

# Write output package
package.write_to_file(OUTPUT_PACKAGE)
print(f"Anki package created: {OUTPUT_PACKAGE}")
