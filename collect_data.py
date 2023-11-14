import requests
import datetime


def check_timeframe(news_list, lookback_days):
   # [Function description remains the same]
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


def fetch_latest_news(api_key, news_keywords, lookback_days=10,startdaysago=10,preferred_sources=None):
   if preferred_sources is None:
       preferred_sources = []
   # [Function description remains the same]
   today = datetime.date.today() - datetime.timedelta(days=startdaysago)
   lookback_date = today - datetime.timedelta(days=lookback_days)
   today_str = today.strftime("%Y-%m-%d")
   lookback_date_str = lookback_date.strftime("%Y-%m-%d")
   url = f"https://newsapi.org/v2/everything?q={news_keywords}&from={lookback_date_str}&to={today_str}&language=en&apiKey={api_key}"
   response = requests.get(url)


   if response.status_code != 200:
       print(f"Failed to fetch news. Status code: {response.status_code}")
       return []


   data = response.json()
   articles = data.get('articles', [])


   #if not check_timeframe(articles, lookback_days):
   #    print("Some articles are outside the specified timeframe.")
   #    return []


   # Filter articles by preferred sources
   filtered_articles = [article for article in articles if is_from_preferred_source(article, preferred_sources)]
   if len(filtered_articles)==0:
       print('no filt')
       return articles
   return filtered_articles


if __name__ == "__main__":
   api_key = "71e57d0e92d640e5b6d2a43e8c88f52e"#"ee459c38b2e54a7f9020c4db78d4b787"
   keywords = "movie"
   preferred_sources = ["Rotten Tomatoes", "Screen Rant", "Metacritic", "Movie Insider", "IMDb","New York Times","LA Times","Boing Boing","Wired"]
   totlist = []
   x=1
   y=0
   while (x,y)<(14,10000):
       news_list = fetch_latest_news(api_key, keywords, lookback_days=x,startdaysago=y,preferred_sources=None)
       totlist.extend(news_list)
       x+=2
       y+=2
  
   for article in totlist:
       #print(article['title'])
       print(article['url'])
       #print()
       #print(article['source']['id'])
   print(len(totlist))