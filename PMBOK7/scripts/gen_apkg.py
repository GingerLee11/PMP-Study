import os
import pandas as pd
import random
import sys
import genanki

# --- Import note models ---
# Make sure this import is correct for your folder structure!
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from anki_decks.models import basic_model, cloze_model

# --- Config ---
CLEANED_CSV = r'PMBOK7\cleaned\PMBOK7_flashcards_cleaned.csv'
OUTPUT_FILE = r'PMBOK7\cleaned\PMBOK7_deck.apkg'

# --- Read the cleaned CSV ---
df = pd.read_csv(CLEANED_CSV).fillna('')

# Shuffle all cards for spaced-repetition randomness
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Insert ID if not already present
if 'ID' not in df.columns:
    df.insert(0, 'ID', range(1, len(df) + 1))

# --- Prepare package ---
package = genanki.Package([])

# --- Group cards by deck ---
for deck_name, group in df.groupby('deck'):
    deck_id = abs(hash(deck_name)) % (10 ** 10)
    deck = genanki.Deck(deck_id, deck_name)

    for _, row in group.iterrows():
        uid = str(row['ID'])
        tags = row['tags'].split() if row['tags'] else []

        if row['note_type'].lower() == 'cloze':
            note = genanki.Note(
                model=cloze_model,
                fields=[row['front'], row['back'], uid],
                tags=tags
            )
        else:
            note = genanki.Note(
                model=basic_model,
                fields=[row['front'], row['back'], uid],
                tags=tags
            )
        deck.add_note(note)

    package.decks.append(deck)

# --- Output to file ---
package.write_to_file(OUTPUT_FILE)
print(f"Anki package created at: {OUTPUT_FILE}")
