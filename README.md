# 🏠 Real Estate AI Assistant (RAG Powered)

An intelligent Real Estate AI Assistant built using **Retrieval-Augmented Generation (RAG)** that answers user queries from real estate documents including brochures, payment plans, floor plans, RERA documents, possession guidelines, FAQs, customer support manuals, and policies.

Instead of relying on pretrained knowledge, the assistant retrieves relevant information from a local vector database and generates grounded responses using an LLM.

---

# Features

- Conversational AI Assistant
- Retrieval-Augmented Generation (RAG)
- Semantic Search using Sentence Transformers
- Local Vector Database (Qdrant)
- Multi-document Retrieval
- Memory-aware Conversations
- Source Citations
- Authentication System
- Beautiful Streamlit UI
- Production-ready Architecture

---

# Tech Stack

### Frontend
- Streamlit

### Backend
- Python
- LangChain

### Vector Database
- Qdrant

### Embedding Model
- sentence-transformers/all-MiniLM-L6-v2

### Large Language Model
- Groq
- Llama-3.3-70B-Versatile

### Document Processing

Supports

- PDF
- DOCX
- HTML
- Markdown
- TXT

---

# Project Architecture

```
                    User

                     │

                     ▼

             Streamlit Interface

                     │

                     ▼

               Conversation Memory

                     │

                     ▼

              Query Rewriter (Optional)

                     │

                     ▼

            Embedding Generation

                     │

                     ▼

             Qdrant Vector Database

                     │

         Top Relevant Chunks Retrieved

                     │

                     ▼

         Prompt Construction (Context)

                     │

                     ▼

             Groq Llama 3.3 70B

                     │

                     ▼

          Grounded Response + Citations
```

---

# Dataset

The knowledge base contains real estate documents such as

- Property Brochures
- Builder FAQs
- Floor Plans
- Payment Plans
- Possession Guidelines
- Registration Process
- Customer Support Documentation
- Privacy Policies
- RERA Guidelines

Documents are automatically indexed into Qdrant during ingestion.

---

# Project Structure

```
real_estate_rag_assistant/

│
├── app.py
├── ingest.py
├── requirements.txt
├── .env
│
├── data/
│
├── rag/
│   ├── chain.py
│   ├── embeddings.py
│   ├── llm.py
│   ├── loader.py
│   ├── memory.py
│   ├── retriever.py
│   ├── splitter.py
│   └── vector_store.py
│
├── ui/
│
├── utils/
│
└── qdrant_storage/
```

---

# Installation

Clone the repository

```bash
git clone <repository-url>

cd real_estate_rag_assistant
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```
GROQ_API_KEY=your_groq_api_key

QDRANT_PATH=./qdrant_storage

COLLECTION_NAME=real_estate_knowledge
```

---

# Build Vector Database

Before running the application, index the documents.

```bash
python ingest.py --reset
```

This will

- Load documents
- Split into chunks
- Generate embeddings
- Store vectors inside Qdrant

---

# Run Application

```bash
streamlit run app.py
```

---

# How It Works

## Step 1

User asks a question

Example

> What is the possession timeline for Skyline Horizon Towers?

---

## Step 2

The question is converted into an embedding.

---

## Step 3

Qdrant performs semantic similarity search.

---

## Step 4

Top relevant chunks are retrieved.

---

## Step 5

Retrieved chunks are passed to the LLM as context.

---

## Step 6

Groq Llama 3.3 generates an answer grounded only on the retrieved documents.

---

## Step 7

Relevant document citations are displayed to the user.

---

# Example Questions

- What is the payment schedule?
- Explain the registration process.
- What documents are required for possession?
- What are the RERA guidelines?
- Tell me about customer support.
- What amenities are available?
- What happens in case of delayed possession?
- What is the refund policy?

---

# Performance Optimizations

Implemented several optimizations for faster retrieval:

- Cached embedding model
- Cached vector database
- Lazy loading
- MMR Retrieval
- Normalized embeddings
- Semantic search using MiniLM
- Local Qdrant storage
- Streamlit resource caching

---

# Future Improvements

- Hybrid Search (BM25 + Dense Retrieval)
- Metadata Filtering
- Multi-query Retrieval
- Parent-Child Retrieval
- Cross Encoder Re-ranking
- OCR for scanned PDFs
- Streaming Responses
- Voice-based Assistant
- Docker Deployment
- Cloud Qdrant Support

---

# Screenshots

Add screenshots here after deployment.

Example

```
screenshots/
    login.png
    dashboard.png
    chat.png
```

---

# Deployment

The application can be deployed using

- Render
- Hugging Face Spaces
- Streamlit Community Cloud
- Docker
- Railway

---

# Author

**Nagamma Donda**

Bachelor of Technology (Computer Science)

AI / ML Engineer

GitHub:
https://github.com/Hemanagu

LinkedIn:
(Add your LinkedIn profile)

---
