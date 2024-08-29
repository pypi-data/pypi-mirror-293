import os
import argparse
from PIL import Image
import numpy as np
import shutil

class ImageDifference:
    def __init__(self, expectation_path, actual_path):
        self.expectation_path = expectation_path
        self.actual_path = actual_path
        self.img1 = None
        self.img2 = None

    def load_images(self):
        self.img1 = Image.open(self.expectation_path).convert('RGB')
        self.img2 = Image.open(self.actual_path).convert('RGB')
        if self.img1.size != self.img2.size:
            raise ValueError("Images are not the same size.")

    def calculate_difference(self):
        img1_array = np.array(self.img1)
        img2_array = np.array(self.img2)
        diff = np.abs(img1_array - img2_array)
        mask = np.any(diff > 0, axis=-1)
        difference_percentage = (np.sum(mask) / mask.size) * 100
        return mask, difference_percentage

    def apply_overlay(self, mask):
        result_array = np.array(self.img1.copy())
        purple = [128, 0, 128]  # Purple color
        result_array[mask] = purple  # Apply purple overlay where differences are found
        return result_array

    def generate_difference_image(self, difference_path):
        self.load_images()
        mask, difference_percentage = self.calculate_difference()
        print(f"Difference percentage: {difference_percentage:.2f}%")
        result_array = self.apply_overlay(mask)
        result_image = Image.fromarray(result_array)
        result_image.save(difference_path)
        return difference_percentage

def init_directories():
    os.makedirs('vrt-expected', exist_ok=True)
    os.makedirs('vrt-actual', exist_ok=True)
    print("Directories 'vrt-expected' and 'vrt-actual' created.")

def compare_images():
    expected_dir = 'vrt-expected'
    actual_dir = 'vrt-actual'
    output_dir = 'vrt-difference'
    results = {}
    os.makedirs(output_dir, exist_ok=True)
    list_files = os.listdir(expected_dir)

    for filename in list_files:
        expected_path = os.path.join(expected_dir, filename)
        actual_path = os.path.join(actual_dir, filename.replace("expected", "actual"))

        if os.path.exists(actual_path):
            diff_filename = f'difference_{filename}'
            difference_path = os.path.join(output_dir, diff_filename)
            image_diff = ImageDifference(expected_path, actual_path)
            difference_percentage = image_diff.generate_difference_image(difference_path)
            results[diff_filename] = f"{difference_percentage:.2f}"
            print(f"Compared {filename}: {difference_percentage:.2f}% difference")
        else:
            print(f"Actual image not found for {filename}")
    for result in results:
       assert results[result] == '0.00', f"{results}"


def approve_images():
    actual_dir = 'vrt-actual'
    expected_dir = 'vrt-expected'

    for filename in os.listdir(actual_dir):
        actual_path = os.path.join(actual_dir, filename)
        expected_filename = filename.replace('actual_', 'expected_', 1)
        expected_path = os.path.join(expected_dir, expected_filename)

        shutil.copy2(actual_path, expected_path)
        print(f"Copied {filename} to {expected_filename}")

def main():
    parser = argparse.ArgumentParser(description="Visual Regression Testing (VRT) CLI Tool")
    subparsers = parser.add_subparsers(dest='command')

    parser_init = subparsers.add_parser('init', help='Initialize the VRT directories')
    parser_compare = subparsers.add_parser('compare', help='Compare images in vrt-expected and vrt-actual')
    parser_approve = subparsers.add_parser('approve', help='Approve actual images and move them to vrt-expected')

    args = parser.parse_args()

    if args.command == 'init':
        init_directories()
    elif args.command == 'compare':
        compare_images()
    elif args.command == 'approve':
        approve_images()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()