# Qdrant Vector Search Demo

This repository demonstrates how to use **Qdrant** for semantic search with both **self-hosted** (Docker) and **Qdrant Cloud** setups.

---

## 📂 Project Structure

```
qdrant-vector-demo/
├── README.md
├── requirements.txt
├── .gitignore
└── scripts/
    ├── qdrantdemo.py        # Self-hosted Qdrant demo
    └── qdrantclouddemo.py   # Qdrant Cloud demo
```

---

## 🚀 Quick Start

### 1️⃣ Run Qdrant (Self-hosted)

```bash
docker pull qdrant/qdrant

docker run -d --name qdrant_local -p 6333:6333 -p 6334:6334 \
 -v "$(pwd)/qdrant_storage:/qdrant/storage:z" qdrant/qdrant

```

Check readiness:

```bash
curl -X GET "http://localhost:6333/healthz"
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run Demo Scripts

- **Self-hosted Qdrant**

  ```bash
  python3 scripts/qdrant-sefthosted-demo.py
  ```
- **Qdrant Cloud**

  ```bash
  python3 scripts/qdrant-cloud-demo.py
  ```

---

## 🧑‍💻 Scripts Overview

### `scripts/qdrantdemo.py`

- Connects to **local Qdrant** (running in Docker).
- Creates a collection.
- Inserts sample ads dataset.
- Performs semantic similarity search with a user query.

### `scripts/qdrantclouddemo.py`

- Connects to **Qdrant Cloud** (requires API key & endpoint).
- Creates a collection.
- Inserts sample entertainment dataset.
- Performs semantic similarity search with a user query.

---

## 🔗 References

* Open-source database: :[https://qdrant.tech/documentation/](https://qdrant.tech/documentation/)
* Cloud documentation: [https://qdrant.tech/documentation/cloud-intro/](https://qdrant.tech/documentation/cloud-intro/)
* Github:[https://github.com/qdrant/qdrant](https://github.com/qdrant/qdrant)
* Qdrant Cloud:[https://cloud.qdrant.io/](https://cloud.qdrant.io/)
* Practical Examples: [https://qdrant.tech/articles/practicle-examples/](https://qdrant.tech/articles/practicle-examples/)**
