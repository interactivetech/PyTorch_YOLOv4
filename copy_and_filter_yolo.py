import os
import shutil
import argparse
import logging
import yaml

def copy_files(src_dir, dest_dir, start_num=1, end_num=20):
    for i in range(start_num, end_num + 1):
        png_file = f"{i:06d}.png"
        txt_file = f"{i:06d}.txt"

        src_png = os.path.join(src_dir, png_file)
        if os.path.exists(src_png):
            dest_png = os.path.join(dest_dir, png_file)
            shutil.copy(src_png, dest_png)
            logging.info(f"Copied {src_png} to {dest_png}")

        src_txt = os.path.join(src_dir, txt_file)
        if os.path.exists(src_txt):
            dest_txt = os.path.join(dest_dir, txt_file)
            shutil.copy(src_txt, dest_txt)
            logging.info(f"Copied {src_txt} to {dest_txt}")

def copy_directory_contents(src_dir, dest_dir):
    for item in os.listdir(src_dir):
        src_item = os.path.join(src_dir, item)
        dest_item = os.path.join(dest_dir, item)

        if os.path.isdir(src_item) and item in ['train', 'val']:
            continue

        if os.path.isdir(src_item):
            shutil.copytree(src_item, dest_item)
        else:
            shutil.copy(src_item, dest_item)
            logging.info(f"Copied {src_item} to {dest_item}")

def copy_filtered_folders(yolo_dir, new_yolo_dir, folder_names):
    for folder_name in folder_names:
        src_folder = os.path.join(yolo_dir, folder_name)
        dest_folder = os.path.join(new_yolo_dir, folder_name)
        if os.path.exists(src_folder):
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
            copy_files(src_folder, dest_folder)

def update_data_yaml(yolo_dir, new_yolo_dir):
    """
    Updates the train and val paths in the data.yml file.

    :param yolo_dir: Original YOLO directory.
    :param new_yolo_dir: New YOLO directory.
    """
    data_yaml_path = os.path.join(yolo_dir, 'data.yml')
    new_data_yaml_path = os.path.join(new_yolo_dir, 'data.yml')

    if os.path.exists(data_yaml_path):
        with open(data_yaml_path, 'r') as file:
            data = yaml.safe_load(file)

        # Update the train and val paths
        data['train'] = os.path.join(new_yolo_dir, 'train')
        data['val'] = os.path.join(new_yolo_dir, 'val')

        # Write the updated data to the new data.yml file
        with open(new_data_yaml_path, 'w') as file:
            yaml.dump(data, file)

        logging.info(f"Updated data.yml file saved at {new_data_yaml_path}")

        
# Set up the argument parser
parser = argparse.ArgumentParser(description="Process YOLO directories.")
parser.add_argument('--yolo-dir', type=str, required=True, help='Original YOLO directory.')
parser.add_argument('--new-yolo-dir', type=str, required=True, help='New YOLO directory to create.')

# Parse the arguments
args = parser.parse_args()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create the new YOLO directory if it doesn't exist
if not os.path.exists(args.new_yolo_dir):
    os.makedirs(args.new_yolo_dir)

# Copy all files except 'train' and 'val' directories
copy_directory_contents(args.yolo_dir, args.new_yolo_dir)

# Copy 'train' and 'val' directories using original copy_files function
copy_filtered_folders(args.yolo_dir, args.new_yolo_dir, ['train', 'val'])

# Update the data.yml file
update_data_yaml(args.yolo_dir, args.new_yolo_dir)