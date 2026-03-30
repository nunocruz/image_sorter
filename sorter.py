import shutil
import argparse
from pathlib import Path
from PIL import Image
from tqdm import tqdm

IMAGE_EXTENSIONS = frozenset(
    {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"}
)


def sort_images(source_dir: str, copy_mode: bool = False) -> None:
    # Convert to Path object for cleaner operations
    source_path: Path = Path(source_dir)

    # Check if source_dir exists and is a readable directory
    if not source_path.is_dir():
        raise ValueError(
            f"Source directory '{source_dir}' does not exist or is not a directory."
        )

    # Verify directory is readable by attempting to list contents
    try:
        next(source_path.iterdir())
    except PermissionError:
        raise ValueError(f"Source directory '{source_dir}' is not readable.")
    except StopIteration:
        pass  # Empty directory is fine

    # Output folders
    horizontal_dir: Path = source_path / "horizontal"
    vertical_dir: Path = source_path / "vertical"
    square_dir: Path = source_path / "square"

    # Create folders if they don't exist
    horizontal_dir.mkdir(exist_ok=True)
    vertical_dir.mkdir(exist_ok=True)
    square_dir.mkdir(exist_ok=True)

    # Get list of files for progress tracking
    files_to_process = [f for f in source_path.iterdir() if f.is_file()]

    for file_path in tqdm(files_to_process, desc="Sorting images", unit="file"):

        if file_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        try:
            with Image.open(file_path) as img:
                width, height = img.size

            if width > height:
                dest: Path = horizontal_dir
            elif height > width:
                dest = vertical_dir
            else:
                dest = square_dir

            dest_path: Path = dest / file_path.name
            if copy_mode:
                shutil.copy2(file_path, dest_path)  # copy2 preserves metadata
            else:
                shutil.move(str(file_path), str(dest_path))

        except Exception as ex:
            print(f"Skipping {file_path.name}: {ex}")


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Sort images by orientation"
    )
    parser.add_argument("source_dir", help="Path to the folder containing images")
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy images instead of moving (preserves originals)",
    )
    args: argparse.Namespace = parser.parse_args()

    try:
        sort_images(args.source_dir, copy_mode=args.copy)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)
