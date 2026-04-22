import pandas as pd
import re
import os

# Section 1: Directory Setup
Raw_DIR = os.path.join("data", "raw")
CLEAN_DIR = os.path.join("data", "clean")

# Section 2: Regex
def extract_birth_year(date_str):
    
   #  Use Regex to pull "Day Month Year" out of the Wikipedia strings

    if pd.isna(date_str):
        return None, None, None
    
    # This pattern looks for: [Day] [Month] [Year], where Day is 1 or 2 digits, Month is a word, and Year is 4 digits
    match = re.search(r'(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})', date_str)
    
    if match:
        day, month, year = match.groups()
        return int(day), month, int(year)
    else:
        return None, None, None

# Section 3: Data Cleaning Logic
def clean_squads_data(file_name):
    print(f"Cleaning data from {file_name}...")

    # Load the raw data 
    raw_path = os.path.join(Raw_DIR, file_name)
    df = pd.read_csv(raw_path)

    # Extract date column (Wikipedia names vary)
    date_col = next((col for col in df.columns if 'date' in col.lower()), None)
    if not date_col:
        print(f"No date column found in {file_name}. Skipping.")
        return          

    col_name = date_col

    # Create three brand new columns for us to analyse
    df[['Birth Day', 'Birth Month', 'Birth Year']] = df[col_name].apply(extract_birth_year).apply(pd.Series)
    
    # Keep only essential columns: player name and date info
    name_col = next((col for col in df.columns if 'name' in col.lower() or col == df.columns[0]), df.columns[0])
    df_clean = df[[name_col, 'Birth Day', 'Birth Month', 'Birth Year']].copy()

    # Save the clean version
    clean_squads_data = file_name.replace("_raw", "").replace(".csv", "_clean.csv")
    save_path = os.path.join(CLEAN_DIR, clean_squads_data)
    df_clean.to_csv(save_path, index=False)
    print(f"Saved cleaned data to {save_path}.")   

    # Main Execution
if __name__ == "__main__":
    # Get a list of all raw data files that we just scraped
    raw_files = [f for f in os.listdir(Raw_DIR) if f.endswith(".csv")]
    for file in raw_files:
        clean_squads_data(file)

