import pandas as pd
import os

INPUT_FILE = "data/team_stats_raw.csv"
OUTPUT_FILE = "data/team_stats_cleaned.csv"

def time_to_sec(t):
    if isinstance(t, str) and ":" in t:
        try:
            if '.' in t:
                min_secs, millisecs = t.split('.')
                mins, secs = map(int, min_secs.split(':'))
                return mins * 60 + secs + float('0.' + millisecs)
            else:
                mins, secs = map(int, t.split(':'))
                return mins * 60 + secs
        except ValueError:
            return None
    return None

def clean_data(df):
    print("\nMissing values before cleaning:\n", df.isna().sum())

    # normalize the columns names
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(":", "")
        .str.replace("/", "_")
    )

    # clean the percentage columns up
    for col in ['red_zone_success_pct', 'red_zone_success_pct_opp']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace('%', '', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # convert the time to seconds
    df['time_possession_sec'] = df['time_of_possession___game'].apply(time_to_sec)
    df['time_possession_sec_opp'] = df['time_of_possession___game_opp'].apply(time_to_sec)


    # convert everything to numeric data type
    for col in df.columns:
        if col not in ['team', 'year']:
            df[col] = pd.to_numeric(df[col], errors='coerce')


    # Convert object columns that should be numeric
    numeric_columns = [
        'scoring_points_game', 'scoring_points_game_opp',
        'total_offense_yards___play', 'total_offense_yards___play_opp',
        'passing_rating', 'passing_rating_opp',
        'penalties_yards', 'penalties_yards_opp'
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # quick edits to the data to make it look nice
    df = df.drop(columns=['time_of_possession___game', 'time_of_possession___game_opp'], errors='ignore')
    df['time_possession_sec'].fillna(df['time_possession_sec'].mean(), inplace=True)

    # fill NA numeric cells w/ the column mean
    df.fillna(df.mean(numeric_only=True), inplace=True)

    return df

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Input file {INPUT_FILE} not found.")
        return

    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded raw data: {df.shape}")

    df_clean = clean_data(df)

    os.makedirs("data", exist_ok=True)
    df_clean.to_csv(OUTPUT_FILE, index=False)
    print(f"Cleaned data saved to {OUTPUT_FILE}")
    print(df_clean.head())

    # check data
    df_clean.info()
    df_clean.describe()

if __name__ == "__main__":
    main()
