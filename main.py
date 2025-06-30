from scraper import get_wnba_player_stats
from predictor import WNBAPredictor
from context import fetch_news_snippets, analyze_sentiment
import pandas as pd

def get_player_input(df, name):
    player = df[df['Player'].str.lower() == name.lower()]
    if player.empty:
        raise ValueError(f"Player '{name}' not found.")
    return player

def format_output(name, prediction, i):
    print(f"\n📊 Prediction for {name}")
    print("-" * 30)
    for stat in ['PTS', 'REB', 'AST', 'STL', 'BLK']:
        print(f"{stat}: {prediction[stat][i]}")
    print(f"FANTASY SCORE: {prediction['FANTASY'][i]}")
    print("-" * 30)

def main():
    print("📥 Loading WNBA stats...")
    df = get_wnba_player_stats()
    predictor = WNBAPredictor()
    predictor.train(df)

    print("✅ Loaded. Example players:")
    print(df['Player'].sample(5).to_string(index=False))

    p1 = input("Enter first player name: ")
    p2 = input("Enter second player name: ")

    try:
        row1 = get_player_input(df, p1)
        row2 = get_player_input(df, p2)
        combined = pd.concat([row1, row2], ignore_index=True)
        predictions = predictor.predict(combined)

        format_output(p1, predictions, 0)
        format_output(p2, predictions, 1)

        # Add context sentiment info
        for i, name in enumerate([p1, p2]):
            news = fetch_news_snippets(name)
            adj, flagged, sentiment = analyze_sentiment(news)
            if adj != 0 or flagged:
                print(f"\n🗞️ Context for {name}:")
                for s in news:
                    print(" •", s)
                print(f"Adjustment: {adj*100:+.0f}% due to recent news/sentiment")

    except ValueError as e:
        print(f"❌ {e}")

if __name__ == "__main__":
    main()
