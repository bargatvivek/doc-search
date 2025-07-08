# doc-search

## Overview

`doc-search` is a Python project for document searching using Retrieval-Augmented Generation (RAG) architecture. It supports semantic search, web search fallback, and integrates with LLMs for advanced question answering.

> **Note:**
> - This project requires [Ollama](https://ollama.com/) to be installed locally. You must also pull the required LLM model (e.g., `ollama pull phi3`) before running the server.
> - You need a valid [Serper API key](https://serper.dev/) for web search integration. Set it in your `.env` file as `SERPER_API_KEY`.

---

## Project Structure

```
doc-search/
│
├── server/
│   ├── main.py
│   ├── mcp_instance.py
│   ├── rag/
│   │   ├── web_search.py
│   │   ├── qa_chain.py
│   │   ├── retrieval.py
│   │   ├── llm_filter.py
│   │   └── rerank.py
│   ├── tools/
│   │   ├── upload.py
│   │   └── query.py
│   └── utils/
│       ├── config.py
│       ├── chunking.py
│       ├── logging.py
│       └── vectorstore.py
├── vectorstore/
│   └── chroma.sqlite3
├── requirement.txt
├── readme.md
└── .env
```

---

## Features

- Document upload and chunking
- Semantic search using vector embeddings
- RAG-based question answering
- Web search fallback (Google Search API)
- Metadata filtering
- LLM-based answer synthesis
- Modular and extensible workflows

---

## Explanation of Each Workflow

### 1. Upload Workflow

**Steps:**
1. User uploads documents via the upload tool.
2. Documents are chunked for efficient retrieval.
3. Chunks are embedded using the specified embedding model.
4. Embeddings and metadata are stored in the vector store.

### 2. Query Workflow

**Steps:**
1. User submits a query.
2. Query is embedded using the embedding model.
3. Relevant document chunks are retrieved from the vector store.
4. Metadata filters are applied to narrow results.
5. Retrieved chunks are logged for traceability.
6. LLM-based filtering refines the candidate chunks.
7. If no relevant documents are found, optionally fallback to web search.
8. The QA chain synthesizes a final answer using the LLM.
9. Results are returned to the user.

---

## RAG Architecture

Retrieval-Augmented Generation (RAG) combines information retrieval with generative models. The system retrieves relevant documents and augments the LLM's context, enabling more accurate and grounded answers.

---

## Web Search Integration

If no relevant local documents are found, the system can perform a web search using the Google Search API (requires `SERPER_API_KEY`). This ensures users get answers even when the local knowledge base is insufficient.

---

## Detailed Workflow of RAG Architecture

1. **User Query Submission:** User sends a question to the system.
2. **Query Embedding:** The query is converted into a vector using the embedding model.
3. **Document Retrieval:** The vector store retrieves top-k relevant document chunks.
4. **Metadata Filtering:** Only chunks matching the specified metadata (e.g., identifier) are considered.
5. **Log Retrieval Chunks:** Retrieved chunks are logged for debugging and traceability.
6. **LLM-Based Filtering:** The LLM filters and ranks the chunks for relevance.
7. **Handle No Relevant Documents:** If no chunks are relevant, the system can fallback to web search (if enabled).
8. **QA Chain:** The LLM synthesizes an answer from the filtered chunks or web results.
9. **Return Results:** The final answer and its source (local/web) are returned to the user.

---

## Summary of Workflow

- Upload documents → Chunk & embed → Store in vector store
- User query → Embed → Retrieve & filter → LLM answer synthesis
- Fallback to web search if needed

---

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- [Poetry](https://python-poetry.org/) or `pip` for dependency management

### 2. Clone the Repo

```sh
git clone <your-repo-url>
cd doc-search
```

### 3. Create a Virtual Environment

```sh
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```sh
pip install -r requirement.txt
```
or with Poetry:
```sh
poetry install
```

### 5. Configure Environment Variables

Edit `.env` with your API keys and settings:
```
SERPER_API_KEY=your_serper_api_key
LLM_MODEL=phi3
EMBEDDING_MODEL=phi3
VECTORSTORE_DIR=./vectorstore
TOP_K=5
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

### 6. Run the MCP Server

```sh
mcp dev server/main.py
```

---

## Usage

- **Upload documents:** Use the upload tool to add new documents to the vector store.
- **Query:** Use the query tool or API to ask questions. Set `use_web_search=True` to enable web fallback.

---

## Key Components

### 1. Vector Store

- Stores document embeddings and metadata.
- Uses ChromaDB for efficient similarity search.
- Supports filtering by document identifier and other metadata.

### 2. Web Search API

- Located in `server/rag/web_search.py`
- Uses Google Search API via `SERPER_API_KEY`
- Called automatically if no relevant local documents are found and web search is enabled.

### 3. QA Chain

- Located in `server/rag/qa_chain.py`
- Orchestrates retrieval, filtering, and answer synthesis using LLMs.

### 4. Tools

- **Upload Tool:** Handles document ingestion, chunking, and embedding.
- **Query Tool:** Handles user queries, document retrieval, LLM-based filtering, and web search fallback.
- Tools are registered with the MCP server and can be extended for additional workflows.

---

## Logging

- Logging is set up at server start and records all major workflow steps.
- Logs include document retrieval, chunking, filtering, and query processing.
- Log files are useful for debugging and workflow traceability.

---

## Troubleshooting

### 1. Logs Not Created

- Ensure logging is properly configured in `server/utils/logging.py`.
- Check file permissions and log file paths.

### 2. Tools Not Listed

- Make sure tools are imported and registered in `server/main.py`.
- Check for typos in tool decorators or registration code.

### 3. No Relevant Documents Found

- Verify documents are uploaded and indexed correctly.
- Check vector store path and embedding model configuration.
- Enable web search fallback if local results are insufficient.

---

## Future Enhancements

- Add support for more LLMs and embedding models.
- Integrate additional web search providers.
- Implement user authentication and access control.
- Enhance UI for document upload and query.
- Add analytics and usage dashboards.
- Improve error handling and reporting.

---

For more details, see the code and comments in each module.

---
