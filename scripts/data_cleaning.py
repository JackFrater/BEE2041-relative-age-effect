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
    
    # Add birth quarter column based on country-specific school year cutoffs
    def assign_quarter(month, country):
        if not month: return None
        month = month.lower()

        # Standardise month to a number for easier comparison
        month_map = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12
        }
        month_num = month_map.get(month)
        if not month_num: return None   

        if "england" in country.lower():
            # England school year cut off is September 1st, so Q1 = September-November, Q2 = December-February, Q3 = March-May, Q4 = June-August
            if month_num in [9, 10, 11]: return 'Q1'
            elif month_num in [12, 1, 2]: return 'Q2'
            elif month_num in [3, 4, 5]: return 'Q3'
            elif month_num in [6, 7, 8]: return 'Q4'
        else:
            # South African school year cut off is January 1st, so Q1 = January-March, Q2 = April-June, Q3 = July-September, Q4 = October-December
            if month_num in [1, 2, 3]: return 'Q1'
            elif month_num in [4, 5, 6]: return 'Q2'
            elif month_num in [7, 8, 9]: return 'Q3'
            elif month_num in [10, 11, 12]: return 'Q4'
        return None 

    df['Birth Quarter'] = df['Birth Month'].apply(lambda m: assign_quarter(m, file_name))
    
    # Keep only essential columns: player name and date info
    name_col = next((col for col in df.columns if 'name' in col.lower() or col == df.columns[0]), df.columns[0])
    df_clean = df[[name_col, 'Birth Day', 'Birth Month', 'Birth Year', 'Birth Quarter']].copy()

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


