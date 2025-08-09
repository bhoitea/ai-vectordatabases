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
