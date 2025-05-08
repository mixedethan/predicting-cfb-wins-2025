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
YEARS = list(range(2016, 2025))
DELAY = 1.5  # seconds between requests

def load_team_ids(path=TEAM_FILE):
    df = pd.read_csv(path)
    return dict(zip(df["team_name"], df["team_id"]))

team_dict = load_team_ids()

test_url = f"https://cfbstats.com/2024/team/{team_dict.get('Air Force')}/index.html"

try:
    response = requests.get(test_url, timeout=10)
    print("HTTP Status Code:", response.status_code)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
        print("Request Error:", e)
        
soup = BeautifulSoup(response.text, 'html.parser')

stat_table = soup.find('table', {'class': 'team-statistics'})

for row in stat_table.find_all('tr'):
     cols = row.find_all('td')
     if len(cols) != 3:
          continue
     print(cols)
     break
     
