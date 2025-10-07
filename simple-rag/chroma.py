from langchain_chroma import Chroma
from uuid import uuid4
from langchain_core.documents.base import Document

from openai_service import get_openai_embeddings
from settings import settings

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_chroma_store():
    logger.info("Initializing Chroma vector store...")
    return Chroma(
        collection_name=settings.CHROMA_COLLECTION_NAME,
        embedding_function=get_openai_embeddings(),
        persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
    )


async def store_documents(vector_store: Chroma, documents: list[Document]):
    logger.info(f"Storing {len(documents)} documents in the vector store...")
    uuids = [str(uuid4()) for _ in range(len(documents))]
    await vector_store.aadd_documents(documents=documents, ids=uuids)


def get_retriever(
        vector_store: Chroma,
        k: int = 5,
        score_threshold: float = 0.45
):
    logger.info("Creating retriever with MMR search...")
    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": k,
            "score_threshold": score_threshold,
        }
    )


async def retrieve_similar_documents(
        vector_store: Chroma,
        query: str,
        k: int = 5,
        score_threshold: float = 0.45
) -> list[Document]:
    logger.info(f"Retrieving documents similar to the query: {query}")
    retriever = get_retriever(vector_store, k, score_threshold)
    return await retriever.ainvoke(query)
