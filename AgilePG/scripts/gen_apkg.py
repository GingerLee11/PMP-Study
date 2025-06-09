import os
import pandas as pd
import random
import genanki
from models import basic_model, cloze_model

# Config
CLEANED_DIR = r'AgilePG\flashcards\cleaned'
OUTPUT_FILE = r'AgilePG\flashcards\AgilePG_Deck.apkg'

# Prepare the package
package = genanki.Package([])

# Read and shuffle all subdecks
all_cards = []

for filename in os.listdir(CLEANED_DIR):
    if not filename.endswith('.csv'):
        continue

    filepath = os.path.join(CLEANED_DIR, filename)
    df = pd.read_csv(filepath).fillna('')

    # Shuffle cards within subdeck
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    all_cards.append(df)

# Combine all shuffled subdecks
combined_df = pd.concat(all_cards, ignore_index=True)

# Final shuffle across all cards
combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Insert ID if not already present
if 'ID' not in combined_df.columns:
    combined_df.insert(0, 'ID', range(1, len(combined_df) + 1))

# Group by deck name
for deck_name, group in combined_df.groupby('deck'):
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

# Output to file
package.write_to_file(OUTPUT_FILE)
print(f"✅ Anki package created at: {OUTPUT_FILE}")
