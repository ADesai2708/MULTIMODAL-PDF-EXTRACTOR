import os
import glob
import json
import fitz

from llama_parse import LlamaParse
from app.config import settings


def init_parser() -> LlamaParse:
    """
    Initialize LlamaParse with multimodal support.
    """

    return LlamaParse(

        api_key=settings.LLAMA_CLOUD_API_KEY,

        result_type="markdown",

        extract_charts=True,

        verbose=True
    )


def extract_images_local(
    pdf_path,
    output_dir
):
    """
    Fallback local image extraction using PyMuPDF.
    """

    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)

    saved_images = []

    print("\n🖼️ Running fallback image extraction...")

    for page_num in range(len(doc)):

        page = doc[page_num]

        images = page.get_images(full=True)

        print(
            f"📄 Page {page_num+1}: "
            f"{len(images)} image(s)"
        )

        for idx, img in enumerate(images):

            xref = img[0]

            base_image = doc.extract_image(xref)

            image_bytes = base_image["image"]

            image_ext = base_image["ext"]

            filename = (
                f"page_{page_num+1}_img_{idx+1}.{image_ext}"
            )

            image_path = os.path.join(
                output_dir,
                filename
            )

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            saved_images.append({

                "image_name": filename,

                "image_path": image_path
            })

            print(
                f"✅ Saved: {filename}"
            )

    return saved_images


def parse_pdf_document(pdf_path: str):

    """
    Parse PDF into markdown + extracted images.
    """

    if not os.path.exists(pdf_path):

        raise FileNotFoundError(
            f"Target PDF file not found at: {pdf_path}"
        )

    print(
        f"\n🚀 Ingesting: "
        f"{os.path.basename(pdf_path)}"
    )

    parser = init_parser()

    images_output_dir = settings.OUTPUT_DIR

    os.makedirs(
        images_output_dir,
        exist_ok=True
    )

    print(
        "\n⏳ Parsing layout + visuals..."
    )

    json_results = parser.get_json_result(
        pdf_path
    )

    print(
        "\n⏳ Rendering markdown..."
    )

    markdown_results = parser.load_data(
        pdf_path
    )

    full_markdown_text = "\n\n".join(
        [
            doc.text
            for doc in markdown_results
        ]
    )

    # Save raw debug JSON
    try:

        with open(
            "debug_llamaparse.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                json_results,
                f,
                indent=2
            )

        print(
            "\n✅ Saved debug JSON"
        )

    except Exception as e:

        print(
            f"\n⚠️ Failed saving debug JSON: {e}"
        )

    # Try LlamaParse image extraction
    try:

        print(
            "\n🖼️ Extracting images via LlamaParse..."
        )

        images_downloaded = parser.get_images(

            json_results,

            download_path=images_output_dir
        )

        print(
            f"✅ LlamaParse extracted "
            f"{len(images_downloaded)} image(s)"
        )

    except Exception as e:

        print(
            f"\n❌ LlamaParse image extraction failed: {e}"
        )

        images_downloaded = []

    # Fallback extraction
    if not images_downloaded:

        print(
            "\n⚠️ No images detected via LlamaParse"
        )

        print(
            "🔄 Switching to PyMuPDF fallback..."
        )

        images_downloaded = extract_images_local(

            pdf_path,

            images_output_dir
        )

    print("\n================================================")

    print("✅ INGESTION COMPLETE")

    print("================================================")

    print(
        f"📄 Parsed sections: "
        f"{len(markdown_results)}"
    )

    print(
        f"🖼️ Extracted images: "
        f"{len(images_downloaded)}"
    )

    print(
        f"📂 Output directory: "
        f"{images_output_dir}"
    )

    return {

        "markdown_text":
        full_markdown_text,

        "raw_chunks":
        markdown_results,

        "extracted_images":
        images_downloaded
    }


if __name__ == "__main__":

    print(
        "\n🔍 Testing parser..."
    )

    pdf_files = glob.glob(

        os.path.join(
            settings.INPUT_DIR,
            "*.pdf"
        )
    )

    if not pdf_files:

        print(
            f"\n⚠️ No PDFs found inside "
            f"'{settings.INPUT_DIR}'"
        )

    else:

        sample_target = pdf_files[0]

        try:

            results = parse_pdf_document(
                sample_target
            )

            print(
                "\n📘 Markdown Preview:\n"
            )

            print("-" * 60)

            print(
                results[
                    "markdown_text"
                ][:1000]
            )

            print("\n...[truncated]...")

            print("-" * 60)

        except Exception as e:

            print(
                f"\n❌ Parsing failed: {e}"
            )