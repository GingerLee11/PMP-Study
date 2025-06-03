import pandas as pd
# This script generates flashcards for the PMBOK6 core terms

# Creating flashcards for performing integration and complexity

data = [
    {
        "deck": "PMBOK6 - Core Terms",
        "front": "What is the key benefit of the Control Scope process?",
        "back": "The scope baseline is maintained throughout the project.",
        "tags": "KA::Scope PG::Monitoring ECO::Process",
        "note_type": "Basic",
        "media": ""
    },
    {
        "deck": "PMBOK6 - Core Terms",
        "front": "What does the Control Scope process monitor and manage?",
        "back": "The status of the project and product scope and changes to the scope baseline.",
        "tags": "KA::Scope PG::Monitoring ECO::Process",
        "note_type": "Basic",
        "media": ""
    },
    {
        "deck": "PMBOK6 - Core Terms",
        "front": "{{c1::Scope creep}} is the uncontrolled expansion to product or project scope without adjustments to time, cost, and resources.",
        "back": "Scope creep",
        "tags": "KA::Scope PG::Monitoring ECO::Process",
        "note_type": "Cloze",
        "media": ""
    },
    {
        "deck": "PMBOK6 - Core Terms",
        "front": "What analysis technique is used in Control Scope to compare the baseline to actual results?",
        "back": "Variance analysis",
        "tags": "KA::Scope PG::Monitoring ECO::Process",
        "note_type": "Basic",
        "media": ""
    },
    {
        "deck": "PMBOK6 - Core Terms",
        "front": "What analysis technique examines project performance over time to identify trends?",
        "back": "Trend analysis",
        "tags": "KA::Scope PG::Monitoring ECO::Process",
        "note_type": "Basic",
        "media": ""
    },
    {
        "deck": "PMBOK6 - Core Terms",
        "front": "What are the outputs of the Control Scope process?",
        "back": "Work performance information, change requests, project management plan updates, project documents updates.",
        "tags": "KA::Scope PG::Monitoring ECO::Process",
        "note_type": "Basic",
        "media": ""
    },
    {
        "deck": "PMBOK6 - Core Terms",
        "front": "What type of baseline may be revised if scope variances are severe?",
        "back": "Scope baseline, schedule baseline, cost baseline, or performance measurement baseline.",
        "tags": "KA::Scope PG::Monitoring ECO::Process",
        "note_type": "Basic",
        "media": ""
    },
]

# Format to expected structure
formatted_data = [
    [f"{deck}", f'"{front}"', f'"{back}"', tags, note_type, ""] 
    for deck, front, back, tags, note_type in data
]

# Create DataFrame
df_cards = pd.DataFrame(formatted_data, columns=["deck", "front", "back", "tags", "note_type", "media"])

# Save the DataFrame to a CSV file
df_cards.to_csv("flashcards.csv", index=False, encoding='utf-8', sep=',', header=True)
  
