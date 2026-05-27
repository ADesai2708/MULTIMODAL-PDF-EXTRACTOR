import os
import base64
from openai import OpenAI
from app.config import settings

def encode_image_to_base64(image_path: str) -> str:
    """
    Converts a local image file into a base64 encoded string 
    so it can be securely transmitted to the Vision API.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def analyze_extracted_image(image_path: str) -> str:
    """
    Passes a schematic, chart, or diagram to GPT-4o and extracts
    a highly thorough technical description for vector indexing.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Target figure asset not found at: {image_path}")
        
    print(f"👁️  Analyzing structural image: {os.path.basename(image_path)}")
    
    # Initialize OpenAI client using our validated settings
    client = OpenAI(api_key=settings.GEMINI_API_KEY)
    
    # Format the image asset
    base64_image = encode_image_to_base64(image_path)
    
    # Craft a strict prompt focusing on technical, mathematical, and data accuracy
    prompt = (
        "You are an expert technical document analyst. Analyze this image extracted from a patent "
        "or research paper. Provide a detailed, highly descriptive summary. Focus on explaining:\n"
        "1. The type of visual element (e.g., block diagram, architectural flowchart, data plot graph, chemical structure).\n"
        "2. All visible annotations, labels, numbers, axis markings, or callout values.\n"
        "3. The core mechanism, technical trend, or relationship being communicated.\n"
        "Be extremely explicit and descriptive, as this summary will be used directly for keyword and vector search."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=700,
            temperature=0.2 # Lower temperature keeps descriptions highly factual
        )
        
        description = response.choices[0].message.content
        return description
        
    except Exception as e:
        print(f"❌ Vision Engine API error on {os.path.basename(image_path)}: {e}")
        return f"[Error generating description for image asset: {os.path.basename(image_path)}]"

if __name__ == "__main__":
    # Standalone validation loop
    import glob
    print("Testing Vision Analysis Routing...")
    
    # Pull any images generated during Step 2
    target_images = glob.glob(os.path.join(settings.OUTPUT_DIR, "*"))
    
    if not target_images:
        print(f"\n⚠️  No extracted images found inside storage area: '{settings.OUTPUT_DIR}'")
        print("👉 Run step 2 first (`parser.py`) with a document that contains figures to test this component!")
    else:
        sample_img = target_images[0]
        print(f"\nFound asset to test: {sample_img}")
        analysis_result = analyze_extracted_image(sample_img)
        
        print("\n" + "="*40 + " VISION ANALYSIS OUTPUT " + "="*40)
        print(analysis_result)
        print("="*104)