import glob
import os
from PIL import Image

from app.config import settings


def analyze_extracted_image(image_path: str) -> str:
    """
    Stub image analysis function. Gemini Vision support has been removed.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Target figure asset not found at: {image_path}")

    print(f"👁️  Vision analysis is currently disabled for: {os.path.basename(image_path)}")
    return f"[Vision analysis disabled for: {os.path.basename(image_path)}]"

if __name__ == "__main__":
    # Standalone validation loop
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