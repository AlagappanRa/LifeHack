import pandas as pd

# Read URLs from urls.csv
try:
    with open('urls.csv', 'r') as file:
        urls = file.read().strip().split(',')
except FileNotFoundError:
    urls = []

# Read URLs from filtered_links.csv
try:
    with open('filtered_links.csv', 'r') as file:
        filtered_links = file.read().strip().split(',')
except FileNotFoundError:
    filtered_links = []

# Combine URLs and remove duplicates
combined_links = list(set(urls + filtered_links))

# Print the number of unique URLs
num_unique_urls = len(combined_links)
print(f"Number of unique URLs: {num_unique_urls}")

# Create a DataFrame from the combined links
combined_df = pd.DataFrame(combined_links, columns=['url'])

# Save the DataFrame to a new file
combined_df.to_csv('combined_links.csv', index=False)

print("Combined links saved to combined_links.csv")
