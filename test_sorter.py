import shutil
import tempfile
import unittest
import os
from pathlib import Path
from PIL import Image

from sorter import sort_images


class TestImageSorting(unittest.TestCase):

    def setUp(self) -> None:
        # Create a temporary directory
        self.test_dir: Path = Path(tempfile.mkdtemp())

        # Create test images
        self.create_image("horizontal.jpg", (200, 100))
        self.create_image("vertical.jpg", (100, 200))
        self.create_image("square.jpg", (150, 150))

    def tearDown(self) -> None:
        # Clean up after test
        shutil.rmtree(self.test_dir)

    def create_image(self, name: str, size: tuple[int, int]) -> None:
        path: Path = self.test_dir / name
        img: Image.Image = Image.new("RGB", size)
        img.save(path)

    def test_images_are_sorted_correctly(self) -> None:
        sort_images(self.test_dir)

        self.assertTrue((self.test_dir / "horizontal" / "horizontal.jpg").exists())
        self.assertTrue((self.test_dir / "vertical" / "vertical.jpg").exists())
        self.assertTrue((self.test_dir / "square" / "square.jpg").exists())

    def test_copy_mode_preserves_originals(self) -> None:
        sort_images(self.test_dir, copy_mode=True)

        # Original should still exist
        self.assertTrue((self.test_dir / "horizontal.jpg").exists())
        # Copy should also exist in subdirectory
        self.assertTrue((self.test_dir / "horizontal" / "horizontal.jpg").exists())

    def test_empty_directory(self) -> None:
        """Test that sorter handles empty directories gracefully."""
        empty_dir: Path = Path(tempfile.mkdtemp())
        try:
            # Should not raise an exception
            sort_images(str(empty_dir))

            # Should create subdirectories
            self.assertTrue((empty_dir / "horizontal").exists())
            self.assertTrue((empty_dir / "vertical").exists())
            self.assertTrue((empty_dir / "square").exists())
        finally:
            shutil.rmtree(empty_dir)

    def test_unsupported_image_types_are_skipped(self) -> None:
        """Test that non-image files are ignored."""
        # Create non-image files
        (self.test_dir / "document.txt").write_text("This is a text file")
        (self.test_dir / "script.py").write_text("print('hello')")
        (self.test_dir / "data.json").write_text('{"key": "value"}')

        # Run sorter
        sort_images(self.test_dir)

        # Non-image files should still be in root directory
        self.assertTrue((self.test_dir / "document.txt").exists())
        self.assertTrue((self.test_dir / "script.py").exists())
        self.assertTrue((self.test_dir / "data.json").exists())

        # They should NOT be in subdirectories
        self.assertFalse((self.test_dir / "horizontal" / "document.txt").exists())
        self.assertFalse((self.test_dir / "vertical" / "script.py").exists())
        self.assertFalse((self.test_dir / "square" / "data.json").exists())

    def test_corrupted_images_are_skipped_gracefully(self) -> None:
        """Test that corrupted images don't crash the sorter."""
        # Create a file with .jpg extension but invalid image data
        corrupted_path: Path = self.test_dir / "corrupted.jpg"
        corrupted_path.write_bytes(b"This is not a valid JPEG file")

        # Should not raise an exception
        sort_images(self.test_dir)

        # Corrupted file should still be in root (not moved/copied)
        self.assertTrue((self.test_dir / "corrupted.jpg").exists())

        # Valid images should still be sorted
        self.assertTrue((self.test_dir / "horizontal" / "horizontal.jpg").exists())
        self.assertTrue((self.test_dir / "vertical" / "vertical.jpg").exists())
        self.assertTrue((self.test_dir / "square" / "square.jpg").exists())

    def test_invalid_file_permissions(self) -> None:
        """Test that sorter gracefully handles permission errors during processing."""
        # Create a valid image
        self.create_image("restricted.jpg", (200, 100))

        # Remove read permissions (but keep write for cleanup)
        restricted_path: Path = self.test_dir / "restricted.jpg"
        os.chmod(restricted_path, 0o000)

        try:
            # Should not raise an exception; file should be skipped
            sort_images(self.test_dir)

            # File should still exist in root (permission denied prevented moving)
            self.assertTrue(restricted_path.exists())

            # Other images should still be sorted
            self.assertTrue((self.test_dir / "horizontal" / "horizontal.jpg").exists())
        finally:
            # Restore permissions for cleanup
            os.chmod(restricted_path, 0o644)


if __name__ == "__main__":
    unittest.main()
