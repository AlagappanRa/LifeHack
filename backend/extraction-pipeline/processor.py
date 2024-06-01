import json
import re

# Load the JSON data from the input file
with open('backend/cleaned_content_dataset.json', 'r') as file:
    data = json.load(file)

# Define a function to preprocess the cleaned text
def preprocess_text(text):
    # Remove the "Part of HuffPost...All rights reserved." section
    text = re.sub(r'Part of HuffPost.*?All rights reserved\.', '', text)
    # Remove the "Location, date (Reuters)" sections
    text = re.sub(r'\b[A-Z]+(?:\/[A-Z]+)?(?:, [A-Z][a-z]+)?(?: [A-Z][a-z]+)? \(Reuters\)', '', text)
    text = re.sub(r'\b[A-Z]+\/[A-Z]+(?:, [A-Z][a-z]+)?(?: [A-Z][a-z]+)? \d{1,2} \(Reuters\)', '', text)
    text = re.sub(r'\b[A-Z][a-z]+, [A-Z][a-z]+(?: [A-Z][a-z]+)? \d{1,2} \(Reuters\)', '', text)
    # Remove entries that start with "As Americans head to the polls in 2024,"
    text = re.sub(r'^As Americans head to the polls in 2024,.*', '', text)
    # Remove extra spaces and newlines
    text = text.strip()
    return text

# Process each entry in the data
processed_data = []
for entry in data:
    if 'cleaned_text' in entry:
        output = preprocess_text(entry['cleaned_text'])
        if output: 
            print("text: ", output[:100])
            processed_data.append({"text": output})
        

# Save the processed data to the output file
with open('output.json', 'w') as file:
    json.dump(processed_data, file, indent=1)

print("Processed data saved to output.json")
