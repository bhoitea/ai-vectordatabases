#!/usr/bin/env python3
# 🌟 Pinecone Vector Search Hands-On Demo
"""
This script demonstrates:
- How to delete an existing index (to reset)
- How to create a new Pinecone serverless index
- How to insert vectors with descriptive metadata
- How to query by semantic similarity + metadata filters
- How to interpret similarity scores in a vector database context

Use this as a foundation for real-world workflows involving LLMs, RAG, or semantic search pipelines.
"""

# STEP 1: Install Pinecone SDK if not already done
# Run this in your terminal (not in Python):
# pip install pinecone-client

from pinecone import Pinecone, ServerlessSpec
import time

# STEP 2: Initialize Pinecone Client
# 🔐 Replace with your actual Pinecone API key and environment identifier
pc = Pinecone(api_key="pcsk_3g5ZMv_ZEf5gFp1bLeGFobV3cDimRgmPv3pJF9brskbJ4MDSJceJAPj527cPZK7tYPFKV", environment="us-east-1-aws")

# STEP 3: Define index configuration
index_name = "docs-example"        # Index name (like a database table)
dimension = 1536                   # Vector size (e.g., OpenAI's text-embedding-ada-002)
metric = "cosine"                  # Similarity metric: cosine, euclidean, or dotproduct
cloud = "aws"                      # Cloud provider for serverless deployment
region = "us-east-1"              # Specific region
namespace = "example-namespace"   # Logical partition (akin to schema/sub-database)

# STEP 4: Cleanup -- delete existing index to start fresh
if index_name in pc.list_indexes().names():
   pc.delete_index(index_name)
   print(f"🗑️ Deleted existing index '{index_name}'.")

# STEP 5: Create a new serverless index
# Pinecone provisions the backend automatically
pc.create_index(
   name=index_name,
   dimension=dimension,
   metric=metric,
   spec=ServerlessSpec(cloud=cloud, region=region)
)
print(f"✅ Created new index '{index_name}'.")

# STEP 6: Connect to the newly created index
index_info = pc.describe_index(index_name)
index = pc.Index(host=index_info.host)

# STEP 7: Prepare sample vectors for demonstration
vector_a = [0.1] * dimension
vector_b = [0.15] * dimension     # Slightly different from A
vector_c = [0.5] * dimension      # Far apart from A and B

vectors = [
 {"id":"A","values":vector_a,"metadata":{"genre":"comedy","text":"I want a heartwarming comedy about a stand‑up comedian.","year":2020}},
 {"id":"B","values":vector_b,"metadata":{"genre":"comedy","text":"Show me a light comedy featuring family road‑trip adventures.","year":2021}},
 {"id":"C","values":vector_c,"metadata":{"genre":"thriller","text":"Recommend a suspense thriller with lots of plot twists.","year":2022}}
]


# STEP 8: Upsert (upload) the vectors into the index
index.upsert(vectors=vectors, namespace=namespace)
print(f"✅ Upserted {len(vectors)} vectors into namespace '{namespace}'.")

# STEP 9: Wait for indexing to complete
print("\n⏳ Waiting for vectors to be indexed...")
for attempt in range(5):
   stats = index.describe_index_stats(namespace=namespace)
   count = stats["namespaces"].get(namespace, {}).get("vector_count", 0)
   if count >= len(vectors):
       break
   print(f"⏳ Attempt {attempt + 1}: {count}/{len(vectors)} indexed. Retrying in 2s...")
   time.sleep(2)

# STEP 10: Prepare and print the query
query_text = "I'm in the mood for a funny movie about family adventures."
print("\n🔍 Query text:", query_text)

# Normally you'd generate this via an embedder; here it's hardcoded for demo
query_vector = [0.11] * dimension
print("🔍 Query vector preview:", query_vector[:5], "...")  # show first 5 dimensions

# STEP 11: Query for similar vectors with metadata filter
query_response = index.query(
   vector=query_vector,
   top_k=3,
   include_values=False,      # We only need metadata and scores
   include_metadata=True,
   namespace=namespace,
   filter={                   # Filter ensures only comedies from 2020 onwards
       "genre": {"$eq": "comedy"},
       "year": {"$gte": 2020}
   }
)

# STEP 12: Print query results in a user-friendly format
print("\n📋 Results for your query:")
if not query_response["matches"]:
   print("No matches found.")
else:
   for match in query_response["matches"]:
       md = match["metadata"]
       print(f"- ID: {match['id']} | Score: {match['score']:.4f}")
       print(f"  Genre: {md['genre']}, Year: {md['year']}")
       print(f"  Description: {md['text']}\n")

# STEP 13: Show inserted vectors metadata for comparison
print("🧾 All inserted vectors:")
for v in vectors:
   md = v["metadata"]
   print(f"- {v['id']}: genre={md['genre']}, year={md['year']}")
   print(f"  text: {md['text']}")