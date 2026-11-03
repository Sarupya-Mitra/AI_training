# LangChain:
Before learning about LangChain we need to first know about Retrieval Augmented Generation(RAG).
## What is RAG?
RAG augments a LLM's text generation capabilities by retrieving external information from different sources like documents and databases.

So RAG invloves the following steps:
1) *Document Loader and Chunking* - External documents are loaded and then broken into smaller "chunks" for indexing.
2) *Embedding* - The text chunks are converted into numerical vectors which holds the semantic relation between words, hence capturing the meaning.
3) *Storing in Vector DB* - The embedding vectors are stored in specialised databases which has the capabilities of storing vectors. 
4) *Searching the Vector DB* - Using the index, the different chunks, which are relevant to answer the user's queries, are efficiently retrieved.
5) *Feed to LLM* - The retrieved chunks are fed into the LLM, which then generates a coherent response.

## What is LangChain?
LangChain is the software toolkit that helps developers to build RAG applications. So RAG is basically a theoretical design strategy while, LangChain is the practical software library that helps realizing that design pattern.

## LangChain's Roles and Contributions:
- LangChain provides sophisticated algorithms for rapid and accurate information retrieval within large datasets.
- It also provides tools to analyze the retrieved data and understand the relationships between components, allowing the LLM to interpret the data and efficiently utilize it for the task at hand.
- It also simplifies the RAG integration into various applications.

