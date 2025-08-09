--Inside the psql shell, enable the pgvector extension (only needs to be done once per database)
CREATE EXTENSION IF NOT EXISTS vector;

--Create a products table with a vector column (3D vectors in this example)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    description_embedding VECTOR(3)
);

--Insert sample products with semantic vector embeddings for descriptions
INSERT INTO products (name, description, description_embedding) VALUES
('iPhone 14', 'Smartphone with great camera', '[0.9,0.1,0.2]'),
('Pixel 7', 'Affordable phone with good photos', '[0.85,0.15,0.25]'),
('Galaxy S22', 'Android phone with sharp display', '[0.8,0.2,0.1]'),
('Canon EOS', 'DSLR camera for photography', '[0.2,0.9,0.4]');

-- Create HNSW index on the vector column
CREATE INDEX ON products USING hnsw (description_embedding vector_l2_ops);

-- Temporarily turn off seq scan for testing index
SET enable_seqscan = off;

-- Perform a vector similarity search using the <-> (Euclidean distance) operator
-- Retrieve the top 3 products closest to the query vector [0.88,0.12,0.2]
SELECT id, name, description, description_embedding
FROM products
ORDER BY description_embedding <-> '[0.88,0.12,0.2]'
LIMIT 3;

