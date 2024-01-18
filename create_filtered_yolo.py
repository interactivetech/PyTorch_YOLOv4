import os
import shutil
import argparse
import logging

def copy_files(src_dir, dest_dir, start_num=1, end_num=20):
    """
    Copies files from src_dir to dest_dir. Only copies files with numbers from start_num to end_num.

    :param src_dir: Source directory from which to copy files.
    :param dest_dir: Destination directory to which to copy files.
    :param start_num: Starting number of files to copy.
    :param end_num: Ending number of files to copy.
    """
    # Create the destination directory if it does not exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Loop through the range of file numbers
    for i in range(start_num, end_num + 1):
        # Construct file names for PNG and text files
        png_file = f"{i:06d}.png"
        txt_file = f"{i:06d}.txt"

        # Copy PNG file if it exists
        src_png = os.path.join(src_dir, png_file)
        if os.path.exists(src_png):
            dest_png = os.path.join(dest_dir, png_file)
            shutil.copy(src_png, dest_png)
            logging.info(f"Copied {src_png} to {dest_png}")
        # Copy text file if it exists
        src_txt = os.path.join(src_dir, txt_file)
        if os.path.exists(src_txt):
            dest_txt = os.path.join(dest_dir, txt_file)
            shutil.copy(src_txt, dest_txt)
            logging.info(f"Copied {src_txt} to {dest_txt}")

# Example usage
# copy_files('path/to/source/directory', 'path/to/destination/directory')

# Set up the argument parser
parser = argparse.ArgumentParser(description="Copy a subset of files from source to destination directory.")
parser.add_argument('--src-dir', type=str, required=True, help='Source directory from which to copy files.')
parser.add_argument('--dest-dir', type=str, required=True, help='Destination directory to which to copy files.')

# Parse the arguments
args = parser.parse_args()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Call the function with the provided arguments
copy_files(args.src_dir, args.dest_dir)