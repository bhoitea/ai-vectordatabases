# Redis Vector Search — Redis Stack + HNSW Demo

This repository contains a Python-based demo for performing **semantic vector search** using **Redis Stack** with the **HNSW algorithm** for Approximate Nearest Neighbor (ANN) search.

It showcases how to:

- Create a vector index in Redis
- Insert documents with text, metadata, and vector embeddings
- Run similarity searches with optional filtering

---

## 📜 Overview

- **Redis Stack** for vector search capabilities
- **RediSearch** module for indexing and querying text + vector data
- **HNSW** algorithm for fast approximate nearest neighbor search
- Python client for connecting and performing operations

---

## 🛠 Prerequisites

Before beginning, ensure you have:

- Redis Stack running (via Docker or local installation)
- Python 3.x installed
- Required libraries: `redis` and `numpy`

Install dependencies:

```bash
pip install redis numpy
```

---

## ⚡ Quick Start

### 1️⃣ Start Redis with Vector Support

```bash
docker run -d --name redis-vector -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

- Redis CLI: `localhost:6379`
- Redis Insight UI: `localhost:8001`

---

### 2️⃣ Run the Python Script

**Copy the provided `redis_vector_demo.py` script into your working directory and execute:**

```bash
python scripts/redis_vector_demo.py
```

---

## 📂 Files in this Repo

| File                             | Description                                            |
| -------------------------------- | ------------------------------------------------------ |
| `scripts/redis_vector_demo.py` | Python script demonstrating full Redis Vector workflow |
| `README.md`                    | Project documentation                                  |

---

## 🔍 Example Output

```
🚀 Redis Vector Demo Starting...
✅ Vector index created successfully
📄 Document 'AI in Legal Technology' inserted with key doc:1
📄 Document 'Machine Learning for Finance' inserted with key doc:2
📄 Document 'Healthcare AI Applications' inserted with key doc:3

🔍 Performing vector similarity search...

📋 Found 3 similar documents:
  • Healthcare AI Applications (Category: healthcare, Score: 0.251367151737)
  • AI in Legal Technology (Category: legal, Score: 0.251555621624)
  • Machine Learning for Finance (Category: finance, Score: 0.261262178421)

⚖️ Legal documents only (1 found):
  • AI in Legal Technology (Score: 0.251555621624)
```

---

## 🧠 How It Works

1. **Create the Index**Using `FT.CREATE` with:

   - `title` and `content` as text fields
   - `category` as a tag field
   - `timestamp` as a numeric field
   - `embedding` as a `FLOAT32` vector field with **HNSW** indexing
2. **Insert Documents**

   - Store embeddings as binary `FLOAT32` arrays
   - Include metadata fields for filtering
3. **Search**

   - Perform **KNN** similarity search with optional category filters
   - Sort results by similarity score

---

## 📚 Resources

- [Redis GitHub](https://github.com/redis/redis)
- [Redis Vector Docs](https://redis.io/docs/latest/develop/get-started/vector-database/)

---

**Author:** Amol Bhoite
