# CFB Stats Scraper & Cleaner (WIP)

This project aims to scrape college football team statistics from cfbstats.com and then clean the collected data for use in analysis.

## Project Structure

* `stats_scraper.py`: Script responsible for scraping raw team statistics from the cfbstats.
* `stats_cleaner.py`: Script responsible for processing and then cleaning the raw scraped data.
* `data/`: Directory to store inputs (like team IDs) and outputs (raw and cleaned stats) CSV files.
    * `team_ids.csv`: Contains mappings of team names to their IDs as set by the website.
    * `team_stats_raw.csv`: Raw data output from `stats_scraper.py`.
    * `team_stats_cleaned.csv`: Cleaned data output from `stats_cleaner.py`.

## Getting Started

1.  **Clone the repository** (or download the files).
2.  **Install dependencies:**
    ```bash
    pip install requests beautifulsoup4 pandas
    ```

## Usage

To run the scraping and cleaning process:

```bash
python stats_scraper.py
