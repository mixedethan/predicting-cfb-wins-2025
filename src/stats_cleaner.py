import pandas as pd
import os
import numpy as np

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

def create_net_stat_column(df, base_stat_name, decimals=4):
    
    team_col = base_stat_name
    opp_col = base_stat_name + '_opp'
    net_col_name = 'net_' + base_stat_name

    # check stat columns exist
    if team_col not in df.columns or opp_col not in df.columns:
        print(f"Warning: Cannot calculate '{net_col_name}'.")
        df[net_col_name] = np.nan
        return df

    for col in [team_col, opp_col]:
        if df[col].dtype == 'object':
             df[col] = df[col].astype(str).str.replace(',', '', regex=False).str.strip()
             df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col].fillna(df[col].mean(), inplace=True)

    # special handling since we refer opponent minus team for penalties yards.
    if base_stat_name == 'penalties_yards':
        df[net_col_name] = df[opp_col] - df[team_col]
    else:
        df[net_col_name] = df[team_col] - df[opp_col]

    df[net_col_name] = df[net_col_name].round(decimals)

    return df

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
            df[col] = df[col].astype(str).str.replace(',', '', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # convert the time to seconds
    df['time_possession_sec'] = df['time_of_possession___game'].apply(time_to_sec)
    df['time_possession_sec_opp'] = df['time_of_possession___game_opp'].apply(time_to_sec)

    # convert everything to numeric data type
    for col in df.columns:
        if col not in ['team', 'year']:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip()
                df[col] = df[col].str.replace(',', '', regex=False)
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
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip()
                df[col] = df[col].str.replace(',', '', regex=False)

            df[col] = pd.to_numeric(df[col], errors='coerce')

    # quick edits to the data to make it look nice
    df = df.drop(columns=['time_of_possession___game', 'time_of_possession___game_opp'], errors='ignore')
    df['time_possession_sec'].fillna(df['time_possession_sec'].mean(), inplace=True)

    ### --- derived stats ---

    # win_percentage
    for col in ['wins', 'losses']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    if 'wins' in df.columns and 'losses' in df.columns:
        total_games = df['wins'] + df['losses']
        df['win_percentage'] = df['wins'] / total_games
        df['win_percentage'].fillna(0, inplace=True)
    else:
        print("Warning: Couldn't calculate win percentage!")
    
    # turnover_margin
    turnover_cols = [
        'interceptions_returns', 'fumbles_lost_opp',
        'pass_ints', 'fumbles_lost'
    ]

    for col in turnover_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        else:
            print("Warning: Not all turnover columns are available")
            df[col] = 0
    
    if all(col in df.columns for col in turnover_cols):
        df['turnovers_gained'] = df['interceptions_returns'] + df['fumbles_lost_opp']
        df['turnovers_committed'] = df['pass_ints'] + df['fumbles_lost']
        df['turnover_margin'] = df['turnovers_gained'] - df['turnovers_committed']
    else:
        print('Warning: Not all turnover columns were found.')
        df = df.drop(columns=[col for col in turnover_cols if col not in ['interceptions_returns', 'fumbles_lost_opp', 'pass_ints', 'fumbles_lost']], errors='ignore')

    net_stats_to_create = [
        'scoring_points_game',
        'total_offense_yards___play',
        'red_zone_success_pct',
        'time_possession_sec',
        'penalties_yards'
    ]

    for base_stat in net_stats_to_create:
        df = create_net_stat_column(df, base_stat)
    
    # final check to fill NA numeric cells w/ the column mean
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
