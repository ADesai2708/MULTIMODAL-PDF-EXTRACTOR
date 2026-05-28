import os
import glob
import qdrant_client
from app.config import settings
from app.parser import parse_pdf_document
from app.vision_analyzer import generate_image_description
def run_multimodal_ingestion_pipeline(pdf_path: str):
    """
    Orchestrates the entire ingestion workflow:
    1. Parses PDF into markdown and extracts raw image assets.
    2. Identifies all extracted images from the document.
    3. Uses Vision LLM to generate descriptive text for those images.
    4. Compiles text and visual descriptions into a final indexing payload.
    """
    print("=" * 60)
    print(f"🎬 STARTING MULTIMODAL PIPELINE FOR: {os.path.basename(pdf_path)}")
    print("=" * 60)
    
    # Step 1: Run LlamaParse to extract markdown text and download embedded figures
    parsing_results = parse_pdf_document(pdf_path)
    
    markdown_text = parsing_results["markdown_text"]
    extracted_images = parsing_results["extracted_images"]
    
    # Step 2: Loop through every extracted image and generate BLIP captions
    visual_elements = []
    
    if extracted_images:
        print(f"\n🔄 Found {len(extracted_images)} extracted visual assets. Commencing BLIP captioning...")
        for img_info in extracted_images:
            # LlamaParse returns image paths or metadata structures depending on version
            image_path = (
                os.path.abspath(img_info.get("image_path"))
                if isinstance(img_info, dict)
                else os.path.abspath(img_info)
            )

            image_name = (
                img_info.get("image_name")
                if isinstance(img_info, dict)
                else os.path.basename(image_path)
            )

            if image_path and os.path.exists(image_path):
                print(f"👁️ Analyzing image: {image_name}")
                try:
                    description = generate_image_description(image_path)
                    print("✅ Caption generated")

                    visual_elements.append({
                        "image_name": image_name,
                        "image_path": image_path,
                        "description": description
                    })
                except Exception as e:
                    print(f"⚠️ Failed to generate caption for {image_name}: {e}")
                    visual_elements.append({
                        "image_name": image_name,
                        "image_path": image_path,
                        "description": f"[Error generating caption: {e}]"
                    })
            else:
                print(f"⚠️ Could not resolve valid path for image asset: {img_info}")
    else:
        print("\nℹ️ No visual assets or diagrams detected in this specific document layout.")

    # Step 3: Combine structural layout text with BLIP descriptions into a unified payload
    print("\nFusing text elements and visual descriptions...")
    
    final_payload = {
        "source_document": os.path.basename(pdf_path),
        "document_text_content": markdown_text,
        "visual_elements": visual_elements
    }
    
    print("\n" + "=" * 60)
    print("🏁 PIPELINE PROCESSING COMPLETE!")
    print(f"   • Compiled Document Text: {len(markdown_text)} characters.")
    print(f"   • Contextualized Images: {len(visual_elements)} elements described.")
    print("=" * 60)
    
    return final_payload

if __name__ == "__main__":
    from app.vector_store import index_multimodal_payload
    
    pdf_files = glob.glob(os.path.join(settings.INPUT_DIR, "*.pdf"))
    
    if not pdf_files:
        print(f"\n⚠️ Place a sample PDF in '{settings.INPUT_DIR}' to run the full pipeline.")
    else:
        sample_pdf = pdf_files[0]
        try:
            # 1. Parse and analyze document structure
            processed_data = run_multimodal_ingestion_pipeline(sample_pdf)
            
            # 2. Commit the parsed structure directly to Qdrant Index
            index_multimodal_payload(processed_data)
            
        except Exception as e:
            print(f"\n❌ Pipeline failed during execution: {e}")