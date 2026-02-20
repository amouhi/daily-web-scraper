import requests
import csv
import os
import time
from datetime import datetime, timedelta

def cleanup_old_files(folder_path, days_to_keep=30):
    """Deletes files in the specified folder older than days_to_keep."""
    if not os.path.exists(folder_path):
        return
    
    # Calculate the cutoff time in seconds
    now = time.time()
    cutoff = now - (days_to_keep * 86400)
    
    deleted_count = 0
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Check if it's a file and if its last modified time is older than the cutoff
        if os.path.isfile(file_path):
            if os.path.getmtime(file_path) < cutoff:
                os.remove(file_path)
                print(f"Deleted old file: {filename}")
                deleted_count += 1
    
    if deleted_count > 0:
        print(f"Cleanup finished. Removed {deleted_count} files older than {days_to_keep} days.")

def fetch_tech_headlines():
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("ERROR: NEWS_API_KEY is missing.")
        return

    file_date = datetime.now().strftime("%Y%m%d")
    folder_name = "files"
    os.makedirs(folder_name, exist_ok=True)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    # API query for Azure
    url = f"https://newsapi.org{api_key}"
    
    try:
        response = requests.get(url, headers=headers)
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
        
        # --- NEW: Run cleanup after saving the new file ---
        cleanup_old_files(folder_name, days_to_keep=3)
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    fetch_tech_headlines()
        
