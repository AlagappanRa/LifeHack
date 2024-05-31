import json
import pandas as pd
import spacy
import networkx as nx
import matplotlib.pyplot as plt
from transformers import pipeline
import pickle

## 1. Entity Extraction
# Load SpaCy model
nlp = spacy.load('en_core_web_sm')

# Load cleaned JSON data
with open('backend/cleaned_content_dataset.json', 'r', encoding='utf-8') as file:
    cleaned_data = json.load(file)

# Convert JSON data to DataFrame
df = pd.DataFrame(cleaned_data)

# Entity extraction function focusing on relevant entities
def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in {"PERSON", "ORG", "GPE", "LOC", "EVENT", "DATE"}]
    return entities

# Apply entity extraction to the cleaned text column
df['entities'] = df['cleaned_text'].apply(extract_entities)

# Save the data with extracted entities to a new JSON file
output_data_with_entities = df.to_dict(orient='records')

with open('backend/content_with_entities.json', 'w', encoding='utf-8') as outfile:
    json.dump(output_data_with_entities, outfile, indent=4)

print("Data with extracted entities saved to content_with_entities.json")

## 2. Knowledge Graph Creation
# Create a knowledge graph
G = nx.Graph()

# Add entities and relationships to the graph
for entry in df['entities']:
    previous_entity = None
    for ent in entry:
        G.add_node(ent[0], label=ent[1])
        if previous_entity:
            G.add_edge(previous_entity[0], ent[0])
        previous_entity = ent

# Save the knowledge graph to a file using pickle
with open("knowledge_graph.gpickle", "wb") as f:
    pickle.dump(G, f)

print("Knowledge graph created and saved to knowledge_graph.gpickle")

##3. QA Chatbot with Knowledge Graph

# Load the pre-trained question answering pipeline
qa_pipeline = pipeline("question-answering")

# Load the knowledge graph
with open("knowledge_graph.gpickle", "rb") as f:
    G = pickle.load(f)

# Function to create a context from the knowledge graph
def create_context(node):
    neighbors = list(G.neighbors(node))
    context = f"{node} is related to: " + ", ".join(neighbors)
    return context

# Chatbot function
def chatbot(question):
    # Extract possible entities from the question
    doc = nlp(question)
    entities = [ent.text for ent in doc.ents]
    
    # Create a context from the knowledge graph
    context = ""
    for entity in entities:
        if G.has_node(entity):
            context += create_context(entity) + " "
    
    if not context:
        return "I don't have enough information to answer that question."
    
    # Use the QA model to answer the question
    result = qa_pipeline(question=question, context=context)
    return result['answer']

# Example questions
questions = [
    "Who escaped from the prison?",
    "Where did the terrorist attack happen?",
    "What is the name of the suspect?"
]

# Answer questions
for question in questions:
    answer = chatbot(question)
    print(f"Question: {question}\nAnswer: {answer}\n")

