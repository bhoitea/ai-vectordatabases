import redis
import numpy as np

# Connect to Redis Stack
r = redis.Redis(host='localhost', port=6379, decode_responses=False)

def create_vector_index():
    """
    Create a RediSearch index optimized for vector search using HNSW algorithm.
    This index supports both vector similarity and traditional text/tag filtering.
    """
    try:
        r.execute_command(
            "FT.CREATE", "ai_docs_index",      # Index name
            "ON", "HASH",                      # Use Redis HASH data structure
            "PREFIX", "1", "doc:",             # Index keys starting with 'doc:'
            "SCHEMA",                          # Define searchable fields
            "title", "TEXT", "WEIGHT", "2.0",  # Title field with higher weight
            "content", "TEXT",                 # Full-text searchable content
            "category", "TAG",                 # Category for filtering
            "timestamp", "NUMERIC",            # Timestamp for time-based queries
            "embedding", "VECTOR", "HNSW", "6", # Vector field configuration
            "TYPE", "FLOAT32",                 # Vector data type
            "DIM", "1536",                     # Dimensionality (matches OpenAI)
            "DISTANCE_METRIC", "COSINE"        # Similarity metric
        )
        print("✅ Vector index created successfully")
    except redis.exceptions.ResponseError as e:
        if "Index already exists" in str(e):
            print("ℹ️ Index already exists, continuing...")
        else:
            raise e

def insert_document(doc_id, title, content, category, embedding_vector):
    """
    Insert a document with its embedding into Redis.
    Each document is stored as a Redis Hash with multiple fields.
    """
    # Convert numpy array to bytes for Redis storage
    embedding_bytes = embedding_vector.astype('float32').tobytes()
    
    # Store document with all metadata
    doc_key = f"doc:{doc_id}"
    r.hset(doc_key, mapping={
        "title": title,
        "content": content,
        "category": category,
        "timestamp": int(np.random.uniform(1640995200, 1672531200)),  # Random timestamp
        "embedding": embedding_bytes
    })
    print(f"📄 Document '{title}' inserted with key {doc_key}")

def vector_search(query_embedding, k=5, category_filter=None):
    """
    Perform semantic vector search with optional category filtering.
    Returns the k most similar documents.
    """
    query_bytes = query_embedding.astype('float32').tobytes()
    
    # Build search query with optional filtering
    search_query = "*"
    if category_filter:
        search_query = f"@category:{{{category_filter}}}"
    
    # Add KNN vector search clause
    search_query += f"=>[KNN {k} @embedding $query_vec AS similarity_score]"
    
    # Execute the search
    results = r.execute_command(
        "FT.SEARCH", "ai_docs_index",
        search_query,
        "PARAMS", "2", "query_vec", query_bytes,
        "SORTBY", "similarity_score",
        "RETURN", "4", "title", "category", "similarity_score", "content",
        "DIALECT", "2"
    )
    
    return parse_search_results(results)

def parse_search_results(raw_results):
    """
    Parse Redis search results into a more readable format.
    """
    if not raw_results or raw_results[0] == 0:
        return []
    
    total_results = raw_results[0]
    results = []
    
    # Parse results (format: [total, key1, fields1, key2, fields2, ...])
    for i in range(1, len(raw_results), 2):
        doc_key = raw_results[i].decode() if isinstance(raw_results[i], bytes) else raw_results[i]
        fields = raw_results[i + 1]
        
        # Convert field list to dictionary
        doc = {"key": doc_key}
        for j in range(0, len(fields), 2):
            field_name = fields[j].decode() if isinstance(fields[j], bytes) else fields[j]
            field_value = fields[j + 1].decode() if isinstance(fields[j + 1], bytes) else fields[j + 1]
            doc[field_name] = field_value
        
        results.append(doc)
    
    return results

def main():
    """
    Demonstrate complete Redis Vector workflow
    """
    print("🚀 Redis Vector Demo Starting...")
    
    # Step 1: Create the vector index
    create_vector_index()
    
    # Step 2: Generate sample documents with embeddings
    documents = [
        {
            "id": "1",
            "title": "AI in Legal Technology",
            "content": "Artificial intelligence is revolutionizing the legal industry through document analysis and case prediction.",
            "category": "legal"
        },
        {
            "id": "2", 
            "title": "Machine Learning for Finance",
            "content": "Financial institutions are leveraging ML algorithms for fraud detection and risk assessment.",
            "category": "finance"
        },
        {
            "id": "3",
            "title": "Healthcare AI Applications", 
            "content": "AI-powered diagnostic tools are improving patient outcomes and reducing healthcare costs.",
            "category": "healthcare"
        }
    ]
    
    # Step 3: Insert documents with random embeddings (in production, use real embeddings)
    for doc in documents:
        embedding = np.random.rand(1536)  # Simulate OpenAI embedding
        insert_document(doc["id"], doc["title"], doc["content"], doc["category"], embedding)
    
    # Step 4: Perform semantic search
    print("\n🔍 Performing vector similarity search...")
    query_embedding = np.random.rand(1536)  # Simulate query embedding
    
    # Search all documents
    all_results = vector_search(query_embedding, k=3)
    print(f"\n📋 Found {len(all_results)} similar documents:")
    for result in all_results:
        print(f"  • {result['title']} (Category: {result['category']}, Score: {result['similarity_score']})")
    
    # Search with category filter
    legal_results = vector_search(query_embedding, k=2, category_filter="legal")
    print(f"\n⚖️ Legal documents only ({len(legal_results)} found):")
    for result in legal_results:
        print(f"  • {result['title']} (Score: {result['similarity_score']})")

if __name__ == "__main__":
    main()