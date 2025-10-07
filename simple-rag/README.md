# simple-rag

A minimal implementation of Retrieval-Augmented Generation (RAG) in Python.

## Features

- Document retrieval using Chroma vector database (in-memory)
- Uses OpenAI embeddings for document indexing
- Integrates OpenAI models for answer generation
- Simple and extensible codebase

## Installation

```bash
git clone <repo>
cd simple-rag
pip install -r requirements.txt

vi .env # add your openai api key

python rag.py
```

## Example

```bash
python rag.py

INFO:__main__:Loaded 132 pages from principles_2nd_edition_updated.pdf...
----------------------------------------------------------------------------------------------------

INFO:chroma:Initializing Chroma vector store...
INFO:root:Creating text-embedding-3-small...
INFO:chromadb.telemetry.product.posthog:Anonymized telemetry enabled. See                     https://docs.trychroma.com/telemetry for more information.
INFO:chroma:Storing 132 documents in the vector store...
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
----------------------------------------------------------------------------------------------------

Enter your query: Can you get me a brief summary please?
INFO:chroma:Retrieving documents similar to the query: Can you get me a brief summary please?
INFO:chroma:Creating retriever with MMR search...
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
----------------------------------------------------------------------------------------------------

INFO:__main__:Organized retrieval results...
----------------------------------------------------------------------------------------------------

INFO:root:Generating answer with gpt-4o-mini...
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/responses "HTTP/1.1 200 OK"
----------------------------------------------------------------------------------------------------


Answer:

The text discusses key concepts in building AI agents, particularly focusing on memory systems and tracing for debugging. It highlights hierarchical memory, which combines recent interactions with long-term memories to formulate responses, showcasing how this works in a practical example. The text also touches on tracing, a method for monitoring functions in applications to visualize input and output, emphasizing the importance of standardization through OpenTelemetry. The author, Sam Bhagwat, emphasizes the relevance of these principles for developing effective AI applications, particularly in the context of the rapid advancements in large language models.
```

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

