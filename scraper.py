import requests
import csv
import os
from datetime import datetime

def fetch_tech_headlines():
    # Load API key from GitHub Secrets
    api_key = os.getenv("NEWS_API_KEY")
    # Endpoint for 10 US technology headlines
    url = f"https://newsapi.org{api_key}"
    
    response = requests.get(url)
    data = response.json()

    if data.get("status") == "ok":
        articles = data.get("articles", [])
        
        # Filename format: scrapping_results_YYYYMMDD.csv
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"scrapping_results_{date_str}.csv"

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Source", "Headline", "URL", "Published At"])
            
            for article in articles:
                writer.writerow([
                    article['source']['name'],
                    article['title'],
                    article['url'],
                    article['publishedAt']
                ])
        print(f"Successfully saved 10 technology headlines to {filename}")
    else:
        print(f"Error: {data.get('message', 'Unknown error occurred')}")

if __name__ == "__main__":
    fetch_tech_headlines()
      
