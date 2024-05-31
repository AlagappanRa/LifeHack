import json
import pandas as pd
import spacy
import networkx as nx
import pickle
from transformers import pipeline
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Load SpaCy model
nlp = spacy.load('en_core_web_sm')

# Load the pre-trained question answering pipeline
qa_pipeline = pipeline("question-answering")

# Load the knowledge graph
with open("../knowledge_graph.gpickle", "rb") as f:
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

# Define a route for the chatbot
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    answer = chatbot(question)
    return jsonify({'question': question, 'answer': answer})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
