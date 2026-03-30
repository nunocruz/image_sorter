import os
import shutil
import argparse
from PIL import Image

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp")


def sort_images(source_dir):
    # Output folders
    horizontal_dir = os.path.join(source_dir, "horizontal")
    vertical_dir = os.path.join(source_dir, "vertical")
    square_dir = os.path.join(source_dir, "square")

    # create folders if they don't exist
    os.makedirs(horizontal_dir, exist_ok=True)
    os.makedirs(vertical_dir, exist_ok=True)
    os.makedirs(square_dir, exist_ok=True)

    for filename in os.listdir(source_dir):
        if not filename.lower().endswith(IMAGE_EXTENSIONS):
            continue

        file_path = os.path.join(source_dir, filename)

        try:
            with Image.open(file_path) as img:
                width, height = img.size

            if width > height:
                dest = horizontal_dir
            elif height > width:
                dest = vertical_dir
            else:
                dest = square_dir

            shutil.move(file_path, os.path.join(dest, filename))

        except Exception as e:
            print(f"Skipping {filename}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sort images by orientation")
    parser.add_argument("source_dir", help="Path to the folder containing images")
    args = parser.parse_args()

    sort_images(args.source_dir)
