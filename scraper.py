import requests
import csv
import os
from datetime import datetime

def fetch_tech_headlines():
    # 1. Load API Key from GitHub Secrets
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("ERROR: NEWS_API_KEY environment variable is empty. Check your GitHub Secrets.")
        return

    # 2. Setup Dates and Folder
    now = datetime.now()
    today_date = now.strftime("%Y-%m-%d")  # For API query (YYYY-MM-DD)
    date_str = now.strftime("%Y%m%d")      # For Filename (YYYYMMDD)
    
    folder_name = "files"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created folder: {folder_name}")

    # 3. Construct the URL (Topic: Azure)
    url = f"https://newsapi.org/v2/everything?q=azure&from={today_date}&sortBy=publishedAt&apiKey={api_key}"
    
    try:
        response = requests.get(url)

        # 4. Error Handling for API Response
        if response.status_code != 200:
            print(f"FAILED: Status Code {response.status_code}")
            print(f"RAW RESPONSE BODY: {response.text}")
            return

        # 5. Parse JSON and Extract Articles
        data = response.json()
        articles = data.get("articles", [])
        
        # Check if list is empty
        if not articles:
            print(f"No articles found for {today_date} yet. CSV will be empty.")

        # 6. Save to CSV inside the 'files' folder
        filename = f"{folder_name}/scrapping_results_{date_str}.csv"

        with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(["Source", "Headline", "URL", "Published At"])
            
            rows_count = 0
            for article in articles:
                # Use .get() to avoid KeyErrors if some data is missing
                source_name = article.get('source', {}).get('name', 'Unknown')
                title = article.get('title', 'No Title')
                link = article.get('url', '')
                published = article.get('publishedAt', '')
                
                writer.writerow([source_name, title, link, published])
                rows_count += 1
        
        print(f"Successfully saved {rows_count} rows to {filename}")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    fetch_tech_headlines()
