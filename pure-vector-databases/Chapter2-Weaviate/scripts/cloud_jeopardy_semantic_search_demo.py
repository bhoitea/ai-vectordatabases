"""
Weaviate Jeopardy Semantic Search (10 Items, 2 Queries)

Demonstrates:
1. Connect to Weaviate
2. Create/reuse 'Question' collection
3. Insert 10 hardcoded Q&A
4. Log insertions
5. Perform semantic searches (2 queries) w/ deduplication
6. Show top result w/ similarity
7. Print the entire dataset at the end
8. Close connection
"""

import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure
from weaviate.classes.query import MetadataQuery

def main():
  client = weaviate.connect_to_weaviate_cloud(
      cluster_url="k2ecrve7srg1jgxghzo2ta.c0.asia-southeast1.gcp.weaviate.cloud",
      auth_credentials=Auth.api_key("***"),
  ); print("🔌 Connected")

  try:
      q = client.collections.create(name="Question", vectorizer_config=Configure.Vectorizer.text2vec_weaviate())
      print("✅ Created 'Question'")
  except:
      q = client.collections.get("Question"); print("⚠️ Reusing 'Question'")

  data = [
      ("This organ removes excess glucose from the blood & stores it as glycogen","Liver","SCIENCE"),
      ("This large mammal is known for its long trunk used for drinking and grabbing food","Elephant","ANIMALS"),
      ("It's the only living mammal in the order Proboscidea","Elephant","ANIMALS"),
      ("The gavial looks very much like a crocodile except for this bodily feature","the nose or snout","ANIMALS"),
      ("In 1953 Watson & Crick built a model of the molecular structure of this, the gene‑carrying substance","DNA","SCIENCE"),
      ("This element has the atomic number 79 and is a precious yellow metal","Gold","SCIENCE"),
      ("This planet is known as the Red Planet","Mars","SCIENCE"),
      ("He painted the Mona Lisa","Leonardo da Vinci","ART"),
      ("The capital city of Japan","Tokyo","GEOGRAPHY"),
      ("The author of 'Romeo and Juliet'","William Shakespeare","LITERATURE"),
  ]
  print(f"📥 Inserting {len(data)} items")
  with q.batch.fixed_size(batch_size=200) as batch:
      for i,(qq,aa,cc) in enumerate(data,1):
          batch.add_object({"question":qq,"answer":aa,"category":cc})
          #print(f" ↳ #{i}: A={aa}")
  print("✅ Inserted all items")
  # Print the full dataset
  print("\n📄 Full dataset:")
  for i,(qq,aa,cc) in enumerate(data,1):
      print(f" {i}. Q: {qq} | A: {aa} | Cat: {cc}")


  for uq in ("animal with long trunk","organ that stores glycogen"):
      print(f"\n🔍 Query: {uq}")
      resp = q.query.near_text(query=uq,limit=5,auto_limit=1,return_metadata=MetadataQuery(distance=True))
      seen,unique=set(),[]
      for o in resp.objects:
          if o.uuid not in seen:
              seen.add(o.uuid); unique.append(o)
      if unique:
          o=unique[0]; p=o.properties; d=o.metadata.distance
          print(f"→ {p['answer']} (Q: {p['question']}) dist={d:.4f}")
  client.close(); print("🔒 Closed")

if __name__=="__main__":
  main()