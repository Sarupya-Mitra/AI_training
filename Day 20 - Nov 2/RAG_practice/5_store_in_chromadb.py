"""STEP 5 — Embed each chunk, save its vector and text into local ChromaDB."""
from rag_core import (
    COLLECTION_NAME, DB_PATH, DOCUMENT_PATHS, PROJECT_DIR,
    embed_texts, get_database, make_chunks, read_document,
)
client = get_database()
all_chunks = []
all_vectors = []
all_ids = []
all_metadatas = []

for i,doc in enumerate(read_document()):
    filechunks = make_chunks(doc, chunk_size=120, overlap=20)
    print(f"1. Created {len(filechunks)} text chunks for document {i+1}.")

    vectors = embed_texts(filechunks)
    print(f"2. Created {len(vectors)} embeddings; each has {len(vectors[0])} values.")

    # Add chunks and embeddings to master lists
    all_chunks.extend(filechunks)
    all_vectors.extend(vectors)

    # Generate unique IDs and metadata
    for j, chunk in enumerate(filechunks):

        all_ids.append(f"doc_{i+1}_chunk_{j+1:03d}")

        all_metadatas.append({
            "source": f"{i+1}.txt",
            "chunk_number": j+1
        })

# Re-create the collection so re-running the script removes stale old chunks.
if COLLECTION_NAME in [collection.name for collection in client.list_collections()]:
    client.delete_collection(COLLECTION_NAME)

collection = client.create_collection(
    name=COLLECTION_NAME,
    embedding_function=None,
    configuration={"hnsw": {"space": "cosine"}},
)

# Store ALL chunks from BOTH documents
collection.add(
    ids=all_ids,
    documents=all_chunks,
    embeddings=all_vectors,
    metadatas=all_metadatas
)

print(f"3. Stored {collection.count()} searchable chunks in ChromaDB.")
print(f"4. Database folder: {DB_PATH}")
# print("5. Sample IDs:", ids[:5])
# print("\nNow run 06_search_chroma.py.")
