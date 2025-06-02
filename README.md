# Predicting College Football Wins for 2025
Created by Ethan Wilson. A big thanks to cfbstats.com for allowing web scraping and making this project possible.
## Project Status: [Active]

### Project Introduction
The purpose of this project is to create an end-to-end data pipeline that predicts NCAA college football win percentages based on their historical performance statistics. This proejct simulates a real world sport analytics workflow: from webscraping and cleaning to modeling and prediction.

### Methods Used
* Web Scraping - Extracted 1,000+ rows of historical NCAA team stats (2016-2024)
* Data Cleaning - Standardized, parsed, and converted raw HTML data into usable datasets
* Feature Engineering - Created 'win_percentage' and 'turnover margin' to enhance predictive power
* Data Visualization - Plotted correlations, distributions, and model results for insight
* Machine Learning (WIP) -

### Technologies
* Python
* BeautifulSoup + Requests - Web scraping team stats from cfbstats.com
* Pandas & NumPy - Data manipulation and numerical operations
* Seaborn & Matplotlib - Data visualization & EDA
* Jupyter - Interactive analysis
* Scikit-learn - Regression modeling and evaluations

## Project Description
This project analyzes NCAA Division 1 FBS football teams from 2016 to 2023. The dataset includes team stats such as points per game, rushing yards, turnovers, penalties, and more. The goal of this project is to understand which stats are most predictive of win percentage and to build machine learning models that can forecast a 2025 team's success.

### Data Source
All data was scraped from [cfbstats.com](https://www.cfbstats.com/) using custom Python scripts.

### Questions Explored
- Which team statistics are most predictive of a successful season?
- Can we forecast team win percentages for this upcoming season and future seasons?
- How do turnovers, red zone performance, and offensive efficiency correlate with wins?

### Challenges Faced
- Cleaning inconsistent stat formats (time strings, compound fields, non-numeric characters)
- Handling missing or incomplete data (Missing years, stats, etc.)
- Balancing model simplicity vs. performance
- Handling outlier COVID-19 year (2020 season)

## Next Steps

- [x] Finish scraping and cleaning 2016–2023 team data
- [x] Conduct EDA and correlation analysis
- [x] Engineer key features (win_percentage, turnover_margin)
- [ ] Train/test regression models to predict 2025 win % 
- [ ] Evaluate model performance and interpret results
- [ ] Visualize and publish predictions for 2025

## Getting Started

1. Clone this repo (or download the files).
2. Install the dependencies.
    ```bash
    pip install requests beautifulsoup4 pandas seaborn matplotlib scikit-learn
    ```
    
3. To run the scraping and cleaning process:
    ```bash
    python stats_scraper.py
    ```

## Key Files
* `stats_scraper.py` – Web scraper for NCAA team stats from cfbstats.com
* `stats_cleaner.py` – Cleaning and preprocessing logic
* `eda.ipynb` – Exploratory data analysis and visualizations
* `modeling.ipynb` – Regression modeling and predictions
* `team_stats_cleaned.csv` – Final dataset used for modeling


## Contact

**Ethan Wilson**  
[LinkedIn](https://www.linkedin.com/in/ethan---wilson/)  
[GitHub](https://github.com/mixedethan)