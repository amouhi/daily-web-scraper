import requests
import csv
import os
from datetime import datetime

def fetch_tech_headlines():
    api_key = os.getenv("NEWS_API_KEY")
    
    # get today's date
    today_date = datetime.now().strftime("%Y-%m-%d")
    # 1. Check if the secret is actually being loaded
    if not api_key:
        print("ERROR: NEWS_API_KEY environment variable is empty. Check your GitHub Secrets.")
        return

    # 2. Construct the URL carefully (verify the slash after .org)
    url = f"https://newsapi.org/v2/everything?q=azure&from={today_date}&sortBy=publishedAt&apiKey={api_key}"
    
    response = requests.get(url)

    # 3. Debugging: If not 200 OK, print the raw response to see the real error
    if response.status_code != 200:
        print(f"FAILED: Status Code {response.status_code}")
        print(f"RAW RESPONSE BODY: {response.text}") # This will show you exactly what is wrong
        return

    # 4. Attempt to parse JSON only after confirming it's a successful response
    try:
        data = response.json()
        articles = data.get("articles", [])
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"scrapping_results_{date_str}.csv"

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Source", "Headline", "URL", "Published At"])
            for article in articles:
                writer.writerow([article['source']['name'], article['title'], article['url'], article['publishedAt']])
        print(f"Successfully saved to {filename}")
        
    except requests.exceptions.JSONDecodeError:
        print("ERROR: Could not decode JSON. The server response was:")
        print(response.text)

if __name__ == "__main__":
    fetch_tech_headlines()
        
