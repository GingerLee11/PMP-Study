import pandas as pd
import os

# Config
CSV_PATH = r'PMBOK6\clean_PM6.csv'
OUTPUT_DIR = r'PMBOK6\PMBOK6_cleaned_decks'
KNOWLEDGE_AREAS = [
    "Integration", "Scope", "Schedule", "Cost", "Quality",
    "Resource", "Communication", "Risk", "Procurement", "Stakeholder"
]

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load CSV
df = pd.read_csv(CSV_PATH).fillna('')

# Drop old ID if it exists
df = df.drop(columns=['ID'], errors='ignore')

# For each Knowledge Area, filter and export
for ka in KNOWLEDGE_AREAS:
    subset = df[df['tags'].str.contains(ka, case=False, na=False)].copy()
    subset.insert(0, 'ID', range(1, len(subset) + 1))
    subset['deck'] = f'PMBOK6::{ka}'  # Rename deck field
    output_path = os.path.join(OUTPUT_DIR, f'{ka}.csv')
    subset.to_csv(output_path, index=False)
    print(f"Saved {len(subset)} cards to {output_path}")

print("Deck splitting complete.")
