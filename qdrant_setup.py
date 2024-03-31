from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

# Create Qdrant client
qdrant_client = QdrantClient("http://localhost:6333")  # Replace with your Qdrant endpoint

# Specify the collection name
collection_name = "startup_descriptions"  # You can choose any meaningful name here

# Create the collection in Qdrant
qdrant_client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)
