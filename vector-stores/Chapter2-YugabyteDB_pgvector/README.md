# YugabyteDB + pgvector Demo

This repository demonstrates how to:

- Run YugabyteDB in Docker
- Enable the `pgvector` extension
- Store vector embeddings
- Perform similarity search
- Use HNSW for Approximate Nearest Neighbor (ANN) indexing
- Combine vector search with traditional SQL filtering

---

## 📂 Project Structure

```
docker-setup.shChapter2-YugabyteDB_pgvector/
│
├── scripts/
│   ├── docker-setup.sh         # Start YugabyteDB Docker container
│   ├── connect_sql.sh          # Connect to Yugabyte YSQL shell
│   └── load_data.sql           # SQL schema, inserts, and queries for demo
│
└── README.md                   # This file
```

---

## 🚀 Quick Start

### 1️⃣ Run YugabyteDB Docker container

```bash
bash scripts/docker-setup.sh
```

This will:

- Pull YugabyteDB Docker image `2.25.2.0-b359`
- Run container exposing ports 7000, 9000 (UI), 5433 (YSQL), etc.
- Start YugabyteDB server

### 2️⃣ Connect to YugabyteDB YSQL shell

```bash
bash scripts/connect_sql.sh
```

This opens `ysqlsh` with user `yugabyte`.

### 3️⃣ Load schema, data, and run queries

Inside `ysqlsh`, execute:

```sql
\i scripts/load_data.sql
```

This will:

- Enable the `pgvector` extension
- Create a `products` table with a VECTOR(3) column
- Insert 5 sample products with embeddings
- Create an HNSW index on the embedding column
- Run similarity and hybrid SQL + vector filtering queries

---

## 🔍 Example Similarity Query

```sql
SELECT id, name, category, embedding <-> '[0.12, 0.24, 0.31]' AS distance
FROM products
ORDER BY embedding <-> '[0.12, 0.24, 0.31]'
LIMIT 3;
```

---

## 🔍 Example Hybrid SQL + Vector Filter

```sql
SELECT name, category, description
FROM products
WHERE category = 'electronics'
AND created_at > NOW() - INTERVAL '30 days'
ORDER BY embedding <-> '[0.12, 0.24, 0.31]'
LIMIT 5;
```

---

## 🗂 Scripts Overview

### `scripts/run_yugabyte.sh`

```bash
#!/bin/bash
set -e

docker pull yugabytedb/yugabyte:2.25.2.0-b359

docker run -d --name yugabyte -p 7000:7000 -p 9000:9000 -p 15433:15433 -p 5433:5433 -p 9042:9042 \
yugabytedb/yugabyte:2.25.2.0-b359 bin/yugabyted start \
--background=false

echo "YugabyteDB is running"
```

### `scripts/connect_sql.sh`

```bash
#!/bin/bash
# Change the -h hostname with the correct hostname
docker exec -it yugabyte bin/ysqlsh -h 68d2a87797ad -U yugabyte -d yugabyte
```

### `scripts/load_data.sql`

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create products table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    embedding VECTOR(3),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert sample data
INSERT INTO products (name, category, description, embedding) VALUES
('iPhone 14 Pro', 'electronics', 'Latest smartphone with advanced camera', '[0.11, 0.22, 0.33]'), 
('Samsung Galaxy S23', 'electronics', 'Flagship Android phone with great display', '[0.10, 0.25, 0.30]'),
('Nike Air Max', 'apparel', 'Comfortable running shoes for daily use', '[0.80, 0.70, 0.60]'),
('Adidas Ultraboost', 'apparel', 'Premium running shoes with boost technology', '[0.82, 0.68, 0.65]'),
('MacBook Pro M2', 'electronics', 'High-performance laptop for professionals', '[0.15, 0.28, 0.35]');

-- Similarity search example
SELECT id, name, category, embedding <-> '[0.12, 0.24, 0.31]' AS distance
FROM products
ORDER BY embedding <-> '[0.12, 0.24, 0.31]'
LIMIT 3;

-- Create HNSW index
CREATE INDEX products_embedding_idx
ON products USING hnsw (embedding vector_l2_ops)
WITH (m = 16, ef_construction = 64);

-- Hybrid SQL + vector filtering
SELECT name, category, description
FROM products
WHERE category = 'electronics'
AND created_at > NOW() - INTERVAL '30 days'
ORDER BY embedding <-> '[0.12, 0.24, 0.31]'
LIMIT 5;
```

---

## References

- Pgvector extension in YugabyteDB: [https://docs.yugabyte.com/preview/explore/ysql-language-features/pg-extensions/extension-pgvector/](https://docs.yugabyte.com/preview/explore/ysql-language-features/pg-extensions/extension-pgvector/)
- Official pgvector GitHub Repository: [https://github.com/pgvector/pgvector](https://github.com/pgvector/pgvector)

Get started using YugabyteDB:[https://docs.yugabyte.com/latest/quick-start/docker/](https://docs.yugabyte.com/latest/quick-start/docker/)**

---
