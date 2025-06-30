import streamlit as st
from scraper import get_wnba_player_stats
from predictor import WNBAPredictor
from context import fetch_news_snippets, analyze_sentiment
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="WNBA Predictor", layout="wide")
st.title("🏀 WNBA Player Matchup Predictor")

@st.cache_data
def load_model():
    df = get_wnba_player_stats()
    model = WNBAPredictor()
    model.train(df)
    return df, model

df, predictor = load_model()

player_list = sorted(df['Player'].unique())
p1 = st.selectbox("Player 1", player_list, index=0)
p2 = st.selectbox("Player 2", player_list, index=1)

if p1 != p2:
    r1 = df[df['Player'] == p1]
    r2 = df[df['Player'] == p2]
    matchup = pd.concat([r1, r2], ignore_index=True)
    prediction = predictor.predict(matchup)

    col1, col2 = st.columns(2)
    for i, (player, col) in enumerate(zip([p1, p2], [col1, col2])):
        with col:
            st.subheader(f"📊 {player}")
            st.metric("Points", prediction['PTS'][i])
            st.metric("Rebounds", prediction['REB'][i])
            st.metric("Assists", prediction['AST'][i])
            st.metric("Steals", prediction['STL'][i])
            st.metric("Blocks", prediction['BLK'][i])
            st.metric("Fantasy", prediction['FANTASY'][i])

            news = fetch_news_snippets(player)
            adj, flagged, sent = analyze_sentiment(news)
            if adj != 0:
                st.warning(f"Adjustment: {adj*100:+.0f}% — {len(news)} recent news items")
                for s in news:
                    st.caption("🗞️ " + s)

    categories = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FANTASY']
    fig = go.Figure([
        go.Bar(name=p1, x=categories, y=[prediction[c][0] for c in categories], marker_color='blue'),
        go.Bar(name=p2, x=categories, y=[prediction[c][1] for c in categories], marker_color='orange')
    ])
    fig.update_layout(barmode='group', title="Stat Comparison")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Choose two different players.")
