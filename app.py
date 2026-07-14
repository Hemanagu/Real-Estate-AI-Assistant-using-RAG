import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
import streamlit as st
import time
from pathlib import Path

# Load helpers first to configure logging and load env
from utils.helpers import load_environment, logger
load_environment()

# Page configuration
st.set_page_config(
    page_title="Real Estate AI Assistant",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply premium styling
from ui.styles import apply_custom_css
apply_custom_css()

# Import auth page
from ui.auth import show_login_page
from rag.memory import ConversationMemoryManager

# Initialize session states
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "memory" not in st.session_state:
    st.session_state.memory = ConversationMemoryManager()
if "chat_history_ui" not in st.session_state:
    # Separate UI history to store citations and timestamps alongside messages
    st.session_state.chat_history_ui = []

@st.cache_resource
def load_rag_pipeline():
    import time

    from rag.vector_store import QdrantVectorStoreManager
    from rag.retriever import RealEstateRetriever
    from rag.llm import get_llm
    from rag.chain import RAGChain

    start = time.time()

    t = time.time()
    manager = QdrantVectorStoreManager()
    print(f"Qdrant: {time.time()-t:.2f}s")

    t = time.time()
    retriever = RealEstateRetriever(manager)
    print(f"Retriever: {time.time()-t:.2f}s")

    t = time.time()
    llm = get_llm()
    print(f"LLM: {time.time()-t:.2f}s")

    t = time.time()
    chain = RAGChain(retriever, llm)
    print(f"Chain: {time.time()-t:.2f}s")

    print(f"TOTAL: {time.time()-start:.2f}s")

    return manager, chain

def render_citations(docs) -> str:
    """Renders document citations in a beautiful, structured HTML card format."""
    if not docs:
        return ""
        
    citations = []
    seen = set()
    for doc in docs:
        source = doc.metadata.get("source", "Unknown Document")
        page = doc.metadata.get("page", 1)
        file_type = doc.metadata.get("file_type", "TXT")
        
        # Deduplicate citations for cleaner look
        citation_key = (source, page)
        if citation_key not in seen:
            seen.add(citation_key)
            citations.append((source, page, file_type))

    html = """
    <div class="citation-container">
        <div class="citation-title">📚 Source Citations:</div>
    """
    for src, pg, ftype in citations:
        page_str = f" | Page {pg}" if ftype == "PDF" else ""
        html += f'<span class="citation-item">[{ftype}] {src}{page_str}</span>'
    html += "</div>"
    return html

def main():
    # 1. Auth Gate
    if not st.session_state.authenticated:
        show_login_page()
        return

    db_manager = None
    rag_chain = None

    vector_store_online = False
    doc_count = "Not Loaded"

    if st.session_state.get("rag_loaded", False):
        db_manager, rag_chain = load_rag_pipeline()

        if db_manager:
            vstore = db_manager.get_vector_store()
            if vstore:
                vector_store_online = True

            try:
                res = db_manager.client.get_collection(
                    db_manager.collection_name
                )
                doc_count = res.points_count
            except Exception:
                doc_count = "N/A"

    with st.sidebar:
        st.markdown(
            f"""
            <div style='text-align: center; margin-bottom:20px;'>
                <h3 style='margin:0;color:#a5b4fc;'>🏠 Agent Console</h3>
                <p style='color:#94a3b8;font-size:13px;'>Logged in as:
                <b>{st.session_state.username}</b></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown("#### ⚡ System Status")

        if vector_store_online:
            st.success("Qdrant DB: Connected")
            st.info(f"Indexed Chunks: {doc_count}")
        else:
            st.info("Waiting for first query...")
            st.warning("Run: `python ingest.py --reset` to build search index.")

        st.markdown("---")

        if st.button("🔄 Clear Conversation"):
            st.session_state.memory.clear()
            st.session_state.chat_history_ui = []
            st.rerun()

        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.memory.clear()
            st.session_state.chat_history_ui = []
            st.rerun()

    st.markdown(
        """
        <div class="app-title-banner">
            <h1>Real Estate AI Advisor</h1>
            <p>Production RAG-enabled agent.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not vector_store_online:
        st.info(
    "💡 The AI model will be initialized automatically when you ask your first question."
)

    for chat in st.session_state.chat_history_ui:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])
            if chat.get("citations"):
                st.markdown(chat["citations"], unsafe_allow_html=True)

    if prompt := st.chat_input(
        "Ask a question about brochures, listings, RERA, floor plans, or policies..."
    ):
        if not st.session_state.get("rag_loaded", False):
            with st.spinner("🚀 Initializing AI Assistant..."):
                db_manager, rag_chain = load_rag_pipeline()
                st.session_state.rag_loaded = True
                vector_store_online = True
                try:
                    res = db_manager.client.get_collection(db_manager.collection_name)
                    doc_count = res.points_count
                except Exception:
                    doc_count = "N/A"
        else:
            db_manager, rag_chain = load_rag_pipeline()

        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.chat_history_ui.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("assistant"):
            if not rag_chain:
                msg = "I'm sorry, but my knowledge base is currently offline."
                st.markdown(msg)
                st.session_state.chat_history_ui.append(
                    {"role": "assistant", "content": msg}
                )
            else:
                with st.spinner("Analyzing knowledge base & reasoning..."):
                    answer, retrieved_docs = rag_chain.run(
                        st.session_state.memory, prompt
                    )
                    citations_html = render_citations(retrieved_docs)
                    st.markdown(answer)
                    if citations_html:
                        st.markdown(citations_html, unsafe_allow_html=True)
                    st.session_state.chat_history_ui.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "citations": citations_html,
                        }
                    )
        st.rerun()


if __name__ == "__main__":
    main()
