# Image operations

## Requirements

* Python 3.x
* Pillow (Python Imaging Library fork)
* tqdm (for progress bar)

Install dependencies:

```bash
pip install -r requirements.txt
```
# Sorter
A simple Python script to sort images into folders based on their orientation:

- Horizontal (landscape)
- Vertical (portrait)
- Square
- 
## Usage
Run the script from your terminal and pass the folder containing your images as an argument:

```bash
python sorter.py /path/to/your/images
```

### Options

- `--copy`: Copy images instead of moving them (preserves originals in source directory)

```bash
python sorter.py /path/to/your/images --copy
```

### Example
```bash
python src/image_sorter/sorter.py /Users/nuno/Library/CloudStorage/ProtonDrive-nuno.cruz.87@pm.me-folder/Photos/2026/IG\ post 
```

## Output Structure

After running, your source directory will look like this:

```
your/images/
├── horizontal/
├── vertical/
├── square/
```

Each image will be moved into the appropriate folder.

##  Notes

* Only files in the top-level directory are processed (no subfolders).
* Non-image files are ignored.
* Corrupted or unsupported images are skipped.
* By default, images are **moved** to the destination folders. Use `--copy` to preserve originals.
* A progress bar displays sorting progress for large directories.

# Transformer
A Python script that recursively resizes images so their largest dimension does not exceed 1080px, preserving aspect ratio. Images are resized in place.

## Usage

```bash
python src/image_sorter/transformer.py /path/to/your/images
```

### Options
- `--max-dim`: Maximum allowed dimension in pixels (default: 1080)

```bash
python src/image_sorter/transformer.py /path/to/your/images --max-dim 720
```

### Example
```bash
python src/image_sorter/transformer.py /Users/nuno/Library/CloudStorage/ProtonDrive-nuno.cruz.87@pm.me-folder/Photos/2026/IG\ post 
```


## Notes

* All subfolders are scanned recursively.
* Images already within the size limit are skipped.
* Images are overwritten in place (no originals preserved).
* Non-image files are ignored.
* Corrupted or unsupported images are skipped.
* A progress bar displays resizing progress for large directories.
