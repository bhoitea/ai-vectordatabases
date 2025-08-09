# vss_demo.py
import sqlite3
import json
import sqlite_vss   # installed by `pip install sqlite-vss`

DB = "vss_demo.db"


import sqlite3
conn = sqlite3.connect(":memory:")
print(hasattr(conn, 'enable_load_extension'))  # Should print True

# 1) Connect and load the vss extension:
db = sqlite3.connect(DB)
db.enable_load_extension(True)
sqlite_vss.load(db)          # loads vector0 + vss0 into this connection
db.enable_load_extension(False)

# 2) Create a regular table (optional) and the vss virtual table (3-dim used here)
db.execute("CREATE TABLE IF NOT EXISTS docs(id INTEGER PRIMARY KEY, text TEXT);")
db.execute("CREATE VIRTUAL TABLE IF NOT EXISTS docs_vss USING vss0(embedding(3));")

# 3) Insert a few documents + corresponding vectors (vectors as JSON)
docs = [
    (1, "Apple iPhone: great phone"),
    (2, "Banana: yellow fruit"),
    (3, "Orange: citrus and fresh")
]
db.executemany("INSERT OR IGNORE INTO docs(id, text) VALUES (?, ?);", docs)

# Simple example embeddings (3 dims) — in real use: use an embedding model
embeddings = {
    1: [0.9, 0.1, 0.0],   # 'phone' like
    2: [0.1, 0.9, 0.0],   # 'banana' like
    3: [0.1, 0.2, 0.9],   # 'citrus/orange' like
}

# Insert into the vss virtual table (rowid should match doc id if you want)
for rowid, vec in embeddings.items():
    db.execute(
        "INSERT OR REPLACE INTO docs_vss(rowid, embedding) VALUES (?, ?);",
        (rowid, json.dumps(vec))
    )
db.commit()

# 4) Search: find nearest to a query vector
query_vec = json.dumps([0.05, 0.85, 0.05])   # looks like 'banana'
rows = db.execute(
    "SELECT rowid, distance FROM docs_vss WHERE vss_search(embedding, ?) ORDER BY distance LIMIT 5;",
    (query_vec,)
).fetchall()

print("Nearest results (rowid, distance):")
for r in rows:
    print(r, "->", db.execute("SELECT text FROM docs WHERE id = ?;", (r[0],)).fetchone()[0])

db.close()
