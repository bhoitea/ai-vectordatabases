# Weaviate Semantic Search Demos

This chapter demonstrates how to use **Weaviate** for semantic search, both in local (self-hosted) and cloud environments.

---

## 📂 Project Structure

```warp-runnable-command
Chapter2-Weaviate/
│
├── scripts/
│   ├── docker-run.sh                       # Start Weaviate in Docker
│   ├── self_hosted_telecom_demo.py         # Telecom Call Summary Semantic Search (local demo)
│   └── cloud_jeopardy_semantic_search_demo.py # Jeopardy! Q&A search (cloud demo)
│
└── README.md                               # This file
```

---

## 🚀 Quick Start

### 1️⃣ Run Weaviate in Docker

```warp-runnable-command
docker run -p 8081:8080 -p 50051:50051 cr.weaviate.io/semitechnologies/weaviate:1.31.5
```

Once started, confirm readiness:

```warp-runnable-command
curl -i http://localhost:8081/v1/.well-known/live
```

Expected response:

```warp-runnable-command
HTTP/1.1 200 OK
Date: Sat, 12 Jul 2025 14:40:54 GMT
Content-Length: 0
```

Once started, confirm readiness using [http://localhost:8081/v1](http://localhost:8081/v1) URL:

---

### 2️⃣ Install Python Client

Weaviate’s Python client works with Python  **3.8+** . Install from PyPI:

```warp-runnable-command
pip install -U weaviate-client
```

---

### 3️⃣ Run Telecom Call Summary Search (Local Demo)

```warp-runnable-command
python scripts/self_hosted_telecom_demo.py
```

This script connects to your **local Docker Weaviate instance** and demonstrates telecom call summary semantic search.

---

### 4️⃣ Run Jeopardy! Q&A Search (Cloud Demo)

```warp-runnable-command
python scripts/cloud_jeopardy_semantic_search_demo.py
```

This script connects to a **cloud-hosted Weaviate instance** and demonstrates Jeopardy-style semantic Q&A search.

---

## 📑 References

* Weaviate Database Documentation:[https://docs.weaviate.io/weaviate](https://docs.weaviate.io/weaviate)
* Weaviate Cloud Documentation: [https://docs.weaviate.io/cloud](https://docs.weaviate.io/cloud)
* Concepts and Architecture: [https://docs.weaviate.io/weaviate/concepts](https://docs.weaviate.io/weaviate/concepts)
* Model Integrations:[https://docs.weaviate.io/weaviate/model-providers](https://docs.weaviate.io/weaviate/model-providers)
* API Reference:[https://docs.weaviate.io/weaviate/config-refs](https://docs.weaviate.io/weaviate/config-refs)
* Installation Guides:[https://docs.weaviate.io/deploy/installation-guides](https://docs.weaviate.io/deploy/installation-guides)
