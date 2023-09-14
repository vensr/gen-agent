import pinecone
import openai

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import dotenv
openai.api_key=dotenv.get_key(key_to_get= "OPENAI_API_KEY", dotenv_path=".env")

pinecone.init()
index = pinecone.Index('avatar')

input = """In summary, handling a situation where an employee becomes emotional during a feedback conversation requires a delicate and empathetic approach. The manager should prioritize creating a supportive environment, active listening, and offering assistance to address the underlying issues. Additionally, proactive training and fostering open communication can help managers better prepare for and handle such situations in the future.
"""

def create_embeddings(input_data):
    # create embeddings
    MODEL = "text-embedding-ada-002"
    embeddings_data = openai.Embedding.create(
        input=[input_data], engine=MODEL
    )

    embeds = [record['embedding'] for record in embeddings_data['data']]
    return embeds

def save_to_vector_db(embeds):
    upsert_response = index.upsert(
        vectors=[
            ("employee_drama", embeds, {"genre": "drama"}),
        ]
    )
    print(upsert_response)
    return upsert_response

def search_vector_db(embeds):
    query_response = index.query(
    top_k=2,
    include_values=True,
    include_metadata=True,
    vector=embeds,
    filter={
        "genre": {"$in": ["comedy", "documentary", "drama"]}
    }
    )
    return query_response

# create embeddings and save to vector db
# save_to_vector_db(create_embeddings(input))

embeds = create_embeddings("how to handle a emotional employee?")
response = search_vector_db(embeds)
print(response)

# python3 10_pinecone_db.py
