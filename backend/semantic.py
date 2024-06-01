from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd

# Load your data
df = pd.read_pickle("cleaned.pkl")

# Use a pre-trained model to get embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create embeddings for the cleaned_text
embeddings = model.encode(df['cleaned_text'].tolist())

# Save embeddings using Faiss
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

# Save the index to a file
faiss.write_index(index, "faiss_index.bin")

# Save the original text with embeddings
df['embeddings'] = embeddings.tolist()
df.to_pickle("data_with_embeddings.pkl")
