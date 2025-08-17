# Chapter 3 - Milvus + Zilliz Cloud Demo

This repository demonstrates how to use **Milvus** for vector similarity search,
both in a **self-hosted setup (Docker)** and in **Zilliz Cloud (managed Milvus)**.

## 📂 Project Structure

```
Chapter3-Milvus/
├── README.md
├── requirements.txt
└── scripts/
    ├── milvus-selfhosted-demo.py
    └── zillizcloud-demo.py
```

---

## **Install Milvus in Docker**

Run the following commands:

```
pip install -U pymilvus
```

Download Milvus standalone script

```
curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh -o standalone_embed.sh
```

Start Milvus. This script runs Docker containers (Milvus standalone + dependencies).

```
bash standalone_embed.sh start
```

If you encounter a **Docker mount permission error** like:

```
docker: Error response from daemon: error while creating mount source path ... permission denied.
```

✅  **Fix (macOS Docker Desktop users)** :

Switch file-sharing to **gRPC-FUSE**

* Open **Docker Desktop → Settings → General**
* Enable **Use gRPC-FUSE for file sharing**
* Apply and **Restart Docker**

Then run:

```
mkdir -p ~/milvus/volumes
chmod -R 777 ~/milvus/volumes
bash standalone_embed.sh start
```

If successful, you should see:

Wait for Milvus Starting...
Start successfully.

📌  **Default configuration after startup** :

* **Milvus Server** : `localhost:19530`
* **Embedded etcd** : port `2379`
* **Data volume** : `~/milvus/volumes`
* **WebUI** : [http://127.0.0.1:9091/webui/](http://127.0.0.1:9091/webui/)

---

## 🚀 Self-hosted Demo

Run the Python demo:

```bash
python milvus-selfhosted-demo.py
```

This script will:

- Create a collection with embeddings
- Insert sample data
- Run similarity search queries

---

## ☁️ Zilliz Cloud Setup

1. Sign up at [https://zilliz.com/cloud](https://zilliz.com/cloud)
2. Create a free cluster
3. Copy the **API key** and **endpoint**
4. Update the values in `zillizcloud-demo.py`

Run the demo:

```bash
python zillizcloud-demo.py
```

This script will:

- Use the default embedding function
- Insert and query vectors
- Demonstrate semantic search

---

## 🗂 References

- Milvus open-source database: [https://milvus.io/docs/overview.md](https://milvus.io/docs/overview.md)
- Zilliz Cloud(fully managed Milvus cloud): [https://docs.zilliz.com/docs/home](https://docs.zilliz.com/docs/home)
- Integrations: [https://milvus.io/docs/integrations_overview.md](https://milvus.io/docs/integrations_overview.md)
