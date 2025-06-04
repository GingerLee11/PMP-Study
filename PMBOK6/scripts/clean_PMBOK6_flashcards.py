import pandas as pd

# Config
CSV_PATH = 'PMBOK6_study_flashcards.csv'
CLEAN_CSV = r'PMBOK6\clean_PM6.csv'
FLAG_CSV = r'PMBOK6\flag_PM6.csv'
DROP_REPORT = r'PMBOK6\drop_report.txt'

# Load CSV
df = pd.read_csv(CSV_PATH).fillna('')
df = df[['deck', 'front', 'back', 'tags', 'note_type', 'media']].copy()
df.insert(0, 'ID', range(1, len(df) + 1))

# Track drops and flags
drop_count = 0
flags = []

# Drop backs over 80 chars (non-Cloze only)
drop_mask = (df['note_type'].str.lower() != 'cloze') & (df['back'].str.len() > 80)
drop_count += drop_mask.sum()
df = df[~drop_mask]

# Flag backs between 50 and 80 chars (non-Cloze only)
for idx, row in df.iterrows():
    back_len = len(row['back'])
    if row['note_type'].lower() != 'cloze' and 50 <= back_len <= 80:
        flagged_row = row.to_dict()
        flagged_row['flag_reason'] = 'back_length_50_80_consider_cloze'
        flags.append(flagged_row)

# Convert flags to DataFrame
flag_rows = pd.DataFrame(flags).drop_duplicates(subset='ID')

# Drop flagged rows from df to get final clean set
df_clean = df[~df['ID'].isin(flag_rows['ID'])]

# Save outputs
df_clean.to_csv(CLEAN_CSV, index=False)
flag_rows.to_csv(FLAG_CSV, index=False)

with open(DROP_REPORT, 'w') as f:
    f.write(f"Dropped {drop_count} cards due to back > 80 chars\n")
    f.write(f"Kept {len(df_clean)} cards\n")
    f.write(f"Flagged {len(flag_rows)} cards for review\n")

print("Simplified cleaning complete. Outputs written.")
