import pandas as pd
from sklearn.ensemble import RandomForestRegressor

class WNBAPredictor:
    def __init__(self):
        self.models = {}

    def train(self, player_stats_df):
        features = ['MIN', 'FGA', 'FG%', 'FTA', 'FT%', '3PA', '3P%', 'TO', 'PF']
        targets = ['PTS', 'REB', 'AST', 'STL', 'BLK']

        for stat in targets:
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(player_stats_df[features], player_stats_df[stat])
            self.models[stat] = model

    def predict(self, matchup_df):
        features = ['MIN', 'FGA', 'FG%', 'FTA', 'FT%', '3PA', '3P%', 'TO', 'PF']
        predictions = {}

        for stat, model in self.models.items():
            predictions[stat] = model.predict(matchup_df[features]).round(2)

        fantasy = (
            predictions['PTS'] +
            1.2 * predictions['REB'] +
            1.5 * predictions['AST'] +
            3.0 * predictions['STL'] +
            3.0 * predictions['BLK'] -
            1.0 * matchup_df['TO'].values
        ).round(2)

        predictions['FANTASY'] = fantasy
        return predictions
