# import json
# import pandas as pd
# import spacy
# import networkx as nx
# import matplotlib.pyplot as plt
# from transformers import pipeline
# import pickle


# # Load cleaned JSON data
# with open('cleaned.pkl', 'rb') as file:
#     df = pickle.load(file)

# # def construct_graph(df: pd.DataFrame):
# #     G = nx.Graph()

# #     # Add entities and relationships to the graph
# #     for idx, entry in df['entities'].items():
# #         previous_entity = None
# #         for ent in entry:
# #             G.add_node(ent[0], label=ent[1])
# #             if previous_entity:
# #                 G.add_edge(previous_entity[0], ent[0])
# #             previous_entity = ent

# #     # Save the knowledge graph to a file using pickle
# #     with open("knowledge_graph.gpickle", "wb") as f:
# #         pickle.dump(G, f)

# #     print("Knowledge graph created and saved to knowledge_graph.gpickle")

# def construct_graph(df: pd.DataFrame):
#     G = nx.Graph()

#     # Debugging: Print the structure of df['entities']
#     print("Structure of df['entities']:", df['entities'])

#     # Add entities and relationships to the graph
#     for idx, entry in enumerate(df['entities']):
#         print(f"Processing entry {idx}: {entry}")  # Debugging: Print each entry
#         previous_entity = None
#         for ent in entry:
#             print(f"Adding node {ent[0]} with label {ent[1]}")  # Debugging: Print each node addition
#             G.add_node(ent[0], label=ent[1])
#             if previous_entity:
#                 print(f"Adding edge from {previous_entity[0]} to {ent[0]}")  # Debugging: Print each edge addition
#                 G.add_edge(previous_entity[0], ent[0])
#             previous_entity = ent

#     # Save the knowledge graph to a file using pickle
#     with open("knowledge_graph.gpickle", "wb") as f:
#         pickle.dump(G, f)

#     print("Knowledge graph created and saved to knowledge_graph.gpickle")

# if __name__ == "__main__":
#     construct_graph(df)

import pandas as pd
import networkx as nx
import pickle

# Load cleaned JSON data
with open('cleaned.pkl', 'rb') as file:
    df = pickle.load(file)

# Debugging: Check the type and structure of df
print(f"Type of df: {type(df)}")

if isinstance(df, pd.DataFrame):
    print("Columns in df:", df.columns)
else:
    print("Loaded object is not a DataFrame")

def construct_graph(df: pd.DataFrame):
    if 'entities' not in df.columns:
        raise ValueError("The DataFrame does not contain an 'entities' column")
    
    G = nx.Graph()

    # Ensure df['entities'] is accessed correctly
    entities = df['entities']

    # Debugging: Print the structure of df['entities']
    print("Structure of df['entities']:", entities)

    # Add entities and relationships to the graph
    for idx, entry in enumerate(entities):
        print(f"Processing entry {idx}: {entry}")  # Debugging: Print each entry
        previous_entity = None
        for ent in entry:
            print(f"Adding node {ent[0]} with label {ent[1]}")  # Debugging: Print each node addition
            G.add_node(ent[0], label=ent[1])
            if previous_entity:
                print(f"Adding edge from {previous_entity[0]} to {ent[0]}")  # Debugging: Print each edge addition
                G.add_edge(previous_entity[0], ent[0])
            previous_entity = ent

    # Save the knowledge graph to a file using pickle
    with open("knowledge_graph.gpickle", "wb") as f:
        pickle.dump(G, f)

    print("Knowledge graph created and saved to knowledge_graph.gpickle")

if __name__ == "__main__":
    if isinstance(df, pd.DataFrame):
        construct_graph(df)
    else:
        print("The loaded data is not a DataFrame. Please check the pickle file.")
