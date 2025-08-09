# Redis Vector Search Demo with Redis Stack + HNSW

This project demonstrates **semantic vector search** using **Redis Stack** and the **HNSW algorithm** for approximate nearest neighbor search.
It creates a vector index, inserts documents with embeddings, and performs similarity search with optional filtering.

---

## 🚀 Features

- **Redis Stack** for vector search with `FT.CREATE` and `HNSW` index.
- Store text metadata and embeddings together in Redis.
- Perform **semantic similarity search** with cosine distance.
- Filter by metadata fields (e.g., category).
- Simple Python script — no extra frameworks needed.

---

## 🛠 Prerequisites

- **Docker** installed
- **Python 3.8+**
- Internet access to pull Redis Stack image

---

## 📦 Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/redis-vector-demo.git
cd redis-vector-demo
```
