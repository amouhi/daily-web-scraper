import requests
import csv
import os
from datetime import datetime

def fetch_tech_headlines():
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("ERROR: NEWS_API_KEY is missing.")
        return

    # Generate dates
    now = datetime.now()
    today_date = now.strftime("%Y-%m-%d")
    file_date = now.strftime("%Y%m%d")
    
    # Ensure folder exists
    os.makedirs("files", exist_ok=True)

    # 1. ADD HEADERS: This is the missing piece that makes the script act like a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    # 2. URL (Same as yours, but with pageSize=20 to ensure we get a good batch)
    url = f"https://newsapi.org/v2/everything?q=azure&from={today_date}&sortBy=publishedAt&pageSize=20&apiKey={api_key}"
    
    try:
        # 3. Pass the headers into the request
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"API Error {response.status_code}: {response.text}")
            return

        data = response.json()
        articles = data.get("articles", [])
        
        # Log counts for debugging
        total_found = data.get('totalResults', 0)
        print(f"API reported total results: {total_found}")
        print(f"Articles received in this request: {len(articles)}")

        filename = f"files/scrapping_results_{file_date}.csv"

        # 4. Write to CSV
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
