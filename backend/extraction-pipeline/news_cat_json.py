import pandas as pd
import json

# Define the list of keywords related to terrorism
keywords = ['terrorism', 'terrorist', 'terror attack', 'bombing', 'extremism', 'militant', 'radicalization']

# Load the JSON file
with open('News_Category_Dataset_v3.json', 'r') as file:
    data = [json.loads(line) for line in file]

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Function to check if any keyword is in the text
def contains_keywords(text, keywords):
    if isinstance(text, str):
        return any(keyword.lower() in text.lower() for keyword in keywords)
    return False

# Filter articles containing keywords in the headline or short_description
filtered_df = df[df['headline'].apply(lambda x: contains_keywords(x, keywords)) | df['short_description'].apply(lambda x: contains_keywords(x, keywords))]

# Extract links
new_links = filtered_df['link'].tolist()

# Read existing links from the CSV file
try:
    with open('filtered_links.csv', 'r') as file:
        existing_links = file.read().strip().split(',')
except FileNotFoundError:
    existing_links = []

# Combine new links with existing links, avoiding duplicates
combined_links = list(set(existing_links + new_links))
combined_links_str = ",".join(combined_links)

# Save to file
with open('filtered_links.csv', 'w') as file:
    file.write(combined_links_str)

print("Filtered links appended to filtered_links.csv")
