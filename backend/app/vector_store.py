# import os
# import qdrant_client

# from llama_index.core import (
#     VectorStoreIndex,
#     StorageContext,
#     Document,
#     Settings
# )

# from llama_index.vector_stores.qdrant import QdrantVectorStore
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from sentence_transformers import SentenceTransformer

from app.config import settings


# Local embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def init_qdrant():

    db_path = os.path.join(
        os.path.dirname(__file__),
        "../data/qdrant_local"
    )

    os.makedirs(
        db_path,
        exist_ok=True
    )

    client = QdrantClient(
        path=db_path
    )

    collection_name = (
        "multimodal_documents"
    )

    existing = [

        collection.name

        for collection in
        client.get_collections().collections
    ]

    if collection_name not in existing:

        client.recreate_collection(

            collection_name=
            collection_name,

            vectors_config={
                "text": VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            }
        )

        print(
            "✅ Created Qdrant collection"
        )

    else:

        print(
            "✅ Existing vector "
            "index loaded"
        )

    return client, collection_name




def embed_text(text):

    return embedding_model.encode(
        text
    ).tolist()


def index_multimodal_payload(
    pipeline_payload
):

    client, collection_name = init_qdrant()

    source_doc_name = pipeline_payload[
        "source_document"
    ]

    documents = []

    # Main document text
    documents.append({

        "text":
        pipeline_payload[
            "document_text_content"
        ],

        "metadata": {

            "source":
            source_doc_name,

            "type":
            "layout_text_and_tables"
        }
    })

    # Visual elements
    visual_elements = pipeline_payload.get(
        "visual_elements",
        []
    )

    for element in visual_elements:

        documents.append({

            "text":
            element["description"],

            "metadata": {

                "source":
                source_doc_name,

                "type":
                "figure_diagram_description",

                "image_name":
                element["image_name"],

                "image_local_path":
                element["image_path"]
            }
        })

    print(
        f"\n📥 Processing: "
        f"{source_doc_name}"
    )

    print(
        f"📷 Found "
        f"{len(visual_elements)} "
        f"visual items"
    )

    points = []

    for doc in documents:

        vector = embed_text(
            doc["text"]
        )

        points.append(

            PointStruct(

                id=str(uuid.uuid4()),

                vector={
                    "text":vector
                },

                payload={

                    "text":
                    doc["text"],

                    **doc["metadata"]
                }
            )
        )

    print(
        f"📤 Uploading "
        f"{len(points)} chunks..."
    )

    client.upsert(

        collection_name=collection_name,

        points=points
    )

    print(
        f"✅ Successfully indexed: "
        f"{source_doc_name}"
    )


if __name__ == "__main__":

    print(
        "Testing vector DB..."
    )

    init_qdrant()
