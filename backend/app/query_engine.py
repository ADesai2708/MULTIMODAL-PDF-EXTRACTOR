
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

from app.config import settings
import os


embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def execute_multimodal_query(
    query_str: str
):

    print(f"\n🔍 Searching: {query_str}")

    db_path = os.path.join(
        os.path.dirname(__file__),
        "../data/qdrant_local"
    )

    client = QdrantClient(
        path=db_path
    )

    collection_name = (
        "multimodal_documents"
    )

    query_vector = embedding_model.encode(
        query_str
    ).tolist()

    results = client.search(

        collection_name=collection_name,

        query_vector=(
            "text",
            query_vector
        ),

        limit=3
    )

    context_blocks = []

    referenced_images = []

    for result in results:

        payload = result.payload

        context_blocks.append(

            payload.get(
                "text",
                ""
            )
        )

        if payload.get(
            "type"
        ) == "figure_diagram_description":

            referenced_images.append({

                "name":
                payload.get(
                    "image_name"
                ),

                "path":
                payload.get(
                    "image_local_path"
                )
            })

    final_answer = (
    "This document appears to discuss:\n\n"
    + "\n".join(context_blocks[:3])
)

    prompt = f"""
You are a helpful research assistant.

Answer the user's question using ONLY the context below.

QUESTION:
{query_str}

CONTEXT:
{final_answer}
"""

    # Gemini Vision / generative AI call removed.
    # Return the concatenated context directly as the answer.
    return {

        "answer":
        final_answer,

        "referenced_images":
        referenced_images
    }

