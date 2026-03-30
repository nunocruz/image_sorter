import os
import shutil
import argparse
from PIL import Image

# Argument parser
parser = argparse.ArgumentParser(description="Sort images by orientation")
parser.add_argument("source_dir", help="Path to the folder containing images")
args = parser.parse_args()

SOURCE_DIR = args.source_dir

# 📁 Output folders
HORIZONTAL_DIR = os.path.join(SOURCE_DIR, "horizontal")
VERTICAL_DIR = os.path.join(SOURCE_DIR, "vertical")
SQUARE_DIR = os.path.join(SOURCE_DIR, "square")

# Create folders if they don't exist
os.makedirs(HORIZONTAL_DIR, exist_ok=True)
os.makedirs(VERTICAL_DIR, exist_ok=True)
os.makedirs(SQUARE_DIR, exist_ok=True)

# Supported image extensions
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp")

for filename in os.listdir(SOURCE_DIR):
    if not filename.lower().endswith(IMAGE_EXTENSIONS):
        continue

    file_path = os.path.join(SOURCE_DIR, filename)

    try:
        with Image.open(file_path) as img:
            width, height = img.size

        if width > height:
            dest = HORIZONTAL_DIR
        elif height > width:
            dest = VERTICAL_DIR
        else:
            dest = SQUARE_DIR

        shutil.move(file_path, os.path.join(dest, filename))
        print(f"Moved {filename} → {dest}")

    except Exception as e:
        print(f"Skipping {filename}: {e}")