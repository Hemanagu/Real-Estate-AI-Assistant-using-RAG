# 🏠 Real Estate AI Assistant

An intelligent **Retrieval-Augmented Generation (RAG)** application that helps users answer questions about real estate projects using natural language. The assistant retrieves relevant information from property documents such as brochures, RERA guidelines, payment plans, FAQs, possession guidelines, and customer support documents before generating accurate responses using an LLM.

The application is built with **Streamlit**, **LangChain**, **Qdrant**, **Sentence Transformers**, and **Groq Llama 3.3 70B**.

---

## 🚀 Features

- 🔍 Retrieval-Augmented Generation (RAG)
- 📄 Multi-format document ingestion
  - PDF
  - DOCX
  - HTML
  - Markdown
- 🧠 Semantic search using Sentence Transformers
- 🗂️ Local Qdrant Vector Database
- 🎯 MMR (Maximum Marginal Relevance) Retrieval
- 💬 Conversational AI with chat history
- 📚 Source citations for every response
- ⚡ Cached pipeline for improved performance
- 🔐 Basic Authentication
- 🎨 Modern Streamlit UI
- ☁️ Ready for deployment on Render

---

# 🏗️ Project Architecture

```
Documents
    │
    ▼
Document Loader
    │
    ▼
Document Splitter
    │
    ▼
Sentence Transformer Embeddings
    │
    ▼
Qdrant Vector Database
    │
    ▼
Retriever (MMR Search)
    │
    ▼
Prompt Construction
    │
    ▼
Groq Llama 3.3 70B
    │
    ▼
Final Answer + Source Citations
```

---

# 📂 Supported Documents

The assistant can ingest and search across:

- Property Brochures
- RERA Information
- Payment Plans
- Possession Guidelines
- Registration Process
- Customer Support Documents
- FAQs
- Builder Policies

---

# 🛠️ Tech Stack

### Frontend

- Streamlit

### Backend

- Python
- LangChain

### Vector Database

- Qdrant (Local)

### Embedding Model

- sentence-transformers/all-MiniLM-L6-v2

### Large Language Model

- Groq
- Llama-3.3-70B-Versatile

### Libraries

- LangChain
- Sentence Transformers
- Qdrant Client
- HuggingFace Embeddings
- Streamlit

---

# 🔐 Authentication

The application includes a simple login system to restrict access to the chatbot.

### Default Credentials

**Username**

```
admin
```

**Password**

```
realestate2026
```

### Authentication Features

- Username & Password login
- Session-based authentication
- Protected chatbot interface
- Logout functionality
- Conversation history cleared on logout

> **Note:** This authentication mechanism is intended for demonstration purposes. For production deployments, secure authentication methods such as password hashing, JWT/OAuth2, HTTPS, and database-backed user management should be implemented.

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/real_estate_rag_assistant.git

cd real_estate_rag_assistant
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ⚙️ Environment Variables

Create a `.env` file in the project root.

Example

```env
GROQ_API_KEY=your_groq_api_key

QDRANT_PATH=./qdrant_storage

QDRANT_COLLECTION=real_estate_knowledge
```

---

# 📚 Build the Vector Database

Run the ingestion script

```bash
python ingest.py --reset
```

This command

- Loads all supported documents
- Splits them into chunks
- Generates embeddings
- Stores embeddings in Qdrant

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

The application will be available at

```
http://localhost:8501
```

---

# 💬 Example Questions

- What is the possession timeline for Skyline Horizon Towers?
- Explain the payment plan for Meridian Greens Residency.
- What documents are required during registration?
- What happens if possession is delayed?
- What amenities are available in Urban Nest Riverside?
- What are the RERA guidelines for buyers?
- Explain the cancellation policy.
- What customer support channels are available?

---

# 📚 Retrieval Pipeline

1. User submits a question.
2. Conversation history is considered.
3. Query is converted into embeddings.
4. Qdrant retrieves the most relevant document chunks using MMR.
5. Retrieved chunks are passed to the LLM.
6. Groq Llama generates an answer strictly based on the retrieved context.
7. Source citations are displayed alongside the response.

---

# 📊 Key Features

- Semantic Vector Search
- MMR Retrieval
- Context-Aware Conversations
- Retrieval-Augmented Generation
- Source Attribution
- Multi-document Reasoning
- Fast Local Vector Database
- Cached Initialization
- Modern Responsive UI

---

# 📁 Project Structure

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
│   ├── embeddings.py
│   ├── loader.py
│   ├── splitter.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── llm.py
│   ├── chain.py
│   └── memory.py
│
├── ui/
│
├── utils/
│
└── qdrant_storage/
```

---

# 🚀 Deployment

This application is fully compatible with **Render** deployment.

Deployment steps:

1. Push the project to GitHub.
2. Create a new Web Service on Render.
3. Connect the GitHub repository.
4. Add the required environment variables:
   - `GROQ_API_KEY`
5. Deploy the application.

---

# 📌 Future Improvements

- Cloud-hosted Qdrant
- User Registration
- Role-Based Access Control (RBAC)
- Hybrid Search (BM25 + Vector Search)
- Streaming Responses
- PDF Upload and Dynamic Ingestion
- OCR Support
- Voice Input
- Multi-language Support
- Admin Dashboard

---

# 👩‍💻 Author

**Nagamma Donda**

B.Tech in Computer Science and Engineering

AI / Machine Learning Enthusiast

---

## ⭐ If you found this project useful, consider giving it a star!
