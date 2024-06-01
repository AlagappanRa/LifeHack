import streamlit as st
import time
import pickle
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import boto3
import os

# Access secrets
aws_access_key_id = st.secrets["default"]["aws_access_key_id"]
aws_secret_access_key = st.secrets["default"]["aws_secret_access_key"]

# Create S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# Function to download files from S3
def download_from_s3(bucket_name, file_key, download_path):
    s3.download_file(bucket_name, file_key, download_path)

# Load necessary resources with error handling
@st.cache_resource
def load_resources():
    try:
        # Define S3 bucket and file paths
        bucket_name = "securegpt"
        data_file_key = "data_with_embeddings.pkl"
        faiss_index_key = "faiss_index.bin"

        # Define local paths to save the downloaded files
        data_file_path = "data_with_embeddings.pkl"
        faiss_index_path = "faiss_index.bin"

        # Download the files from S3
        download_from_s3(bucket_name, data_file_key, data_file_path)
        download_from_s3(bucket_name, faiss_index_key, faiss_index_path)

        # Load the Faiss index
        index = faiss.read_index(faiss_index_path)

        # Load the data
        df = pd.read_pickle(data_file_path)

        # Load the sentence transformer model
        semantic_model = SentenceTransformer('all-MiniLM-L6-v2')

        # Load the question answering pipeline with a specific model
        qa_pipeline = pipeline("question-answering", model="distilbert/distilbert-base-cased-distilled-squad")

        return index, df, semantic_model, qa_pipeline

    except Exception as e:
        st.error(f"Error loading resources: {e}")
        raise

index, df, semantic_model, qa_pipeline = load_resources()

def process_query(user_input):
    # Perform semantic search to get the most relevant text segments
    query_embedding = semantic_model.encode([user_input])
    distances, indices = index.search(np.array(query_embedding), 3)
    results = df.iloc[indices[0]]

    # Combine the retrieved text into a single context
    context = " ".join(results['cleaned_text'].tolist())
    
    # Generate the answer using the QA model
    response = qa_pipeline(question=user_input, context=context)
    return response['answer']

# Initialize chat history if not already present
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = ""

# Custom CSS for dark theme
st.markdown("""
<style>
    .css-18e3th9 {
        background-color: #121212;
        color: #fff;
    }
    .css-1d391kg {
        background-color: #333333;
        color: #fff;
    }
    .st-bx {
        color: #fff;
    }
    .st-ae {
        color: #fff;
    }
    .st-bw {
        color: #fff;
    }
    .st-bq {
        color: #fff;
    }
    .st-bc {
        color: #fff;
    }
    body {
        color: #fff;
    }
    h1 {
        color: #0d6efd;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #0d6efd;'>SecureGPT</h1>", unsafe_allow_html=True)
st.markdown("This chatbot provides information about terrorism events over the past year. Please type your queries below. The knowledge of this bot is generated from knowledge graphs.", unsafe_allow_html=True)

# Sidebar for navigation
with st.sidebar:
    st.header("Navigate")
    if st.button('Clear Chat'):
        st.session_state['chat_history'] = ""
    if st.button("View Chat"):
        st.session_state['current_page'] = 'chat'
    if st.button("About: Knowledge Graph"):
        st.session_state['current_page'] = 'knowledge'

# Decide which page to display
if 'current_page' in st.session_state and st.session_state['current_page'] == 'knowledge':
    st.subheader("Knowledge")
    st.write("What the model can answer.")
elif 'current_page' in st.session_state and st.session_state['current_page'] == 'chat':
    # User query input
    user_input = st.text_input("Enter your query here:", key="user_input")
    
    # Placeholder for response while processing
    placeholder = st.empty()
    
    if st.button('Send'):
        # Show loading message
        with placeholder.container():
            st.markdown(
                """
                <div style="text-align: center;">
                    <label>Processing...</label>
                    <br>
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            response = process_query(user_input)
            placeholder.empty()  # Clear the placeholder after processing
            
        st.session_state['chat_history'] += f"You: {user_input}\nChatbot: {response}\n"
    
    st.text_area("Chat History:", value=st.session_state['chat_history'], height=300, key="display_chat_history")
else:
    # Default view when the page loads for the first time or current_page is not set
    user_input = st.text_input("Enter your query here:", key="user_input")
    placeholder = st.empty()
    
    if st.button('Send'):
        with placeholder.container():
            st.markdown(
                """
                <div style="text-align: center;">
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            response = process_query(user_input)
            placeholder.empty()  # Clear the placeholder after processing
        
        st.session_state['chat_history'] += f"You: {user_input}\nChatbot: {response}\n"
    
    st.text_area("Chat History:", value=st.session_state['chat_history'], height=300, key="display_chat_history")

st.markdown("---")