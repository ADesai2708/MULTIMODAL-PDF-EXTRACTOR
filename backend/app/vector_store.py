import os
import qdrant_client

from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    Document,
    Settings
)

from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


def init_vector_index(
    collection_name: str = "multimodal_documents"
) -> VectorStoreIndex:
    """
    Initializes a local disk-persisted Qdrant vector store
    using FREE local HuggingFace embeddings.
    """

    # FREE local embeddings (no OpenAI key needed)
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    # Create local Qdrant storage directory
    db_path = os.path.join(
        os.path.dirname(__file__),
        "../data/qdrant_local"
    )

    os.makedirs(db_path, exist_ok=True)

    # Start local Qdrant
    client = qdrant_client.QdrantClient(
        path=db_path
    )

    # Adapter for LlamaIndex
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name
    )

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    try:
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            storage_context=storage_context
        )

        print("✅ Existing vector index loaded")

    except Exception:

        print("⚡ Creating new vector index")

        index = VectorStoreIndex(
            [],
            storage_context=storage_context
        )

    return index


def index_multimodal_payload(
    pipeline_payload: dict
):
    """
    Converts multimodal pipeline payloads
    into searchable vector documents.
    """

    index = init_vector_index()

    source_doc_name = pipeline_payload[
        "source_document"
    ]

    documents_to_insert = []

    print(
        f"\n📥 Processing: {source_doc_name}"
    )

    # Main text content
    text_doc = Document(
        text=pipeline_payload[
            "document_text_content"
        ],
        metadata={
            "source": source_doc_name,
            "type": "layout_text_and_tables"
        }
    )

    documents_to_insert.append(
        text_doc
    )

    # Figure descriptions
    visual_elements = pipeline_payload.get(
        "visual_elements",
        []
    )

    if visual_elements:

        print(
            f"📷 Found {len(visual_elements)} visual items"
        )

        for element in visual_elements:

            vision_doc = Document(
                text=element[
                    "description"
                ],

                metadata={
                    "source": source_doc_name,
                    "type": "figure_diagram_description",
                    "image_name":
                        element[
                            "image_name"
                        ],
                    "image_local_path":
                        element[
                            "image_path"
                        ]
                }
            )

            documents_to_insert.append(
                vision_doc
            )

    print(
        f"📤 Uploading {len(documents_to_insert)} chunks..."
    )

    for doc in documents_to_insert:
        index.insert(doc)

    print(
        f"✅ Successfully indexed: {source_doc_name}"
    )

    return index


if __name__ == "__main__":

    print(
        "Testing vector store..."
    )

    try:

        idx = init_vector_index()

        print(
            "✅ Qdrant connected successfully"
        )

    except Exception as e:

        print(
            f"❌ Error: {e}"
        )