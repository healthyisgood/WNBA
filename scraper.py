import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_wnba_player_stats(year=2024):
    url = "https://www.basketball-reference.com/wnba/years/{year}.html"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    table = soup.find('table', {'id': 'per_game_stats'})
    tables = pd.read_html(str(table))
if len(tables) == 0:
    raise ValueError("No tables found on the page. The website structure may have changed.")
    df = tables[0]

    df = df[df['Player'] != 'Player']
    df = df.fillna(0)

    for col in df.columns[5:]:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    keep = ['Player', 'Pos', 'Tm', 'MP', 'FG%', '3P%', 'FT%', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF',
            'PTS', 'FGA', 'FTA', '3PA']
    df = df[[col for col in keep if col in df.columns]]
    df = df.rename(columns={'MP': 'MIN', 'TRB': 'REB', 'TOV': 'TO'})
    return df.reset_index(drop=True)
