from pathlib import Path
from chroma import (
    get_chroma_store,
    store_documents,
    retrieve_similar_documents
)

from openai_service import get_answer_from_openai
from langchain_core.documents.base import Document
import fitz
import pymupdf

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_pdf(file_path: Path) -> list[Document]:
    """Load a PDF file and return its content as a list of Document objects."""
    documents = []

    filename = file_path.name
    with fitz.open(file_path) as pdf:
        total_pages = len(pdf)

        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            text = page.get_text()

            if not text.strip():
                continue

            metadata = {
                "source": filename,
                "page_number": page_num + 1,
                "total_pages": total_pages
            }

            documents.append(Document(page_content=text, metadata=metadata))
    logger.info(f"Loaded {len(documents)} pages from {filename}...")
    return documents


def organize_retrieval_results(results: list[Document]) -> dict:
    organized_results = set()
    for doc in results:
        page_content = doc.page_content
        page_content = page_content.replace("\n", " ").strip()
        page_number = doc.metadata.get("page_number", "N/A")
        total_pages = doc.metadata.get("total_pages", "N/A")
        page_content = f"Page {page_number} of {total_pages}\n\n{page_content}"

        if page_content not in organized_results:
            organized_results.add(page_content)

    retrieved_information = "The relevant information for the given query:\n\n"
    organized_results = "\n\n".join(organized_results)
    retrieved_information += organized_results.lstrip().strip()

    logger.info("Organized retrieval results...")
    return retrieved_information


if __name__ == "__main__":
    filepath = Path(input("Enter the path to the PDF file: ").strip())

    try:
        docs = load_pdf(filepath)
    except pymupdf.FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        exit(1)
    print(f"{'--' * 50}\n")

    vector_store = get_chroma_store()

    import asyncio
    asyncio.run(store_documents(vector_store, docs))
    print(f"{'--' * 50}\n")

    query = input("Enter your query: ")
    results = asyncio.run(retrieve_similar_documents(vector_store, query))
    print(f"{'--' * 50}\n")

    organized_results = organize_retrieval_results(results)
    print(f"{'--' * 50}\n")

    answer = get_answer_from_openai(query, organized_results)
    print(f"{'--' * 50}\n")
    print("\nAnswer:\n")
    print(answer)
