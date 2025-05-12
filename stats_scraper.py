import requests
from bs4 import BeautifulSoup
import csv
import time
import os
import pandas as pd
import random

# using team id data from teamid_scraper, we can now scrape stats for each team.
BASE_URL = "https://cfbstats.com"
OUTPUT_FILE = "data/team_stats.csv"
TEAM_FILE = "data/team_ids.csv"
#YEARS = list(range(2016, 2024))
YEARS = [2016]
DELAY = 1.5  # seconds between requests
total_data = []

raw_key_stats = [
    "Scoring: Points/Game",
    "Total Offense: Yards / Play",
    "First Downs: Total",
    "Passing: Rating",
    "Rushing: Attempts - Yards - TD",
    "Passing: Attempts - Completions - Interceptions - TD",
    "Interceptions: Returns - Yards - TD",
    "Fumbles: Number - Lost",
    "Penalties: Number - Yards",
    "Time of Possession / Game",
    "Red Zone: Success %",
    "Red Zone: Attempts - Scores"
]

def normalize_stat(s):
    # normalizes the stat names by stripping whitespace and joining the words
    return " ".join(s.strip().split())

def generate_clean_key(stat_name_normalized):
     return stat_name_normalized.replace(" ", "_").replace(":", "").replace("/", "_").replace("-", "_").replace("%", "pct")

key_stats = [normalize_stat(s) for s in raw_key_stats]

compound_stat_list = {
    normalize_stat("Rushing: Attempts - Yards - TD"): ["rushing_attempts", "rushing_yards", "rushing_tds"],
    normalize_stat("Passing: Attempts - Completions - Interceptions - TD"): ["pass_attempts", "pass_completions", "pass_ints", "pass_tds"],
    normalize_stat("Fumbles: Number - Lost"): ["fumbles_total", "fumbles_lost"],
    normalize_stat("Penalties: Number - Yards"): ["penalties_number", "penalties_yards"],
    normalize_stat("Red Zone: Attempts - Scores"): ["redzone_attempts", "redzone_scores"]
}

headers = {
    # to be a little misleading...
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def load_team_ids(path=TEAM_FILE):
    df = pd.read_csv(path)
    return dict(zip(df["team_name"], df["team_id"]))

team_dict = load_team_ids()
if not team_dict:
    print("Couldn't load team information. Exiting.")
    exit()

test_teams = list(team_dict.items())[:3]

# for each year...
for year in YEARS:

    # for each team...
    for team_name, team_id in test_teams:
        
        url = f"{BASE_URL}/{year}/team/{team_id}/index.html"
        print(f"Attempting to scrape: {url}")

        try:
            sleep_time = random.uniform(DELAY * 0.8, DELAY * 1.2)
            print(f"Sleeping for {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {team_name} ({year}): {e}")
            time.sleep(random.uniform(5, 10)) # let's give it some time :|
            continue
        
        soup = BeautifulSoup(response.text, 'html.parser')

        stat_table = soup.find('table', {'class': 'team-statistics'})

        if not stat_table:
            print(f"Stat table not found for {team_name} ({year}), Skipping for now.")
            continue

        row_data = {
            "year": year,
            "team": team_name
        }

        for stat_normalized in key_stats:
            clean_name_base = generate_clean_key(stat_normalized)

            if stat_normalized in compound_stat_list:
                # initiliaze compound stat sub parts
                for sub in compound_stat_list[stat_normalized]:
                    row_data[sub] = None
                row_data[f"{clean_name_base}_opp"] = None
            else:
                # initialize key for regular stats
                row_data[clean_name_base] = None
                row_data[f"{clean_name_base}_opp"] = None


        # for each row within the stat table
        for row in stat_table.find_all('tr'):
            # cols is the three data entries (stat_name, team_value, opponent value)
            cols = row.find_all('td')
            if len(cols) != 3:
                continue
            
            # select the text for each data entry in a row
            stat_name_raw = cols[0].get_text(strip=True)
            team_value = cols[1].get_text(strip=True)
            opponents_value = cols[2].get_text(strip=True)
            stat_name_normalized = normalize_stat(stat_name_raw)

            # if it's a stat we're not paying attention to, continue
            if stat_name_normalized not in key_stats:
                continue
            
            print("Found stat label:", stat_name_normalized)
            
            clean_name_base = generate_clean_key(stat_name_normalized)

            # if it's a compound stat
            if stat_name_normalized in compound_stat_list:
                team_parts = team_value.split(" - ")
                
                expected_parts = len(compound_stat_list[stat_name_normalized])
                if len(team_parts) == expected_parts:
                    for sub_name, val in zip(compound_stat_list[stat_name_normalized], team_parts):
                        row_data[sub_name] = val
                else:
                    print(f"Warning: Mismatch in parts for compound stat '{stat_name_raw}' (Normalized: '{stat_name_normalized}') in {year} for {team_name}. Value: '{team_value}'. Expected {expected_parts} parts, got {len(team_parts)}.")

            # if it's a regular(single-valued) stat
            else:
                row_data[clean_name_base] = team_value

            row_data[f"{clean_name_base}_opp"] = opponents_value

        # add the data for a given team & a given year into the total data list
        total_data.append(row_data)

# after scraping all teams and years, create a pandas df
df = pd.DataFrame(total_data)
print("\n--- Scraping Complete ---")
print("Following is the total data:\n")
print(df.head())
print(f"\nDataFrame shape: {df.shape}")

os.makedirs('data', exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)
print(f"\nData saved to {OUTPUT_FILE}")