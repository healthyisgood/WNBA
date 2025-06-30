import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

def fetch_news_snippets(player_name):
    query = f"{player_name} WNBA news"
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}&hl=en"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        snippets = [s.get_text() for s in soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')]
        return snippets[:5]
    except Exception as e:
        return [f"Error fetching news: {e}"]

def analyze_sentiment(snippets):
    score = 0
    injury_flag = False
    keywords = ['injury', 'hurt', 'ankle', 'out', 'rest', 'sore', 'personal', 'miss']

    for snippet in snippets:
        score += TextBlob(snippet).sentiment.polarity
        if any(k in snippet.lower() for k in keywords):
            injury_flag = True

    avg_sentiment = score / len(snippets) if snippets else 0
    if injury_flag:
        adjustment = -0.10
    elif avg_sentiment < -0.2:
        adjustment = -0.05
    elif avg_sentiment > 0.2:
        adjustment = +0.05
    else:
        adjustment = 0

    return adjustment, injury_flag, avg_sentiment
