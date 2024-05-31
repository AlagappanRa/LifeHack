import pandas as pd
import requests
import time

def fetch_gdelt_data(keyword, start_date, end_date, max_records):
    all_articles = []
    records_per_request = 250
    num_requests = max_records // records_per_request
    
    for i in range(num_requests):
        start_record = i * records_per_request
        url = (f'https://api.gdeltproject.org/api/v2/doc/doc?query={keyword}'
               f'&mode=artlist&maxrecords={records_per_request}&startrecord={start_record}'
               f'&startdatetime={start_date}&enddatetime={end_date}&format=json')
        response = requests.get(url)
        
        if response.status_code == 200:
            try:
                data = response.json()
                if 'articles' in data:
                    all_articles.extend(data['articles'])
                else:
                    break  # No more articles to fetch
            except requests.exceptions.JSONDecodeError:
                print("Error decoding JSON response:")
                print(response.text)
                break
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            print(response.text)
            break
        
        time.sleep(1)  # To avoid hitting API rate limits
    
    return all_articles

# Define the list of keywords related to terrorism
keywords = ['terrorism', 'terrorist', 'terror attack', 'bombing', 'extremism', 'militant', 'radicalization']

# Date range to cover the past year
start_date = '20220101000000'
end_date = '20221231235959'

all_articles_data = []
max_records_per_keyword = 5000

# Fetch articles for each keyword
for keyword in keywords:
    articles_data = fetch_gdelt_data(keyword, start_date, end_date, max_records_per_keyword)
    if articles_data:
        all_articles_data.extend(articles_data)
    print(f"Fetched {len(articles_data)} articles for keyword: {keyword}")

# Create a DataFrame from the collected articles
if all_articles_data:
    articles_df = pd.json_normalize(all_articles_data)
    print(f"Total number of articles fetched: {len(articles_df)}")
    
    # Filter for English language articles
    english_articles_df = articles_df[articles_df['language'] == 'English']
    print(f"Total number of English language articles: {len(english_articles_df)}")
    
    print(english_articles_df.columns)
    print(english_articles_df.head())
    
    # Extract URLs and save as comma-separated list
    urls = english_articles_df['url'].tolist()
    urls_str = ",".join(urls)
    
    # Save to file
    with open('urls.csv', 'w') as file:
        file.write(urls_str)
    
    print("URLs saved to urls.csv")
else:
    print("No data fetched.")
