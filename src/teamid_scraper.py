import requests
from bs4 import BeautifulSoup
import csv
import os

# webscraper to scrape team names and team IDs from cfbstats.com which are then saved to a csv

def get_team_ids():

    url = "https://cfbstats.com"

    # error checking for the website
    try:
        response = requests.get(url, timeout=10)
        print("HTTP status:", response.status_code)
        print("Final URL:", response.url)
        response.raise_for_status()
        

    except requests.exceptions.RequestException as e:
        print("Request Error:", e)
        return {}

    # load bs4 parser
    soup = BeautifulSoup(response.text, 'html.parser')
    team_dict = {}

    # locate the sidebar containing all the teams
    sidebar = soup.find('div', id='leftColumn')
    if not sidebar:
        print('Sidebar not found in HTML.')
        return team_dict

    # find all the a tags and hrefs containing team names & ids
    for link in sidebar.find_all('a'):
        href = link.get('href', '')
        if f"/2024/team/" in href and href.endswith("/index.html"):
            try:
                parts = href.split("/")
                team_id = parts[3]
                team_name = link.text.strip()
                team_dict[team_name] = team_id
            except IndexError:
                continue

    return team_dict

def save_team_ids(team_dict, path="data/team_ids.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        #initial row
        writer.writerow(["team_name", "team_id"])
        for name, tid in team_dict.items():
            writer.writerow([name, tid])
    print(f"\nSaved team ID map to {path}")


if __name__ == "__main__":
    # Run test to verify all teams
    teams = get_team_ids()
    print("\nFound teams (expect 134):", len(teams))
    for name, tid in list(teams.items()):
        print(f"{name} -> {tid}")

    save_team_ids(teams) 
