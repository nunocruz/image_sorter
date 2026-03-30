# Image Orientation Sorter

A simple Python script to sort images into folders based on their orientation:

- Horizontal (landscape)
- Vertical (portrait)
- Square

## Requirements

* Python 3.x
* Pillow (Python Imaging Library fork)

Install dependencies:

```bash
pip install pillow
```

## Usage

Run the script from your terminal and pass the folder containing your images as an argument:

```bash
python sorter.py /path/to/your/images
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

* Files are **moved**, not copied. If you want to keep originals, modify the script to use `shutil.copy` instead of `shutil.move`.
* Only files in the top-level directory are processed (no subfolders).
* Non-image files are ignored.
* Corrupted or unsupported images are skipped.

