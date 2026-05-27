from app.vector_store import init_vector_index
import google.generativeai as genai
from app.config import settings

genai.configure(
    api_key=settings.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-1.5-flash-8b"
)

def execute_multimodal_query(query_str: str):
    """
    Search Qdrant, retrieve context,
    then send retrieved text to Gemini manually.
    """

    print(f"\n🔍 Searching: {query_str}")

    index = init_vector_index()

    retriever = index.as_retriever(
        similarity_top_k=3
    )

    source_nodes = retriever.retrieve(
        query_str
    )

    supporting_images=[]

    retrieved_context=[]

    for node in source_nodes:

        metadata=node.node.metadata

        retrieved_context.append(
            node.node.text
        )

        if metadata.get(
            "type"
        )=="figure_diagram_description":

            supporting_images.append(
                {
                    "name":
                    metadata.get(
                        "image_name"
                    ),

                    "path":
                    metadata.get(
                        "image_local_path"
                    )
                }
            )

    context="\n".join(
        retrieved_context
    )

    prompt=f"""
    Use only the context below
    to answer the question.

    Context:
    {context}

    Question:
    {query_str}
    """

    response=model.generate_content(
        prompt
    )

    return {

        "answer":
        response.text,

        "referenced_images":
        supporting_images
    }


if __name__=="__main__":

    print("🤖 RAG ONLINE")

    while True:

        q=input(
            "Question: "
        )

        if q=="exit":
            break

        result=execute_multimodal_query(q)

        print(
            "\nANSWER:"
        )

        print(
            result["answer"]
        )