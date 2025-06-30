import pandas as pd
from sklearn.ensemble import RandomForestRegressor

class WNBAPredictor:
    def __init__(self):
        self.models = {}

    def train(self, player_stats_df):
        # Define input features and target stats
        features = ['MIN', 'FGA', 'FG%', 'FTA', 'FT%', '3PA', '3P%', 'TO', 'PF']
        targets = ['PTS', 'REB', 'AST', 'STL', 'BLK']

        # Only keep features that exist in the dataset
        available_features = [f for f in features if f in player_stats_df.columns]

        for stat in targets:
            if stat not in player_stats_df.columns:
                print(f"⚠️ Skipping model training for missing stat: {stat}")
                continue

            try:
                model = RandomForestRegressor(n_estimators=100, random_state=42)
                model.fit(player_stats_df[available_features], player_stats_df[stat])
                self.models[stat] = model
            except Exception as e:
                print(f"❌ Error training model for {stat}: {e}")

    def predict(self, matchup_df):
        # Define features to use for prediction
        features = ['MIN', 'FGA', 'FG%', 'FTA', 'FT%', '3PA', '3P%', 'TO', 'PF']
        available_features = [f for f in features if f in matchup_df.columns]

        predictions = {}

        for stat, model in self.models.items():
            try:
                preds = model.predict(matchup_df[available_features])
                predictions[stat] = preds.round(2)
            except Exception as e:
                print(f"❌ Prediction failed for {stat}: {e}")
                predictions[stat] = [0.0] * len(matchup_df)

        # Calculate fantasy score (basic scoring format)
        try:
            fantasy = (
                predictions.get('PTS', 0) +
                1.2 * predictions.get('REB', 0) +
                1.5 * predictions.get('AST', 0) +
                3.0 * predictions.get('STL', 0) +
                3.0 * predictions.get('BLK', 0) -
                1.0 * matchup_df.get('TO', pd.Series([0] * len(matchup_df))).values
            ).round(2)
        except Exception as e:
            print(f"⚠️ Fantasy score calculation failed: {e}")
            fantasy = [0.0] * len(matchup_df)

        predictions['FANTASY'] = fantasy
        return predictions
