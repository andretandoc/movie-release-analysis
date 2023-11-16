import requests
import datetime
import json
from pathlib import Path
import os

CACHE_FILE = 'news_cache.json'

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as file:
        json.dump(cache, file)

def check_timeframe(news_list, lookback_days):
    today = datetime.date.today()
    lookback_date = today - datetime.timedelta(days=lookback_days)
    for article in news_list:
        article_date = datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").date()
        if article_date < lookback_date:
            return False
    return True

def is_from_preferred_source(article, preferred_sources):
    # Check if the article's source is in the preferred sources list
    source_name = article['source']['name'].lower()
    return any(preferred_source.lower() in source_name for preferred_source in preferred_sources)

def fetch_latest_news(api_key, news_keywords, lookback_days=10, startdaysago=10, preferred_sources=None):
    if preferred_sources is None:
        preferred_sources = []
    
    cache = load_cache()

    today = datetime.date.today() - datetime.timedelta(days=startdaysago)
    lookback_date = today - datetime.timedelta(days=lookback_days)
    today_str = today.strftime("%Y-%m-%d")
    lookback_date_str = lookback_date.strftime("%Y-%m-%d")

    # Check if data is already in the cache
    cache_key = f"{lookback_date_str}_{today_str}"

    if cache_key in cache:
        print("Fetching from cache...")
        data = cache[cache_key]
    else:
        url = f"https://newsapi.org/v2/everything?q={news_keywords}&from={lookback_date_str}&to={today_str}&language=en&apiKey={api_key}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to fetch news. Status code: {response.status_code}")
            return []

        data = response.json()
        # Save data to cache
        new_articles = data.get('articles', [])
        cache[cache_key] = new_articles
        save_cache(cache)

    articles = data.get('articles', [])

    # Filter articles by preferred sources
    filtered_articles = [article for article in articles if is_from_preferred_source(article, preferred_sources)]
    if not filtered_articles:
        print('No articles from preferred sources in the cache.')
        return articles

    return filtered_articles

if __name__ == "__main__":
    api_key = "71e57d0e92d640e5b6d2a43e8c88f52e"
    keywords = "movie"
    preferred_sources = ["Rotten Tomatoes", "Screen Rant", "Metacritic", "Movie Insider", "IMDb", "New York Times", "LA Times", "Boing Boing", "Wired"]
    totlist = []
    x = 1
    y = 0
    while (x, y) < (14, 10000):
        news_list = fetch_latest_news(api_key, keywords, lookback_days=x, startdaysago=y, preferred_sources=None)
        totlist.extend(news_list)
        x += 2
        y += 2

    for article in totlist:
        print(article['url'])
        
    print(len(totlist))
