"""Prepare a portrait for ASCII conversion. Usage: python scripts/prep_photo.py source-photo.jpg"""
import argparse
from io import BytesIO
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageOps
from rembg import remove

def main():
    parser = argparse.ArgumentParser(description="Remove photo background and enhance local contrast")
    parser.add_argument("image", type=Path)
    parser.add_argument("--output", type=Path, default=Path("source-prepped.png"))
    args = parser.parse_args()
    if not args.image.is_file():
        parser.error(f"Image not found: {args.image}")
    raw = args.image.read_bytes()
    cutout = Image.open(BytesIO(remove(raw))).convert("RGBA")
    white = Image.new("RGBA", cutout.size, (255,255,255,255))
    composite = Image.alpha_composite(white, cutout).convert("RGB")
    gray = cv2.cvtColor(np.asarray(composite), cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    # Keep background white after local-contrast enhancement.
    alpha = np.asarray(cutout.getchannel("A"))
    enhanced[alpha < 12] = 255
    result = Image.fromarray(enhanced, mode="L")
    result = ImageOps.autocontrast(result, cutoff=1)
    arr = np.array(result)
    arr[alpha < 12] = 255
    Image.fromarray(arr, mode="L").save(args.output)
    print(f"Saved prepared image to {args.output}")

if __name__ == "__main__":
    main()
