# 1. Install dependencies:
# pip install qdrant-client

from qdrant_client import QdrantClient, models

# 2. Initialize the Qdrant Cloud client
#    Use the full URL (including https://) and your API key from the Cloud dashboard.
client = QdrantClient(
   url="https://64b4eecf-b2e4-******.us-west-2-0.aws.cloud.qdrant.io:6333",
   api_key="******"
)

# 3. Define the collection name
collection = "entertainment_collection"

# 3a. If the collection already exists, delete it to start fresh
if client.collection_exists(collection):
   client.delete_collection(collection)

# 3b. Create the collection with FastEmbed-compatible vector params:
# get_fastembed_vector_params() ensures correct embedding dimension, HNSW index config, and other settings.
# Leveraging a powerful helper from the FastEmbed integration to automatically configure the vector storage in Qdrant.
client.create_collection(
   collection_name=collection,
   vectors_config=client.get_fastembed_vector_params()
)

# 4. Define 8 entertainment-themed text entries with metadata
docs = [
   "Romantic comedy movie about two unlikely lovers.",
   "Action-packed superhero blockbuster with stunning visuals.",
   "Documentary series exploring wildlife conservation in Africa.",
   "Sci‑fi adventure set in a dystopian future city.",
   "Animated feature film suitable for the whole family.",
   "True‑crime podcast unraveling a mysterious cold case.",
   "Live Broadway‑style musical with elaborate choreography.",
   "Fantasy epic trilogy filled with magic and dragons."
]
metadata = [{"description": text} for text in docs]

# 5. Insert documents using FastEmbed's `add` method
#    This automatically embeds documents and uploads them to the Qdrant collection.
#    Returns list of generated IDs (UUIDs) for each document.
ids = client.add(collection_name=collection, documents=docs, metadata=metadata)

# Print confirmation of insertion
print("✅ Inserted entertainment documents:")
for doc_id, meta in zip(ids, metadata):
   print(f"- id={doc_id}: \"{meta['description']}\"")

# 6. Prompt the user for a semantic search query
query = input("\nEnter your entertainment search query: ")
print(f"\n🔍 Searching for: \"{query}\"")

# 7. Perform semantic search using FastEmbed `query` method
#    This auto-embeds the user query and retrieves top-N semantically similar documents.
results = client.query(
   collection_name=collection,
   query_text=query,
   limit=3  # Fetch the top 3 results
)

# 8. Display the search results with similarity scores and metadata
print("\n🎯 Top matches:")
for res in results:
   desc = res.metadata.get("description", "<no description>")
   print(f"- id={res.id}, score={res.score:.3f}: \"{desc}\"")