import streamlit as st
import time
import pickle
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# Load necessary resources
@st.cache_resource
def load_resources():
    # Load the Faiss index and data
    index = faiss.read_index("faiss_index.bin")
    df = pd.read_pickle("data_with_embeddings.pkl")

    # Load the sentence transformer model
    semantic_model = SentenceTransformer('all-MiniLM-L6-v2')

    # Load the question answering pipeline
    qa_pipeline = pipeline("question-answering", model="distilbert/distilbert-base-cased-distilled-squad")

    return index, df, semantic_model, qa_pipeline

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
    
    st.text_area("Chat History:", value=st.session_state['chat_history'], height=300, key="chat_history")
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
    
    st.text_area("Chat History:", value=st.session_state['chat_history'], height=300, key="chat_history")

st.markdown("---")
st.markdown("<h4 style='text-align: center;'>Please use this information responsibly. Built with ❤️ using Streamlit</h4>", unsafe_allow_html=True)
