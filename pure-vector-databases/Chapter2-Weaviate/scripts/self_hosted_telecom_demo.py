#!/usr/bin/env python3
"""
📡 Telecom Call Summary Semantic Search Demo (Weaviate v3 client)

This script demonstrates:
- What query is being made
- What data went into Weaviate
- How search results are retrieved and interpreted
"""

from sentence_transformers import SentenceTransformer
import weaviate

client = weaviate.Client(url="http://localhost:8081")  # 1️⃣ Connect
client.schema.delete_all()  # 2️⃣ Reset schema
client.schema.create_class({
   "class": "CallSummary",
   "description": "Telecom customer call summaries with metadata",
   "vectorizer": "none",
   "properties": [
       {"name": "summary","dataType": ["text"]},
       {"name": "agent","dataType": ["text"]},
       {"name": "date","dataType": ["date"]},
       {"name": "issueType","dataType": ["text"]}
   ]
})
print("✅ Created CallSummary class")

model = SentenceTransformer("all-MiniLM-L6-v2")  # 3️⃣ Load model

# 4️⃣ Data to be inserted
records = [
   {"summary": "5G signal drops during train handover.", "agent": "Alice", "date": "2025-07-01T10:00:00Z", "issueType": "handover"},
   {"summary": "4G disconnects near long tunnels.",       "agent": "Bob",   "date": "2025-07-03T16:00:00Z", "issueType": "handover"},
   {"summary": "Data slowdown after cell‑site update.",  "agent": "Carlos","date": "2025-06-25T09:15:00Z", "issueType": "throughput"}
]
print(f"🧾 Data inserted ({len(records)} records):")
for r in records:
   print(f" - {r['summary']} [{r['agent']}, {r['date']}, {r['issueType']}]")

# 5️⃣ Insert records with vectors, collection is CallSummary
for rec in records:
   client.data_object.create(data_object=rec, class_name="CallSummary", vector=model.encode(rec["summary"]).tolist())
print("✅ Inserted all records with embeddings")

# 6️⃣ Define & print query
query_text = "5G connection lost during handover"
print(f"\n🔍 Query: \"{query_text}\"")
query_vec = model.encode(query_text).tolist()

# 7️⃣ Search with vector + metadata filter
response = (client.query
   .get("CallSummary", ["summary", "agent", "date", "issueType", "_additional {certainty}"])
   .with_near_vector({"vector": query_vec})
   .with_where({"path": ["issueType"], "operator": "Equal", "valueText": "handover"})
   .with_limit(5)
   .do())

# 8️⃣ Display results
print("\n📋 Search Results (issueType = 'handover'):\n")
for idx, m in enumerate(response["data"]["Get"]["CallSummary"], 1):
   print(f"Result {idx}:")
   print(f" • Summary:   {m['summary']}")
   print(f" • Agent:     {m['agent']}")
   print(f" • Date:      {m['date']}")
   print(f" • IssueType: {m['issueType']}")
   cert = m.get("_additional", {}).get("certainty")
   if cert is not None: print(f" • Certainty: {cert:.3f}")
   print("-" * 40)