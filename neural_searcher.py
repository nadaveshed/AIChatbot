from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


class NeuralSearcher:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        # Initialize encoder model
        self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient("http://localhost:6333")  # Update with your Qdrant endpoint

    def search(self, text):
        # Convert text query into vector
        vector = self.model.encode(text).tolist()

        # Use vector to search for closest vectors in the collection
        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=None,  # You can add filters if needed
            limit=5,  # Adjust as needed
        )

        # Extract relevant data from search result
        relevant_data = [hit.payload for hit in search_result]
        return relevant_data
