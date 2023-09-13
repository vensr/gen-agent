# pip install chromadb
import chromadb

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="my_vector_collection")

# note, no embeddings done in this example
collection.add(
    documents=["Bangalore is a green city", "Bangalore is not a green city"],
    metadatas=[{"source": "Newspapers"}, {"source": "Google"}],
    ids=["id1", "id2"]
)

results = collection.query(
    query_texts=["which is green city?"],
    n_results=1
)
print(results)

# python3 04_vector_db_no_embbedings.py
