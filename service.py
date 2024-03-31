import openai
import json
import requests
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_setup import qdrant_client, collection_name
from qdrant_client.models import VectorParams, Distance

from neural_searcher import NeuralSearcher

app = FastAPI()
qdrant_url = "http://localhost:6333"
qdrant_client = QdrantClient(qdrant_url)

model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
json_url = "https://storage.googleapis.com/generall-shared-data/startups_demo.json"
response = requests.get(json_url)
if response.status_code == 200:
    try:
        # Load the JSON data
        data = response.json()

        # Connect to Qdrant
        qdrant_url = "http://localhost:6333"
        qdrant = qdrant_client.Client(qdrant_url)

        # Define the collection name
        collection_name = "startup_descriptions"

        # Check if the collection exists, if not, create it
        if not qdrant.has_collection(collection_name):
            vector_params = VectorParams(size=384, distance=Distance.COSINE)
            qdrant.recreate_collection(collection_name=collection_name, vectors_config=vector_params)
            print(f"Collection '{collection_name}' created successfully.")

        for doc in data:
            vector = doc["vector"]
            metadata = doc
            qdrant.insert(collection_name, [vector], [metadata])

        print("Data added to the collection successfully.")
    except json.decoder.JSONDecodeError as e:
        print("Failed to decode JSON data. Response content:")
        print(response.content)
else:
    print(f"Failed to fetch data from URL. Status code: {response.status_code}")

vector_params = VectorParams(size=384, distance=Distance.COSINE)

qdrant_client.recreate_collection(
    collection_name=collection_name,
    vectors_config=vector_params
)

print(f"Collection '{collection_name}' created successfully.")

neural_searcher = NeuralSearcher(collection_name="startup_descriptions")

openai.api_key = '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'

session_history = {}


class QueryRequest(BaseModel):
    user_id: str
    message: str


class QueryResponse(BaseModel):
    output: str


@app.get("/api/search")
async def search(q: str = Query(None, title="Query")):
    if q is None:
        return {"error": "Query parameter cannot be None"}
    print(q)
    query_vector = model.encode(q).tolist()

    search_results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=5
    )
    return {"results": search_results}


@app.post("/query")
async def query_handler(request: QueryRequest):
    user_id = request.user_id
    user_message = request.message

    if not user_id or not user_message:
        raise HTTPException(status_code=422, detail="Both user_id and message are required")

    if user_id not in session_history:
        session_history[user_id] = []

    session_history[user_id].append(user_message)

    relevant_data = neural_searcher.search(user_message)

    if relevant_data:
        if len(session_history[user_id]) > 1:
            context = "\n".join(session_history[user_id][-2:])
        else:
            context = user_message

        completion = openai.Completion.create(
            engine="gpt-3.5-turbo-0125",
            prompt=context + "\nUser message: " + user_message + "\nAI response:",
            max_tokens=50
        )

        ai_response = completion.choices[0].text.strip()
    else:
        ai_response = "No relevant data found."

    return {"output": ai_response}


if __name__ == "__main__":
    import uvicorn
    from sentence_transformers import SentenceTransformer

    uvicorn.run(app, host="0.0.0.0", port=8000)
