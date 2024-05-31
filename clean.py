import json
import pandas as pd
import re
import spacy
import subprocess
import sys

# Function to install SpaCy model if not already installed
def install_spacy_model():
    try:
        nlp = spacy.load('en_core_web_sm')
    except OSError:
        print("Downloading SpaCy model 'en_core_web_sm'...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        nlp = spacy.load('en_core_web_sm')
    return nlp

# Install and load SpaCy model
nlp = install_spacy_model()

# Load JSON data with UTF-8 encoding
with open('content_dataset.json', 'r', encoding='utf-8-sig') as file:
    data = json.load(file)

# Convert JSON data to DataFrame
df = pd.DataFrame(data)

# Preprocessing function
def preprocess_text(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove punctuation and numbers
    text = re.sub(r'[^\w\s]', '', text)
    # Lowercase text
    text = text.lower()
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    # Tokenization and lemmatization
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop]
    return ' '.join(tokens)

# Apply preprocessing to the text column
df['cleaned_text'] = df['text'].apply(preprocess_text)

# Save the cleaned data to a new JSON file
output_data = df.to_dict(orient='records')

with open('cleaned_content_dataset.json', 'w', encoding='utf-8') as outfile:
    json.dump(output_data, outfile, indent=4)

print("Preprocessed data saved to cleaned_content_dataset.json")
