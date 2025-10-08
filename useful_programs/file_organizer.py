#!/usr/bin/env python3
"""Organize files in a directory into subfolders by extension.

Usage: python file_organizer.py [target_dir]
"""
import os
import shutil
import sys


def organize(target_dir: str):
    if not os.path.isdir(target_dir):
        raise ValueError(f"Not a directory: {target_dir}")
    for entry in os.listdir(target_dir):
        full = os.path.join(target_dir, entry)
        if os.path.isfile(full):
            _, ext = os.path.splitext(entry)
            ext = ext[1:].lower() or "no_ext"
            dest_dir = os.path.join(target_dir, ext)
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(full, os.path.join(dest_dir, entry))


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    organize(target)
    print(f"Organized files in {target}")


if __name__ == "__main__":
    main()
