# Pinecone Demo

This repository demonstrates how to:

* Connect to Pinecone with an API key
* Create indexes
* Upsert vectors with metadata
* Perform similarity search
* Apply metadata filters for hybrid queries
* Understand cosine similarity scores

---

## 📂 Project Structure

<pre class="overflow-visible!" data-start="468" data-end="638"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"><span class="" data-state="closed"></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>Chapter1-Pinecone/
│
├── scripts/
│   └── pinecone_demo.py        # Script </span><span>to</span><span></span><span>create</span><span></span><span>index</span><span>, </span><span>insert</span><span> data, run queries
│
└── README.md                   # This file
</span></span></code></div></div></pre>

---

## 🚀 Quick Start

### 1️⃣ Install dependencies

```
pip install pinecone
```

---

### 2️⃣ Set your API key

Update `pinecone_demo.py` with your Pinecone API key:

```
pc = Pinecone(api_key="pcsk_3g5ZMv_ZEf5gFp1bLeGF*******", environment="us-east-1-aws")**
```

---

### 3️⃣ Run the demo

```
python3 scripts/pinecone_demo.py
```

This will:

* Create a Pinecone index
* Insert 3 sample vectors (A, B, C) with metadata
* Query with a vector and metadata filter
* Return similarity results

---

## 🔍 Example Similarity Query

<pre class="overflow-visible!" data-start="1143" data-end="1316"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"><span class="" data-state="closed"></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>query_response = index.query(
    vector=[</span><span>0.11</span><span>] * </span><span>1536</span><span>,
    top_k=</span><span>2</span><span>,
    include_metadata=</span><span>True</span><span>,
    </span><span>filter</span><span>={</span><span>"genre"</span><span>: {</span><span>"$eq"</span><span>: </span><span>"comedy"</span><span>}}
)
</span><span>print</span><span>(query_response)
</span></span></code></div></div></pre>

```
query_response = index.query(   
vector=[0.11] * 1536,   
top_k=2,   
include_metadata=True,   
filter={"genre": {"$eq": "comedy"}} ) print(query_response)
```

---

## ✅ Expected Output

The query vector `[0.11] * 1536` is very close to:

* **A** → `[0.1] * 1536` (comedy)
* **B** → `[0.15] * 1536` (comedy)

But far from:

* **C** → `[0.5] * 1536` (thriller, excluded by filter)

So the result will include **A and B** with similarity ≈  **1.0** , excluding  **C** .

---

## References

* Pinecone Database:  https://docs.pinecone.io/guides/get-started/overview
* Pinecone Assistant:[https://docs.pinecone.io/guides/assistant/overview](https://docs.pinecone.io/guides/assistant/overview)
* SDK Reference –SDKs (Python, Node.js, etc.) and API usage. [https://docs.pinecone.io/reference/pinecone-sdks](https://docs.pinecone.io/reference/pinecone-sdks)
