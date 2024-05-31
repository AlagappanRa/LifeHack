import json
import pandas as pd
import re
import spacy
import subprocess
import sys
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

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

# Ensure NLTK stopwords are downloaded
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Load JSON data with UTF-8 encoding
with open('content_dataset.json', 'r', encoding='utf-8-sig') as file:
    data = json.load(file)

# Convert JSON data to DataFrame
df = pd.DataFrame(data)

# Define a regex pattern to match URLs
url_pattern = re.compile(r'https?://\S+')

# Preprocessing function
def preprocess_text(text):
    # Remove URLs
    text = url_pattern.sub('', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove non-word and non-whitespace characters
    text = re.sub(r'[^\w\s]', '', text)
    # Remove digits
    text = re.sub(r'\d+', '', text)
    # Lowercase text
    text = text.lower()
    # Tokenization
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    # Lemmatization
    doc = nlp(' '.join(tokens))
    lemmas = [token.lemma_ for token in doc]
    return ' '.join(lemmas)

# Apply preprocessing to the text column
df['cleaned_text'] = df['text'].apply(preprocess_text)

# Save the cleaned data to a new JSON file
output_data = df.to_dict(orient='records')

with open('cleaned_content_dataset.json', 'w', encoding='utf-8') as outfile:
    json.dump(output_data, outfile, indent=4)

print("Preprocessed data saved to cleaned_content_dataset.json")