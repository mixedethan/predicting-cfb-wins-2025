# Predicting College Football Wins for 2025
 An End-to-End Machine Learning Pipeline for NCAA Football Win Perecentage Forecasting

## Table of Contents
1.  [Project Overview](#project-overview)
2.  [Data Acquisition & Preprocessing](#data-acquisition--preprocessing)
3.  [Exploratory Data Analysis (EDA) & Feature Engineering](#exploratory-data-analysis-eda--feature-engineering)
4.  [Machine Learning Modeling](#machine-learning-modeling)
    * [Ridge Regression](#ridge-regression)
    * [Random Forest Regressor](#random-forest-regressor)
    * [Gradient Boosting (LightGBM)](#gradient-boosting-lightgbm)
    * [Model Comparison & Selection](#model-comparison--selection)
5.  [Key Findings & 2025 Predictions (WIP)](#key-findings--2025-predictions)
6.  [Challenges Faced](#challenges-faced)
7.  [Future Enhancements](#future-enhancements)
8.  [Getting Started](#getting-started)
9.  [Key Files](#key-files)
10. [Contact](#contact)

<!-- Part 1 -->
## Project Overview
The purpose of this project is to create an end-to-end data pipeline that predicts NCAA college football win percentages based on their historical performance statistics. The project analyzes NCAA Division 1 FBS football teams from 2016 to 2024. The dataset includes team stats such as points per game, rushing yards, turnovers, penalties, and more. The goal of this project is to understand which stats are most predictive of win percentage and to build machine learning models that can forecast a 2025 team's success. This proejct simulates a real world sport analytics workflow: from webscraping and cleaning to modeling and prediction.

This project simulates a real-world sports analytics challenge, encompassing:

* **Web Scraping:** Extracted 1,000+ rows of historical NCAA team stats (2016-2024) directly from [cfbstats.com](https://www.cfbstats.com/).
* **Data Engineering:** Cleaning, transforming, and preparing raw, inconsistent data.
* **Feature Engineering:** - Created 'win_percentage' and 'turnover margin' to enhance predictive power.
* **Exploratory Data Analysis (EDA):** Uncovering patterns, trends, and relationships within the cleaned data.
* **Machine Learning Modeling:** Developing, training, and evaluating multiple regression models using advanced techniques such as Linear Regression, Ridge Regression, Random Forest Regressors, and Graident Boosting.
* **Hyperparameter Tuning & Cross-Validation:** Optimizing model performance and ensuring robust generalization.
* **Model Interpretation:** Understanding which statistics drive predictive outcomes.
* **Forecasting:** Generating concrete win percentage predictions for the 2025 season.

**Technologies**
* **Python:** Primary programming language for the entire pipeline.
* **BeautifulSoup + Requests:** For web scraping NCAA team statistics from [cfbstats.com](https://www.cfbstats.com/).
* **Pandas & NumPy:** Essential for data manipulation, cleaning, and numerical operations.
* **Seaborn & Matplotlib:** For creating insightful data visualizations and exploratory data analysis.
* **Jupyter:** For interactive notebooks, analysis, and presenting the modeling workflow.
* **Scikit-learn:** Library used for machine learning, including regression modeling, evaluation measures, feature scaling, and hyperparameter tuning (GridSearchCV, RandomizedSearchCV).
* **LightGBM:** An efficient and powerful gradient boosting framework for predictive modeling.

**Questions Explored**
* Which team statistics are most predictive of a successful season?
* Can we forecast team win percentages for this upcoming season and future seasons?
* How do specific game elements like turnovers, red zone performance, and offensive efficiency correlate with wins?

<!-- Part 2 -->
## Data Acquisition & Preprocessing
This phase focuses on gathering raw data and transforming it into a clean, usable format for both analysis and modeling.

* **Source:** Historical NCAA team statistics (2016-2024 seasons) were extracted from `cfbstats.com` using BeautifulSoup and Requests libraries. This included detailed team-level metrics such as points per game, rushing yards, passing efficiency, turnover differentials, penalties, and more. Statistics such and the Wins and Losses were also scraped from a seperate portion of the website.

* **Web Scraping (`stats_scraper.py`):** A custom Python script was developed to automate the scraping of data from the website's HTML tables using both BeautifulSoup and Requests libraries.
    * Due to the structure of the site, `team_ids.csv` was scraped first in order to allow for a clean scraping of the team stats. The website's link structure was as follows
    ```
    https://cfbstats.com/YEAR/team/TEAM_ID/index.html
    ```
    * Once the IDs were scraped, we could easily loop through both years and `team_ids.csv` in order to send HTTP GET requests.
    * Realistic headers were used to ensure the website wouldn't block HTTP GET requests if it believed it detected a bot.
    

* **Data Cleaning (`stats_cleaner.py`):** The scraped raw data underwent extensive cleaning and preprocessing to address real-world data challenges:
    * Standardizing inconsistent statistical formats (e.g., converting time strings to numerical seconds).
    * Parsing compound fields into separate, usable metrics (e.g., converting `Passing: Attempts - Completions - Interceptions - TD` into four separate stats).
    * Converting non-numeric characters to numerical types.
    * Any missing or incomplete data points were replaced with the average for their respective feature.
    * **Excluding the 2020 Season:** The 2020 season was excluded from the primary model training dataset due to shortened schedules, lack of participations by teams, and different health protocols. The year was an outlier in itself due to the COVID-19 pandemic. Including the year could introduce noise and skew the model's learning.
    
---

<!-- Part 3 -->
## Exploratory Data Analysis (EDA) & Feature Engineering

Before modeling, a deep dive into the cleaned data was conducted to understand its structure, patterns, and to create features that would enhance the models' predictive capabilities.

* **EDA Goal:** To gain insights into the distributions of variables with respect to win percentage, identify outliers, and understand the relationships between different team statistics and win percentage.

* **Key Derived Features:** Several critical features were engineered to provide more direct predictive signals:
    * `win_percentage`: The target variable, calculated as `wins / (wins + losses)`.
    * `turnover_margin`: The difference between turnovers gained and turnovers lost, including both interceptions and fumbles; A crucial indicator of game control.
    * `net_scoring_points_game`: The difference between points scored and points allowed per game, often the most direct contributor to game outcomes.
    * `net_offense_yards_per_play`: A measure of overall offensive efficiency relative to defensive efficiency.
    * `net_penalties_yards`: The difference in penalty yardage.
    * `net_red_zone_success_pct`: How much better a team is in the redzone vs. their opponent.

* **Insights from EDA:**
    * Visualizations (e.g., scatter plots, heatmaps for correlation) revealed strong linear relationships between `net_scoring_points_game` and `win_percentage`, confirming it as the single most powerful predictor of team success.
    * Initial analysis showed the impact of defensive metrics, such as `scoring_points_game_opp` and `time_possesion_sec_opp` on win probability.
    * `turnover_margin` showed a clear **positive correlation** with `win_percentage`, highlighting the importance of ball security and takeaways.
    * The distribution of win percentages often exhibited a bimodal pattern or normal distribution, emphasizing the presence of both high-performing and low-performing teams.
    * Correlation analysis found potential **multicollinearity** within certain offensive and defensive statistics, leading to the decision to use models like Ridge Regression.
    * Since 2018, there has been a steady decline in the average team points per game for each year. This could be contributed to many different factors and needs to be investigated.
    

---

<!-- Part 4 -->
## Machine Learning Modeling

This section explains both the development and evaluation of the different machine learning models used to predict college football win percentages. A **chronological train-test split** was used, with all the models trained on data from 2016-2023 (excluding 2020) and testing their performance on unseen 2024 data, simulating a real-world forecasting scenario. In addition, all features were scaled using the `StandardScaler` class to ensure consistent ranges and better model performance. The tuned models' performance were assessed using Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), R-squared (R2), and Variance Inflation Factor (VIF) on the unseen 2024 test data.

### Ridge Regression

* **Description:** Ridge Regression is a linear regression model that uses L2 regularization. This technique punishes the model for using larges weights which prevents overfitting.
* **Why it was used:** At first, a standard linear regression model was used in order to make predictions. However, variables such as `net_scoring_points_game` and `scoring_points_game` showed extremely large coefficients indicating multicollinearity as one is derived from the other. The solution was to implement a Ridge Regression in order to shrink the coefficients and stabilize the model while retianing interpretability.
* **Hyperparameter Tuning:** `GridSearchCV` was used to  search for the optimal `alpha` parameter. 5-fold cross-validation was used to ensure a proper evaluation of each `alpha` value on the training data. The default alpha  of 1.0 was found to be the optimal value.
* **Result:** Coefficients were analyzed to understand the direct linear relationship between each statistical feature and the predicted win percentage, highlighting the most impactful predictors.

### Random Forest Regressor

* **Description:**

### Gradient Boosting (LightGBM)

* **Description:**

### Model Comparison & Selection

* Following the evaluations of each model, a comparison of their performance metrics (MAE, RMSE, R2) on the **unseen 2024 test set** will be conducted.
* WIP

---
<!-- Part 5-->
##  Key Findings & 2025 Predictions (WIP)

This section will contain the most significant insights gained from the analysis.

* WIP.

---

## Challenges Faced
- Cleaning inconsistent stat formats (time strings, compound fields, non-numeric characters)
- Handling missing or incomplete data (Missing years, stats, etc.)
- Balancing model simplicity vs. performance
- Handling outlier COVID-19 year (2020 season)

## Future Enhancements

This project serves as a strong foundation but I believe there are several exciting features for future development and improvement:

**Current Goals:**
* [x] Finish scraping and cleaning 2016–2023 team data
* [x] Conduct EDA and correlation analysis
* [x] Engineer key features (win_percentage, turnover_margin)
* [ ] Train/test regression models to predict 2025 win % 
* [ ] Evaluate model performance and interpret results
* [ ] Visualize and publish predictions for 2025

**Future Goals:**
* [ ] Create **Feature Importance Visualizations** across all models for comparative insights.
* [ ] Incorporate a **Strength of Schedule (SOS)** feature to account for opponent quality and which is a real-world determinant of team success.

## Getting Started

1. **Clone the Repository:.**
    ```
    git clone https://github.com/mixedethan/predicting-cfb-wins-2025
    cd predicting-cfb-wins-2025
    ```
2. **Install the Dependencies.**
    ```bash
    pip install requests beautifulsoup4 pandas seaborn matplotlib scikit-learn
    ```
    
3. **Run the Data Pipeline:**
    ```bash
    python stats_scraper.py
    ```

5.  **Explore EDA, Modeling & Generate Predictions:**
    ```bash
    jupyter notebook cfb_modeling.ipynb
    ```
    Open the `cfb_modeling.ipynb` notebook and run all cells to execute the data preprocessing, EDA, feature engineering, model training, hyperparameter tuning, evaluation, and generate the 2025 win percentage predictions.

---

## Key Files
* `stats_scraper.py`: Python script responsible for web scraping college football team statistics from `cfbstats.com`.
* `stats_cleaner.py`: Contains functions for cleaning, standardizing, and preprocessing the raw data into a usable format.
* `cfb_modeling.ipynb`: The main Jupyter Notebook detailing the entire machine learning pipeline, including data loading, extensive EDA, feature engineering, model training, model evaluation, comparison, and the final 2025 win percentage predictions.
* `team_stats_raw.csv` : Raw data scraped from `cfbstats.com`.
* `team_stats_cleaned.csv`: The cleaned and preprocessed dataset used for the modeling phase.


## Contact

**Ethan Wilson**  
[LinkedIn](https://www.linkedin.com/in/ethan---wilson/)  
[GitHub](https://github.com/mixedethan)