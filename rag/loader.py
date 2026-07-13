import os
from pathlib import Path
from typing import List
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
import docx2txt
from utils.helpers import logger

class DocumentLoader:
    """Recursively scans a directory and loads documents of various formats (PDF, DOCX, HTML, MD, TXT)."""

    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory {data_dir} does not exist.")

    def load_all(self) -> List[Document]:
        """Scans the directory recursively and loads all supported documents."""
        documents = []
        supported_extensions = {".pdf", ".docx", ".html", ".htm", ".md", ".txt"}
        
        logger.info(f"Scanning directory: {self.data_dir}")
        
        # Traverse the directory recursively
        for root, _, files in os.walk(self.data_dir):
            for file in files:
                file_path = Path(root) / file
                ext = file_path.suffix.lower()
                
                if ext not in supported_extensions:
                    continue
                
                try:
                    logger.info(f"Loading file: {file_path.relative_to(self.data_dir)}")
                    docs = self._load_file(file_path, ext)
                    documents.extend(docs)
                except Exception as e:
                    logger.error(f"Failed to load file {file_path}: {e}", exc_info=True)
                    
        logger.info(f"Loaded a total of {len(documents)} document pages/sections.")
        return documents

    def _load_file(self, file_path: Path, ext: str) -> List[Document]:
        """Loads a single file and returns a list of Document objects."""
        if ext == ".pdf":
            return self._load_pdf(file_path)
        elif ext == ".docx":
            return self._load_docx(file_path)
        elif ext in {".html", ".htm"}:
            return self._load_html(file_path)
        elif ext in {".md", ".txt"}:
            return self._load_text(file_path)
        else:
            return []

    def _load_pdf(self, file_path: Path) -> List[Document]:
        """Loads a PDF file using PyPDFLoader to capture page numbers."""
        loader = PyPDFLoader(str(file_path))
        pages = loader.load()
        
        # Enrich metadata
        enriched_docs = []
        for i, page in enumerate(pages):
            doc = Document(
                page_content=page.page_content,
                metadata={
                    "source": file_path.name,
                    "full_path": str(file_path.resolve()),
                    "page": page.metadata.get("page", i) + 1,  # Ensure 1-indexed
                    "file_type": "PDF",
                    "title": file_path.stem.replace("_", " ").title()
                }
            )
            enriched_docs.append(doc)
        return enriched_docs

    def _load_docx(self, file_path: Path) -> List[Document]:
        """Loads a DOCX file and extracts raw text."""
        # Using docx2txt directly since it is fast and handles simple formatting well
        text = docx2txt.process(str(file_path))
        if not text.strip():
            return []
            
        doc = Document(
            page_content=text,
            metadata={
                "source": file_path.name,
                "full_path": str(file_path.resolve()),
                "page": 1,  # DOCX doesn't have native page numbers in raw text
                "file_type": "DOCX",
                "title": file_path.stem.replace("_", " ").title()
            }
        )
        return [doc]

    def _load_html(self, file_path: Path) -> List[Document]:
        """Loads an HTML file and extracts text using BeautifulSoup."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                html_content = f.read()
        except Exception as e:
            logger.warning(f"UTF-8 read failed for HTML {file_path}, retrying with system default encoding: {e}")
            with open(file_path, "r", errors="ignore") as f:
                html_content = f.read()

        soup = BeautifulSoup(html_content, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get clean text
        text = soup.get_text(separator="\n")
        
        # Break into lines and remove leading/trailing whitespace
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        clean_text = "\n".join(chunk for chunk in chunks if chunk)
        
        if not clean_text.strip():
            return []
            
        doc = Document(
            page_content=clean_text,
            metadata={
                "source": file_path.name,
                "full_path": str(file_path.resolve()),
                "page": 1,
                "file_type": "HTML",
                "title": file_path.stem.replace("_", " ").title()
            }
        )
        return [doc]

    def _load_text(self, file_path: Path) -> List[Document]:
        """Loads a Markdown or TXT file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            # Fallback to ignore errors if encoding is weird
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
        if not content.strip():
            return []
            
        doc = Document(
            page_content=content,
            metadata={
                "source": file_path.name,
                "full_path": str(file_path.resolve()),
                "page": 1,
                "file_type": "Markdown" if file_path.suffix.lower() == ".md" else "TXT",
                "title": file_path.stem.replace("_", " ").title()
            }
        )
        return [doc]
