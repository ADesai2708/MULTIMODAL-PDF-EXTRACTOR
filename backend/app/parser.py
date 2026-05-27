import os
import glob
from llama_parse import LlamaParse
from app.config import settings

def init_parser() -> LlamaParse:
    """
    Initializes LlamaParse with multi-modal capabilities enabled.
    This tells the cloud parser to extract both text layout and images.
    """
    return LlamaParse(
        api_key=settings.LLAMA_CLOUD_API_KEY,
        result_type="markdown",  # Preserves tables as markdown tables
        extract_charts=True,     # Specifically look for complex technical charts
        verbose=True
    )

def parse_pdf_document(pdf_path: str):
    """
    Parses a single target PDF, extracting clean markdown text and images.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Target PDF file not found at: {pdf_path}")
        
    print(f"\n🚀 Ingesting: {os.path.basename(pdf_path)}")
    parser = init_parser()
    
    # 1. Run the layout-aware parser over the document
    # LlamaParse handles image extraction asynchronously under the hood
    images_output_dir = settings.OUTPUT_DIR
    os.makedirs(images_output_dir, exist_ok=True)
    
    # get_json gets comprehensive layout dictionary maps containing image bytes
    print("⏳ Parsing layout structure and extracting images via LlamaParse...")
    json_results = parser.get_json_result(pdf_path)
    
    # Extract the markdown string text data
    print("⏳ Rendering layout markdown chunks...")
    markdown_results = parser.load_data(pdf_path)
    full_markdown_text = "\n\n".join([doc.text for doc in markdown_results])
    
    # 2. Download and write out the extracted images to our staging directory
    # LlamaParse embeds visual assets into the JSON results dictionary metadata
    images_downloaded = parser.get_images(json_results, download_path=images_output_dir)
    
    print("✅ Ingestion Complete!")
    print(f"   • Extracted Chunks: {len(markdown_results)} pages/sections parsed.")
    print(f"   • Extracted Figures/Images: {len(images_downloaded)} files written to '{images_output_dir}'")
    
    return {
        "markdown_text": full_markdown_text,
        "raw_chunks": markdown_results,
        "extracted_images": images_downloaded
    }

if __name__ == "__main__":
    # Test script standalone verification loop
    print("Testing parser routing...")
    pdf_files = glob.glob(os.path.join(settings.INPUT_DIR, "*.pdf"))
    
    if not pdf_files:
        print(f"\n⚠️  No PDFs found inside '{settings.INPUT_DIR}'.")
        print("👉 Drop a sample patent or research paper PDF into that folder to test the extraction script!")
    else:
        # Run a test extraction on the first PDF it matches
        sample_target = pdf_files[0]
        try:
            results = parse_pdf_document(sample_target)
            print("\nSnippet of extracted Markdown content looks like this:")
            print("-" * 50)
            print(results["markdown_text"][:600] + "\n... [truncated] ...")
            print("-" * 50)
        except Exception as e:
            print(f"\n❌ Error encountered during document extraction: {e}")