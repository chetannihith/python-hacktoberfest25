from langchain_openai import OpenAIEmbeddings
from settings import settings
from openai import OpenAI

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI()


def get_openai_embeddings():
    logging.info(f"Creating {settings.EMBEDDING_MODEL}...")
    return OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL, api_key=settings.OPENAI_API_KEY
    )


def get_answer_from_openai(
        query: str,
        information: str,
        temperature: float = 0.5
) -> str:
    logging.info(f"Generating answer with {settings.COMPLETION_MODEL}...")

    user_content = [
        {
            "type": "input_text",
            "text": "Use the given relevant information, and answer the query",
        }
    ]
    user_content.append({"type": "input_text", "text": f"\nQuery: {query}"})
    user_content.append(
        {
            "type": "input_text",
            "text": f"\nRelevant Information: : {information}",
        }
    )

    messages = [{"role": "user", "content": user_content}]

    response = client.responses.create(
        model=settings.COMPLETION_MODEL,
        input=messages,
        temperature=temperature
    )

    return response.output[0].content[0].text
