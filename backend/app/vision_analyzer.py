from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration
)

from PIL import Image

import torch


print("🔄 Loading local BLIP vision model...")

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
).to(device)

print(
    f"✅ BLIP model loaded successfully on hardware target: {device.upper()}!"
)


def generate_image_description(
    image_path: str
):

    try:

        image = Image.open(
            image_path
        ).convert("RGB")

        inputs = processor(
            image,
            return_tensors="pt"
        ).to(device)

        output = model.generate(
            **inputs,
            max_new_tokens=50
        )

        caption = processor.decode(
            output[0],
            skip_special_tokens=True
        )

        return caption

    except Exception as e:

        return f"Error generating description: {e}"