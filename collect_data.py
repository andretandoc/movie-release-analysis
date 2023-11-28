import requests 
import datetime
import json
from pathlib import Path
import os
import re

CACHE_FILE = 'news_cache.json'
API_KEY = "71e57d0e92d640e5b6d2a43e8c88f52e"

def load_cache():
    if os.path.exists(CACHE_FILE):
        # Check if the file is empty
        if os.path.getsize(CACHE_FILE) > 0:
            with open(CACHE_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            print("Cache file is empty.")
            return {}
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as file:
        json.dump(cache, file, ensure_ascii=False, indent=4)

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

def fetch_latest_news(api_key, news_keywords, lookback_days=1, startdaysago=1, preferred_sources=None):
    if preferred_sources is None:
        preferred_sources = []
    
    cache = load_cache()

    today = datetime.date.today() - datetime.timedelta(days=startdaysago)

    # Fetch news for each day over the past month
    totlist = []
    for i in range(15):
        lookback_date = today - datetime.timedelta(days=lookback_days)
        today_str = today.strftime("%Y-%m-%d")
        lookback_date_str = lookback_date.strftime("%Y-%m-%d")

        # Check if data is already in the cache
        cache_key = f"{lookback_date_str}_{today_str}"

        if cache_key in cache:
            print(f"Fetching from cache for date range: {lookback_date_str} to {today_str}")
            data = cache[cache_key]
            articles = data
        else:
            url = f"https://newsapi.org/v2/everything?q={news_keywords}&from={lookback_date_str}&to={today_str}&language=en&apiKey={api_key}"
            response = requests.get(url)

            if response.status_code != 200:
                print(f"Failed to fetch news. Status code: {response.status_code}")
                continue  # Skip to the next iteration if fetching fails

            data = response.json()
            # Save data to cache
            new_articles = data.get('articles', [])
            cache[cache_key] = new_articles
            save_cache(cache)
            articles = data.get('articles', [])

        # Filter articles by preferred sources
        filtered_articles = [article for article in articles if is_from_preferred_source(article, preferred_sources)]
        if not filtered_articles:
            print(f'No articles from preferred sources in the cache for date range: {lookback_date_str} to {today_str}')
            totlist.extend(articles)
        else:
            totlist.extend(filtered_articles)

        # Move to the previous day without overlap
        today -= datetime.timedelta(days=2)
    return totlist

def filter_articles_by_content(articles):
    """
    Filter a list of articles based on content containing both "movie" and "review."

    Args:
    - articles (list): List of articles with content.

    Returns:
    - list: Filtered list of articles.
    """
    def content_filter(content):
        return "movie" in content.lower() 

    filtered_articles = [article for article in articles if content_filter(article.get('content', ''))]

    return filtered_articles

def main():
   # keywords = '"November 2023 movie review" OR "2023 movie"'
    #keywords = '"Mavels movie 2023" OR " Marvels review"'
    keywords = (
    '"movie review" OR "film review" OR "2023 movie" OR "best movies 2023" OR '
    '"upcoming films" OR "box office" OR "Oscar nominations" OR '
    '"directed by" OR "starring" OR "awards season" OR "film premiere" OR '
    '"celebrity interviews" OR "blockbuster movies 2023"'
)
    preferred_sources = ["Rotten Tomatoes", "Screen Rant", "Metacritic", "Movie Insider", "IMDb", "New York Times", "LA Times", "Boing Boing", "Wired"]
    totlist = fetch_latest_news(API_KEY, keywords, lookback_days=1, startdaysago=1, preferred_sources=None)

    #for article in totlist:
        #print(article['url'])
            
    print(f"Total number of articles: {len(totlist)}")

    cache = load_cache()
    filtered_json_data = {}
    for date, articles in cache.items():
        filtered_articles = filter_articles_by_content(articles)
        filtered_json_data[date] = filtered_articles

    # Save filtered articles to a new JSON file
    filtered_json = {'articles': filtered_json_data}
    with open('filtered_news.json', 'w', encoding='utf-8') as json_file:
        json.dump(filtered_json, json_file, ensure_ascii=False, indent=4)

    print(f"Filtered articles saved to 'filtered_news.json'.")

    # Print the count of articles in the new JSON
    article_count = sum(len(articles) for articles in filtered_json_data.values())
    print(f"Number of articles in the new JSON: {article_count}")

if __name__ == "__main__":
    main()