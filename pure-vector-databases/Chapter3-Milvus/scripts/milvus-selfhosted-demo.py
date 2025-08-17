# Self-hosted similarity search using Milvus

from pymilvus import MilvusClient
import random

# 1. Connect to Milvus
print("➡️ Connecting to Milvus Standalone...")
client = MilvusClient(uri="http://localhost:19530", token="root:Milvus")

# 2. Prepare database & collection
db = "milvus_demo"
if db not in client.list_databases(): client.create_database(db)
client.using_database(db)
col = "demo_collection"
if client.has_collection(col): client.drop_collection(col)
client.create_collection(collection_name=col, dimension=768)  # 768-dim

# 3. Insert 5 entries
docs = [
   "Artificial intelligence was founded as an academic discipline in 1956.",
   "Alan Turing was the first person to conduct substantial research in AI.",
   "Born in Maida Vale, London, Turing was raised in southern England.",
   "Marie Curie pioneered research in radioactivity and won two Nobel Prizes.",
   "The first computer programmer was Ada Lovelace in the 19th century."
]
subjects = ["history"]*3 + ["science", "history"]
data = [
   {
       "id": i,
       "vector": [random.uniform(-1, 1) for _ in range(768)],
       "text": docs[i],
       "subject": subjects[i]
   } for i in range(5)
]
print("➡️ Preview of inserted data:")
for e in data: print(f" • id={e['id']}, subj={e['subject']}, text='{e['text']}'")

res = client.insert(collection_name=col, data=data)
# print(f"Inserted {res['insert_count']} entities -- IDs: {res['ids']}")

# 4. Human-readable query and simulated embedding
user_query = "research in AI"
print(f"➡️ User query: \"{user_query}\"")
query_vec = [[random.uniform(-1,1) for _ in range(768)]]
print("✅ Simulated query vector sample:", query_vec[0][:5], "...\n")

# 5. Perform vector search
res_search = client.search(collection_name=col, data=query_vec, limit=2, output_fields=["text","subject"])
print("✅ Search results:")
for hits in res_search:
   for h in hits:
       print(f" • id={h['id']}, distance={h['distance']:.4f}")
       print(f"   subject: {h['entity']['subject']}")
       print(f"   text: {h['entity']['text']}\n")
print("🎉 Script completed.")