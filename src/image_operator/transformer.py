import argparse
from pathlib import Path
from PIL import Image
from tqdm import tqdm

IMAGE_EXTENSIONS = frozenset(
    {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"}
)

MAX_DIMENSION = 1080


def resize_images(source_dir: str, max_dim: int = MAX_DIMENSION) -> None:
    source_path = Path(source_dir)

    if not source_path.is_dir():
        raise ValueError(
            f"Source directory '{source_dir}' does not exist or is not a directory."
        )

    files_to_process = [
        f
        for f in source_path.rglob("*")
        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
    ]

    canvas_size = (max_dim, max_dim)
    background_color = (0x80, 0x80, 0x80)

    for file_path in tqdm(files_to_process, desc="Resizing images", unit="file"):
        try:
            with Image.open(file_path) as img:
                img = img.convert("RGB")
                width, height = img.size
                largest = max(width, height)

                scale = max_dim / largest
                new_size = (int(width * scale), int(height * scale))
                resized = img.resize(new_size, Image.LANCZOS)

                canvas = Image.new("RGB", canvas_size, background_color)
                offset = (
                    (max_dim - resized.width) // 2,
                    (max_dim - resized.height) // 2,
                )
                canvas.paste(resized, offset)
                canvas.save(file_path)

        except Exception as ex:
            print(f"Skipping {file_path}: {ex}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Resize images so the largest dimension is at most 1080px"
    )
    parser.add_argument("source_dir", help="Root folder to search for images")
    parser.add_argument(
        "--max-dim",
        type=int,
        default=MAX_DIMENSION,
        help=f"Maximum dimension in pixels (default: {MAX_DIMENSION})",
    )
    args = parser.parse_args()

    try:
        resize_images(args.source_dir, max_dim=args.max_dim)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)
