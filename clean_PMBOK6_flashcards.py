import pandas as pd
from fuzzywuzzy import fuzz
import re

# Config
CSV_PATH = 'PMBOK6_study_flashcards.csv'
KNOWLEDGE_AREAS = [
    "Integration", "Scope", "Schedule", "Cost", "Quality",
    "Resource", "Communication", "Risk", "Procurement", "Stakeholder"
]
CLEAN_CSV = 'clean_PM6.csv'
FLAG_CSV = 'flag_PM6.csv'
DROP_REPORT = 'drop_report.txt'

# Load CSV
df = pd.read_csv(CSV_PATH).fillna('')
df = df[['deck', 'front', 'back', 'tags', 'note_type', 'media']].copy()

# Track drops and flags
drop_reasons = {rule: 0 for rule in ['overlong_back', 'duplicate_front', 'identical_front_back']}
flags = []

# Rule: Drop overlong backs (only for non-Cloze)
mask = ((df['back'].str.len() > 100) | (df['back'].str.count('\\n') > 1)) & (df['note_type'].str.lower() != 'cloze')
drop_reasons['overlong_back'] += mask.sum()
df = df[~mask]

# Rule: Drop identical front/back
mask = df['front'].str.strip().str.lower() == df['back'].str.strip().str.lower()
drop_reasons['identical_front_back'] += mask.sum()
df = df[~mask]

# Rule: Drop exact duplicate fronts
df['front_lower'] = df['front'].str.lower()
df = df.drop_duplicates(subset='front_lower', keep='first')
drop_reasons['duplicate_front'] = df.duplicated(subset='front_lower').sum()
df = df.drop(columns='front_lower')

# Rule: Flag nearly identical fronts (fuzzy match ≥ 90)
fronts = df['front'].tolist()
for i in range(len(fronts)):
    for j in range(i + 1, len(fronts)):
        if fuzz.token_set_ratio(fronts[i], fronts[j]) >= 70:
            flags.append((df.iloc[i].to_dict(), 'near_duplicate_front'))
            break

# Rule: Flag multi-sentence backs (only for non-Cloze)
def count_sentences(text):
    text = str(text)
    text = re.sub(r'\b(e\.g\.|i\.e\.)', '', text)
    return text.count('.')

for idx, row in df.iterrows():
    if row['note_type'].lower() != 'cloze' and count_sentences(row['back']) > 1:
        flags.append((row.to_dict(), 'multi_sentence_back'))

# Rule: Flag trivial backs (<4 chars, not formulaic, only for non-Cloze)
for idx, row in df.iterrows():
    if row['note_type'].lower() != 'cloze' and len(row['back'].strip()) < 4 and not re.search(r'[0-9+\-*/=]', row['back']):
        flags.append((row.to_dict(), 'trivial_back'))

# Rule: Flag missing KA in tags
def has_ka(tags):
    return any(ka in str(tags) for ka in KNOWLEDGE_AREAS)

for idx, row in df.iterrows():
    if not has_ka(row['tags']):
        flags.append((row.to_dict(), 'missing_ka_tag'))

# Convert flags to DataFrame
flag_rows = pd.DataFrame([f[0] for f in flags]).drop_duplicates()

# Drop flagged rows from df to get final clean set
df_clean = df[~df.index.isin(flag_rows.index)]

# Save outputs
df_clean.to_csv(CLEAN_CSV, index=False)
flag_rows.to_csv(FLAG_CSV, index=False)

with open(DROP_REPORT, 'w') as f:
    for rule, count in drop_reasons.items():
        f.write(f"Dropped {count} cards due to {rule}\n")
    f.write(f"Kept {len(df_clean)} cards\n")
    f.write(f"Flagged {len(flag_rows)} cards for review\n")

print("Cleaning complete. Outputs written.")
