#!/bin/bash
set -e  # stop on error

echo "Running tests..."
python -m unittest tests.test_sorter

echo "Done."
