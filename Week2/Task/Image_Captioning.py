import torch
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration\

MODEL_NAME = "Salesforce/blip-image-captioning-base"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

processor = AutoProcessor.from_pretrained(MODEL_NAME)

model = BlipForConditionalGeneration.from_pretrained( MODEL_NAME).to(device)
model.eval()

def generate_caption(image):
    image = image.convert("RGB")

    inputs = processor(images=image, return_tensors="pt")
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=30)

    return processor.decode(output[0], skip_special_tokens=True)
