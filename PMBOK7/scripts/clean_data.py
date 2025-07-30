import os
import csv
import logging
import re

# Filepaths
input_csv = r'PMBOK7\raw\PMBOK7_flashcards.csv'
output_csv = r'PMBOK7\cleaned\PMBOK7_flashcards_cleaned.csv'
log_file = r'PMBOK7\logs\clean_data.log'

# Ensure output directories exist
os.makedirs(os.path.dirname(output_csv), exist_ok=True)
os.makedirs(os.path.dirname(log_file), exist_ok=True)

# Setup logging
logging.basicConfig(filename=log_file,
                    filemode='w',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

# Mapping helpers
def get_subdeck(row):
    deck = row['deck'].strip()
    tags = row['tags']
    subdeck = deck

    if deck == "PMBOK7::Performance Domains":
        # Match everything after Domain:: up to next tag (e.g., ECO::, MMA::) or end of string
        domain_match = re.search(r"Domain::(.*?)(?:\s+\w+::|$)", tags)
        if domain_match:
            domain_name = domain_match.group(1).strip()
            subdeck = f"{deck}::{domain_name}"
            logging.info(f"Mapped Performance Domain card to subdeck: {subdeck}")
        else:
            logging.warning(f"No Domain:: tag found in tags: '{tags}' for card: {row['front']}")
    elif deck == "PMBOK7::MMA":
        mma_match = re.search(r"MMA::(.*?)(?:\s+\w+::|$)", tags)
        if mma_match:
            mma_name = mma_match.group(1).strip()
            subdeck = f"{deck}::{mma_name}"
            logging.info(f"Mapped MMA card to subdeck: {subdeck}")
        else:
            logging.warning(f"No MMA:: tag found in tags: '{tags}' for card: {row['front']}")
    # Tailoring or other decks are left as-is
    return subdeck

# Main processing
with open(input_csv, encoding='utf-8-sig', newline='') as infile, \
     open(output_csv, 'w', encoding='utf-8', newline='') as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for i, row in enumerate(reader, start=1):
        old_deck = row['deck']
        new_deck = get_subdeck(row)
        row['deck'] = new_deck
        writer.writerow(row)

        if old_deck != new_deck:
            logging.info(f"Row {i}: Changed deck '{old_deck}' -> '{new_deck}'")
        else:
            logging.info(f"Row {i}: Kept deck as '{old_deck}'")

print(f"Processing complete. Cleaned data written to '{output_csv}'. Log at '{log_file}'.")
