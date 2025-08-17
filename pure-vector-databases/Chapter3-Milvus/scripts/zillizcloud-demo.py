# Zilliz cloud - Similarity search using Zilliz cloud

from pymilvus import (
   connections, MilvusClient,
   DataType, CollectionSchema, FieldSchema, Collection, utility
)
from pymilvus import model

# 1️⃣ Connect to Zilliz Cloud token="username:password", db_066b992836da859 is a use name
client = MilvusClient(alias="default",uri="https://in03-066b992836da859.serverless.gcp-us-west1.cloud.zilliz.com",token="db_066b992836da859:*******") 

client = MilvusClient(connection_alias="default")

# 2️⃣ Recreate collection schema with title field
if client.has_collection("recipes"):
   client.drop_collection("recipes")

schema = CollectionSchema([
   FieldSchema("id", DataType.INT64, is_primary=True),
   FieldSchema("vector", DataType.FLOAT_VECTOR, dim=768),
   FieldSchema("title", DataType.VARCHAR, max_length=512)
])
client.create_collection("recipes", schema=schema)

# 3️⃣ Prepare embeddings and data
ef = model.DefaultEmbeddingFunction()
print("🎯 Embedding dim:", ef.dim)

texts = [
   "Spaghetti Pomodoro with tomato, basil, garlic",
   "Tomato Basil Soup rich and creamy",
   "Garlic Bread with butter and herbs",
   "Pesto Pasta with basil, pine nuts, parmesan",
   "Margherita Pizza with tomato, basil, mozzarella",
   "Chicken Alfredo pasta with parmesan and cream",
   "Caprese Salad with tomato, basil, mozzarella",
   "Garlic Shrimp Linguine with parsley and lemon"
]
vectors = ef.encode_documents(texts)

entities = [
   {"id": i+1, "vector": vectors[i], "title": texts[i]}
   for i in range(len(texts))
]

# 4️⃣ Insert data
res = client.insert("recipes", entities)
print(f"\n✅ Inserted {res['insert_count']} recipes:")
for e in entities:
   print(f"• ID {e['id']}: {e['title']}")

# 5️⃣ Index & load collection
collection = Collection("recipes", using="default")
collection.create_index("vector", {
   "index_type": "IVF_FLAT",
   "metric_type": "COSINE",
   "params": {"nlist": 128}
})
collection.load()
utility.wait_for_loading_complete("recipes")
print("Collection indexed & loaded")

# 6️⃣ Prepare and log query
query = "basil tomato chicken pasta"
q_vec = ef.encode_documents([query])[0]
print(f"\n🔍 Query: {query}")
print("🔢 Vector sample:", [round(f,4) for f in q_vec[:5]], "...")

# 7️⃣ Perform search with metadata
res_search = collection.search(data=[q_vec],anns_field="vector",param={"metric_type": "COSINE", "params": {}},limit=3,output_fields=["title"])

# 8️⃣ Print top-3 results
print("\n📊 Top 3 Search Results:")
for hit in res_search[0]:
   print(f"• ID {hit.id}, Title: {hit.entity.get('title')}, Distance: {hit.distance:.4f}")