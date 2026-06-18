
# Engineering Assist

**A lightweight, cost-efficient, offline-first Engineering Intelligence Platform** for technical teams.

Built for engineers working with manuals, drawings, safety documents, SOPs, and part specifications.

## 🎯 Features

- **Hybrid Retrieval** — BM25 (keyword) + Dense Vector Search (mxbai-embed-xsmall-v1)
- **Multi-format Support** — PDF, DOCX, TXT, Images (with OCR)
- **Smart Mixed Content Handling** — Text + Image pages in PDFs
- **Chunking with Metadata** — Page number, source, type preserved
- **Citation System** — Traceable answers with source & page references
- **Lightweight & Offline** — No heavy LLMs, runs on CPU
- **Query Processing** — Cleaning + Keyword Extraction using spaCy
- **Modular LangGraph Architecture** — Easy to extend
- **Logging & Environment Management** — Clean production setup
- **FastAPI Ready** — Can be converted into API easily

---

## 🏗️ Architecture

### High-Level Flow

```
User Query / File Upload
        ↓
   File Router
        ↓
   Parser (pdfplumber + OCR fallback)
        ↓
   Chunking (Recursive + Cleaning)
        ↓
   Embedding + Storage (ChromaDB)
        ↓
   Query Processing (spaCy)
        ↓
   Hybrid Retrieval (BM25 + Dense)
        ↓
   Reranker 
        ↓
   Citation Builder
        ↓
   Response Generator
```

### Phase 1 (Current)
- Ingestion Pipeline (Parser → Chunking → Embedding)
- Hybrid Retrieval + Response

### Phase 2 (Future)
- Knowledge Graph (Neo4j)
- Engineering Rule Engine
- Fine-tuned Domain Embedding Model
- Multi-user + Access Control

## 📁 Modular Code Structure

```bash
engineering-assist/
├── .env
├── main.py
├── workflow.py                     # orchestration layer
├── requirements.txt
├── README.md
│
├── config/
│   └── settings.py                 # Environment & config
│
├── models/
│   └── embedding.py                # EmbeddingModel class
│
├── database/
│   ├── chroma_client.py
│   └── vector_store.py             # ChromaDB operations
│
├── nodes/
│   ├── ingestion/
│   │   ├── file_router.py
│   │   ├── parser_node.py
│   │   ├── chunking_node.py
│   │   └── embedding_storage.py
│   ├── retrieval/
│   │   ├── query_processing.py
│   │   ├── hybrid_retriever.py
│   │   └── reranker.py
│   └── response/
│       ├── citation_builder.py
│       └── response_generator.py
│
├── schemas/
│   └── graph_state.py            # LangGraph State
│
├── utils/
│   ├── logger.py
│   └── helpers.py
│
└── data/
    └── uploads/                    # Uploaded documents
```

---

## 🚀 Key Technologies

- **LangGraph** — Workflow orchestration
- **ChromaDB** — Vector database
- **Sentence-Transformers** — Embeddings (`mxbai-embed-xsmall-v1`)
- **spaCy** — NLP for query processing
- **pdfplumber + pytesseract** — Document parsing
- **rank-bm25** — Keyword search
- **python-dotenv** — Environment management

---

## 🛠️ How to Run

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```
3. Create `.env` file (see example)
4. Run:
   ```bash
   python main.py
   ```

---

## 📌 Future Enhancements

- Domain-specific fine-tuned embedding model
- Knowledge Graph integration
- FastAPI backend + UI
- Multi-file & conversation memory
- Safety rule validation engine
