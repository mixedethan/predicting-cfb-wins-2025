import requests
from bs4 import BeautifulSoup
import csv
import time
import os
import pandas as pd

# using team id data from teamid_scraper, we can now scrape stats for each team.
BASE_URL = "https://cfbstats.com"
OUTPUT_FILE = "data/team_stats.csv"
TEAM_FILE = "data/team_ids.csv"
#YEARS = list(range(2016, 2025))
YEARS = [2016]
DELAY = 1.5  # seconds between requests
total_data = []
key_stats = [
    "Scoring:  Points/Game",
    "Total Offense:  Yards / Play",
    "First Downs: Total",
    "Passing:  Rating",
    "Rushing:  Attempts - Yards - TD",
    "Passing:  Attempts - Completions - Interceptions - TD",
    "Interceptions: Returns - Yards - TD",
    "Fumbles: Number - Lost",
    "Penalties: Number - Yards",
    "Time of Possession / Game",
    "Red Zone: Success %",
    "Red Zone: Attempts - Scores"
]

compound_stat_list = {
    "Rushing:  Attempts - Yards - TD": ["rushing_attempts", "rushing_yards", "rushing_tds"],
    "Passing:  Attempts - Completions - Interceptions - TD": ["pass_attempts", "pass_completions", "pass_ints", "pass_tds"],
    "Fumbles: Number - Lost": ["fumbles_total", "fumbles_lost"],
    "Penalties: Number - Yards": ["penalties_number", "penalties_yards"],
    "Red Zone: Attempts - Scores": ["redzone_attempts", "redzone_scores"]
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def load_team_ids(path=TEAM_FILE):
    df = pd.read_csv(path)
    return dict(zip(df["team_name"], df["team_id"]))

team_dict = load_team_ids()
test_teams = list(team_dict.items())[:3]

# for each year...
for year in YEARS:

    # for each team...
    for team_name, team_id in test_teams:
        
        url = f"{BASE_URL}/{year}/team/{team_id}/index.html"


        try:
            response = requests.get(url, headers=headers, timeout=10)
            print("HTTP Status Code:", response.status_code)
            response.raise_for_status()
            time.sleep(DELAY)
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
            time.sleep(5) # let's give it some time :|
            continue
        
        soup = BeautifulSoup(response.text, 'html.parser')

        stat_table = soup.find('table', {'class': 'team-statistics'})
    
        row_data = {
            "year": year,
            "team": team_name
        }

        for row in stat_table.find_all('tr'):
            # cols is the three data entries (stat_name, team_value, opponent value)

            cols = row.find_all('td')
            if len(cols) != 3:
                continue

            # select the text for each data entry in a row
            stat_name = cols[0].get_text(strip=True)
            team_value = cols[1].get_text(strip=True)
            opponents_value = cols[2].get_text(strip=True)

            # if it's a stat we're not paying attention to, continue
            if stat_name not in key_stats:
                continue
            
            # if it's a compound stat
            if stat_name in compound_stat_list:
                team_parts = team_value.split(" - ")
                for sub_name, val in zip(compound_stat_list[stat_name], team_parts):
                    row_data[sub_name] = val

            # if it's a regular(single-valued) stat
            else:
                clean_name = stat_name.lower().replace(" ", "_").replace(":", "").replace("/", "_")
                row_data[clean_name] = team_value

        # add the data for a given team & a given year into the total data list
        total_data.append(row_data)

df = pd.DataFrame(total_data)
print(df.head())

df.to_csv("data/team_stats_preview.csv", index=False)

