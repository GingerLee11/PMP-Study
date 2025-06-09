import pandas as pd
import os
from pathlib import Path

# Config
GLOSSARY_PATH = r'AgilePG\\flashcards\\raw\\glossary_deck.csv'
CONCEPT_PATH = r'AgilePG\\flashcards\\raw\\APG_concept_card.csv'
OUTPUT_DIR = r'AgilePG\\flashcards\\cleaned'

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load CSVs with safe parsing options
glossary_df = pd.read_csv(GLOSSARY_PATH, quotechar='"', escapechar='\\', encoding='utf-8', on_bad_lines='warn').fillna('')
concept_df = pd.read_csv(CONCEPT_PATH, quotechar='"', escapechar='\\', encoding='utf-8', on_bad_lines='warn').fillna('')

# Normalize tags (pipe-separated to space-separated in glossary)
glossary_df['tags'] = glossary_df['tags'].str.replace('|', ' ', regex=False)

# Remove problematic special characters from all text fields
def clean_text_fields(df):
    return df.applymap(lambda x: x.replace('’', "'").replace('–', '-') if isinstance(x, str) else x)

glossary_df = clean_text_fields(glossary_df)
concept_df = clean_text_fields(concept_df)

# Save glossary as single cleaned CSV
glossary_out = os.path.join(OUTPUT_DIR, 'glossary_deck.csv')
glossary_df.to_csv(glossary_out, index=False)
print(f"Saved glossary to {glossary_out} with {len(glossary_df)} cards")

# Split conceptual deck into separate files by subdeck
for deck_name, group_df in concept_df.groupby('deck'):
    # Clean filename by replacing colons and slashes
    safe_name = deck_name.replace('::', '__').replace(' ', '_').replace('&', 'and')
    output_path = os.path.join(OUTPUT_DIR, f'{safe_name}.csv')
    group_df.to_csv(output_path, index=False)
    print(f"Saved {len(group_df)} cards to {output_path}")

print("Data preprocessing complete.")
