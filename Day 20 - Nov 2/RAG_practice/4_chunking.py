"""STEP 4 — Split the full document into overlapping token-based chunks."""
from rag_core import TOKENIZER, make_chunks, read_document

alltext = read_document()
for text in alltext:
    chunks = make_chunks(text, chunk_size=120, overlap=20)
    print("Total chunks:", len(chunks))
    print("Chunk size: 120 tokens, overlap: 20 tokens\n")

    for i, chunk in enumerate(chunks, start=1):
        print("=" * 70)
        print(f"CHUNK {i} | {len(TOKENIZER.encode(chunk))} tokens")
        print(chunk[:600] + ("..." if len(chunk) > 600 else ""))

    print("\n---------------------------------------------")