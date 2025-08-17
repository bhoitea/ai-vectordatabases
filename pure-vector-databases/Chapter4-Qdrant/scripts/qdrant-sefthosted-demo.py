# Step 1: Import required libraries
# - QdrantClient manages connection and vector operations.
# - SentenceTransformer handles text → vector embeddings.
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
# --------------------------------------------------------------------------
# Step 2: Connect to a local Qdrant instance.
# Ensure Qdrant is running on http://localhost:6333 (e.g., via Docker).
client = QdrantClient(url="http://localhost:6333")  # REST API endpoint
# --------------------------------------------------------------------------
# Step 3: Define the collection and ensure correct configuration.
collection_name = "ads_collection"

# If collection exists, delete it to reset. Qdrant enforces fixed vector dimension.
if client.collection_exists(collection_name):
   client.delete_collection(collection_name)

# Create collection with vectors of 384 dimensions, using cosine similarity.
# This matches the output of all-MiniLM-L6-v2 embeddings (384‑dim) :contentReference[oaicite:1]{index=1}.
client.create_collection(
   collection_name=collection_name,
   vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

# --------------------------------------------------------------------------
# Step 4: Initialize embedding model.
# Using a lightweight yet powerful model to generate semantic embeddings.
embed = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# --------------------------------------------------------------------------
# Step 5: Define 8 real advertisement text lines to insert.
ads = [
   "Limited Time Offer: Grab It Before It's Gone!",
   "Discover the Secret to Ageless Beauty!",
   "Join Thousands Who Made the Smart Choice!",
   "Boost Your Skills: Top-Rated Courses Inside!",
   "Elevate Your Career: Exclusive Workshops!",
   "Unlock Your Special Discount: Click Now!",
   "Experience Luxury at a Fraction of the Cost!",
   "Turn Your Dreams into Reality: Learn How!"
]

# --------------------------------------------------------------------------
# Step 6: Encode ads, create PointStruct objects, and upsert them.
points = []
for i, text in enumerate(ads, start=1):
   vec = embed.encode(text).tolist()  # -> 384-dim vector
   points.append(PointStruct(id=i, vector=vec, payload={"ad_text": text}))

client.upsert(collection_name=collection_name, points=points, wait=True)

# Display the inserted ads for confirmation.
print("Inserted ads:")
for pt in points:
   print(f"- id={pt.id}: \"{pt.payload['ad_text']}\"")

# --------------------------------------------------------------------------
# Step 7: Interactive search query from the user.
user_query = input("\nEnter your search query: ")
print(f"\nSearching for: \"{user_query}\"")

# Encode user query into vector.
q_vec = embed.encode(user_query).tolist()

# Step 8: Execute semantic nearest-neighbor search.
results = client.query_points(collection_name=collection_name,query=q_vec,with_payload=True,limit=3
).points

# Step 9: Print top 3 matching ads with similarity scores.
print("\nTop matching ads:")
for pt in results:
   print(f"- id={pt.id}, score={pt.score:.3f}: \"{pt.payload['ad_text']}\"")