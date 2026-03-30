# Image Orientation Sorter

A simple Python script to sort images into folders based on their orientation:

- Horizontal (landscape)
- Vertical (portrait)
- Square

## Requirements

* Python 3.x
* Pillow (Python Imaging Library fork)
* tqdm (for progress bar)

Install dependencies:

```bash
pip install -r requirements.txt
```

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
python sorter.py ~/Pictures/shoot_01
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

