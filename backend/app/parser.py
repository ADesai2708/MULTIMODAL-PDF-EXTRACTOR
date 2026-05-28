
import os
import glob
import fitz

from app.config import settings


def extract_text_from_pdf(pdf_path: str):

    """
    Extract clean text locally using PyMuPDF.
    """

    document = fitz.open(pdf_path)

    full_text = ""

    print("\n📄 Extracting document text...")

    for page_num in range(len(document)):

        page = document.load_page(page_num)

        text = page.get_text()

        full_text += text + "\n"

        print(
            f"✅ Extracted text from page {page_num + 1}"
        )

    return full_text


def extract_images_local(
    pdf_path,
    output_dir
):

    """
    Extract images locally using PyMuPDF.
    """

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    doc = fitz.open(pdf_path)

    saved_images = []

    print(
        "\n🖼️ Extracting images locally..."
    )

    for page_num in range(len(doc)):

        page = doc[page_num]

        images = page.get_images(
            full=True
        )

        print(
            f"📄 Page {page_num + 1}: "
            f"{len(images)} image(s)"
        )

        for idx, img in enumerate(images):

            try:

                xref = img[0]

                base_image = doc.extract_image(
                    xref
                )

                image_bytes = base_image["image"]

                image_ext = base_image["ext"]

                filename = (
                    f"page_{page_num + 1}_img_{idx + 1}.{image_ext}"
                )

                image_path = os.path.join(
                    output_dir,
                    filename
                )

                with open(
                    image_path,
                    "wb"
                ) as f:

                    f.write(image_bytes)

                saved_images.append({

                    "image_name": filename,

                    "image_path": image_path
                })

                print(
                    f"✅ Saved: {filename}"
                )

            except Exception as e:

                print(
                    f"❌ Failed extracting image: {e}"
                )

    return saved_images


def parse_pdf_document(
    pdf_path: str
):

    """
    Fully local PDF parser:
    - Text extraction
    - Image extraction
    """

    if not os.path.exists(pdf_path):

        raise FileNotFoundError(

            f"PDF not found: {pdf_path}"
        )

    print("\n================================================")

    print(
        f"🚀 Ingesting: "
        f"{os.path.basename(pdf_path)}"
    )

    print("================================================")

    images_output_dir = settings.OUTPUT_DIR

    os.makedirs(
        images_output_dir,
        exist_ok=True
    )

    # -----------------------------
    # TEXT EXTRACTION
    # -----------------------------

    full_text = extract_text_from_pdf(
        pdf_path
    )

    # -----------------------------
    # IMAGE EXTRACTION
    # -----------------------------

    extracted_images = extract_images_local(

        pdf_path,

        images_output_dir
    )

    print("\n================================================")

    print("✅ INGESTION COMPLETE")

    print("================================================")

    print(
        f"📄 Text Length: "
        f"{len(full_text)} characters"
    )

    print(
        f"🖼️ Extracted Images: "
        f"{len(extracted_images)}"
    )

    print(
        f"📂 Output Folder: "
        f"{images_output_dir}"
    )

    return {

        "markdown_text": full_text,

        "raw_chunks": [],

        "extracted_images": extracted_images
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
            f"\n⚠️ No PDFs found in: "
            f"{settings.INPUT_DIR}"
        )

    else:

        sample_target = pdf_files[0]

        try:

            results = parse_pdf_document(

                sample_target
            )

            print("\n📘 TEXT PREVIEW:\n")

            print("-" * 60)

            print(

                results[
                    "markdown_text"
                ][:1500]

            )

            print("\n...[truncated]...")

            print("-" * 60)

        except Exception as e:

            print(
                f"\n❌ Parsing failed: {e}"
            )

