#!/bin/bash
set -e  # stop on error

echo "Running tests..."
python -m unittest test_sorter.py

echo "Done."