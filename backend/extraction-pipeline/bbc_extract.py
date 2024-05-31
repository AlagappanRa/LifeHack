import pandas as pd

# Define the list of keywords related to terrorism
keywords = ['terrorism', 'terrorist', 'terror attack', 'bombing', 'extremism', 'militant', 'radicalization']

# Read the CSV file
df = pd.read_csv('bbc_news.csv')

# Function to check if any keyword is in the text
def contains_keywords(text, keywords):
    if isinstance(text, str):
        return any(keyword.lower() in text.lower() for keyword in keywords)
    return False

# Filter articles containing keywords in the title or description
filtered_df = df[df['title'].apply(lambda x: contains_keywords(x, keywords)) | df['description'].apply(lambda x: contains_keywords(x, keywords))]

# Extract links
links = filtered_df['link'].tolist()
links_str = ",".join(links)

# Save to file
with open('filtered_links.csv', 'w') as file:
    file.write(links_str)

print("Filtered links saved to filtered_links.csv")
