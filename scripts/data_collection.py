import pandas as pd
import os
import requests
import io
from bs4 import BeautifulSoup

# Section 1: Raw Directory Creation

RAW_DIR = os.path.join("data", "raw")
if not os.path.exists(RAW_DIR):
    os.makedirs(RAW_DIR, exist_ok=True)

# Section 2: Scraper Logic

def scrape_wikipedia_squads(url, country_name, filename): 
    """Download birth date tables from Wikipedia and saves to data/raw."""
    print(f"Searching for squads data for {country_name} at {url}...")

    headers = {

        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',

        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',

        'Accept-Language': 'en-US,en;q=0.5',

        'Accept-Encoding': 'gzip, deflate',

        'Connection': 'keep-alive',

        'Upgrade-Insecure-Requests': '1',

        'Cache-Control': 'max-age=0',

    }

    try:
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.content, 'lxml')

        # Check if the page actaully loaded (200 = OK)
        if response.status_code != 200:
            print(f"Failed to load {url}")
            return
        
        target_heading = soup.find(lambda tag: tag.name in ['h2', 'h3'] and (
            tag.get('id') == country_name.replace(' ', '_') or
            (tag.get_text(strip=True) and country_name.lower() == tag.get_text(strip=True).lower())
        ))

        if not target_heading:
            target_heading = soup.find(lambda tag: tag.name in ['h2', 'h3'] and tag.get_text(strip=True) and country_name.lower() in tag.get_text(strip=True).lower())

        if target_heading:
            current_element = target_heading
            found_table = None

            for _ in range(200):  
                current_element = current_element.find_next()
                if not current_element or current_element.name in ["h2", "h3"]: 
                    break

                if current_element.name == "table" and 'class' in current_element.attrs and 'wikitable' in current_element['class']: 
                    html_data = io.StringIO(str(current_element))
                    temp_df = pd.read_html(html_data)[0]

                    if any("Date of birth" in str(col) for col in temp_df.columns):
                        found_table = current_element
                        break   

            if found_table:
                df = pd.read_html(str(found_table))[0]
                save_path = os.path.join(RAW_DIR, filename)
                df.to_csv(save_path, index=False)
                
                first_player = df.iloc[0, 1] if df.shape[1] > 1 else "N/A"
                print(f"Success: Saved {len(df)} players (First: {first_player})")
            else: 
                print(f"Failed: Could not find '{country_name}' squad table.")
        else:
            print(f"No heading found for {country_name} at {url}.")
    except Exception as e:
        print(f"Error scraping {url}: {e}")


# Section 3: Main Execution
if __name__ == "__main__":
    # England Rugby (From the 2023 World Cup)
    scrape_wikipedia_squads("https://en.wikipedia.org/wiki/2023_Rugby_World_Cup_squads", "England", "england_squad.csv")

    # South Africa Rugby (From the 2023 World Cup)
    scrape_wikipedia_squads("https://en.wikipedia.org/wiki/2023_Rugby_World_Cup_squads", "South Africa", "south_africa_squad.csv")

    # England Cricket ( From 2024 T20 World Cup)
    scrape_wikipedia_squads("https://en.wikipedia.org/wiki/2024_Men%27s_T20_World_Cup_squads", "England", "england_cricket_squad.csv")

    # South Africa Cricket ( From 2024 T20 World Cup)
    scrape_wikipedia_squads("https://en.wikipedia.org/wiki/2024_Men%27s_T20_World_Cup_squads", "South Africa", "south_africa_cricket_squad.csv")
