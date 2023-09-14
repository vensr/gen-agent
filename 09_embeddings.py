from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from langchain.embeddings import OpenAIEmbeddings
embedding = OpenAIEmbeddings()
response = embedding.embed_query("Embeddings are great!")

print(response)

# python3 09_embeddings.py
