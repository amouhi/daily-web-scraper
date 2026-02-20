import requests
import csv
import os
from datetime import datetime

def fetch_tech_headlines():
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("ERROR: NEWS_API_KEY is missing.")
        return

    # Use today's date for both API 'from' and filename
    today_date = datetime.now().strftime("%Y-%m-%d")
    file_date = datetime.now().strftime("%Y%m%d")
    
    # Ensure folder 'files' exists
    folder_name = "files"
    os.makedirs(folder_name, exist_ok=True)

    # API query for Azure articles from today
    url = f"https://newsapi.org/v2/everything?q=azure&from={today_date}&sortBy=publishedAt&apiKey={api_key}"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"API Error {response.status_code}: {response.text}")
            return

        data = response.json()
        articles = data.get("articles", [])
        
        filename = os.path.join(folder_name, f"scrapping_results_{file_date}.csv")

        with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(["Source", "Headline", "URL", "Published At"])
            
            for article in articles:
                writer.writerow([
                    article.get('source', {}).get('name', 'Unknown'),
                    article.get('title', 'No Title'),
                    article.get('url', ''),
                    article.get('publishedAt', '')
                ])
        
        print(f"SUCCESS: Saved {len(articles)} articles to {filename}")
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    fetch_tech_headlines()
    
