import os
import shutil
import tempfile
import unittest
from PIL import Image

from sorter import sort_images


class TestImageSorting(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

        # Create test images
        self.create_image("horizontal.jpg", (200, 100))
        self.create_image("vertical.jpg", (100, 200))
        self.create_image("square.jpg", (150, 150))

    def tearDown(self):
        # Clean up after test
        shutil.rmtree(self.test_dir)

    def create_image(self, name, size):
        path = os.path.join(self.test_dir, name)
        img = Image.new("RGB", size)
        img.save(path)

    def test_images_are_sorted_correctly(self):
        sort_images(self.test_dir)

        self.assertTrue(
            os.path.exists(os.path.join(self.test_dir, "horizontal", "horizontal.jpg"))
        )
        self.assertTrue(
            os.path.exists(os.path.join(self.test_dir, "vertical", "vertical.jpg"))
        )
        self.assertTrue(
            os.path.exists(os.path.join(self.test_dir, "square", "square.jpg"))
        )


if __name__ == "__main__":
    unittest.main()
