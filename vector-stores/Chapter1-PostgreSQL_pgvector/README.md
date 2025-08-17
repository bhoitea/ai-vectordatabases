# PostgreSQL + pgvector: Product Similarity Search Demo

This repository contains a quick demo showing how to:

- Run PostgreSQL with the **pgvector** extension in Docker
- Create a table with vector embeddings
- Insert sample products with embeddings
- Create an HNSW index for Approximate Nearest Neighbor (ANN) search
- Run similarity queries using Euclidean distance

---

## 📂 Project Structure

```
Chapter1-PostgreSQL_pgvector/
│
├── scripts/
│   ├── docker-setup.sh        # Script to pull and run PostgreSQL with pgvector in Docker
│   └── sample-products.sql    # SQL commands to enable pgvector, create table, insert data, index vectors, and run similarity queries
│
└── README.md                   # This file
```

---

## 🚀 Quick Start

### 1️⃣ Start PostgreSQL with pgvector

```bash
bash scripts/docker-setup.sh
```

This will:

- Pull the ankane/pgvector Docker image
- Run PostgreSQL with pgvector extension installed
- Set password to pgpass
- Expose port 5432

### 2️⃣ Connect to PostgreSQL

```bash
docker exec -it pgvector-quick psql -U postgres
```

### 3️⃣ Run the SQL Demo

Inside the psql shell:

```sql
\i scripts/sample-products.sql
```

This will:

- Enable the pgvector extension
- Create a products table with a VECTOR(3) column
- Insert 4 sample products with embeddings
- Create an HNSW index for fast ANN search
- Run a similarity search to find the 3 closest products to [0.88,0.12,0.2]

---

## 🔍 Example Query Output

```
 id |   name    |            description             | description_embedding
----+-----------+------------------------------------+-----------------------
  1 | iPhone 14 | Smartphone with great camera       | [0.9, 0.1, 0.2]
  2 | Pixel 7   | Affordable phone with good photos  | [0.85, 0.15, 0.25]
  3 | Galaxy S22| Android phone with sharp display   | [0.8, 0.2, 0.1]
(3 rows)
```

---

## 📚 Notes

- `<->` is the Euclidean distance operator in pgvector.
- `VECTOR(3)` specifies 3D vectors (adjust for your embeddings).
- HNSW indexing (`USING hnsw`) speeds up searches for large datasets.
- You can adapt this to store embeddings from OpenAI, Cohere, or Sentence Transformers.

---

## References

* Official pgvector GitHub Repository: [ https://github.com/pgvector/pgvector](https://github.com/pgvector/pgvector)
* pgvector FAQ: [ https://github.com/pgvector/pgvector?tab=readme-ov-file#frequently-asked-questions](https://github.com/pgvector/pgvector?tab=readme-ov-file#frequently-asked-questions)**
