import streamlit as st
import json
import os
from PIL import Image, ImageDraw
from collections import Counter
import pandas as pd
def extract_unique_image_ids(json_data):
    """Extracts all unique image_ids from the json data."""
    return set([int(i['image_id']) for i in json_data])

def filter_annotations_by_image_id(image_id, json_data):
    """Filters annotations for a given image_id."""
    return [item for item in json_data if item['image_id'] == image_id]

def get_image_annotations(image_id, directory, json_data):
    """Returns the filtered list of annotations for a given image_id and the image path."""
    filtered_annotations = filter_annotations_by_image_id(image_id, json_data)
    image_path = os.path.join(directory, f'{str(image_id).zfill(5)}.png')
    return filtered_annotations, image_path

names=['vehicle','person']

# res = json.load(open('runs/test/yolov4-pacsp-export-22/best_overall_predictions.json','r'))
# res = json.load(open('/nvmefs1/andrew.mendez/fmv_subset_preds/predictions.json','r'))
# unique = list(extract_unique_image_ids(res))

def plot_predictions(image_id, image_directory, annotations_json, threshold=0.4):
    """
    Visualizes object detection predictions on an image.
    
    Args:
        image_id (int): The unique identifier for the image.
        image_directory (str): Path to the directory containing the images.
        annotations_json (list of dict): The JSON data containing the annotations.
        threshold (float): The score threshold for displaying annotations.

    Returns:
        PIL.Image: Image with drawn annotations.
    """
    filtered_annotations, image_path = get_image_annotations(image_id, image_directory, annotations_json)

    # Check if the image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found at {image_path}")

    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Optional: Load a font for text display
    # font = ImageFont.truetype("arial.ttf", 15)  # Replace with the path to your font file

    for annotation in filtered_annotations:
        if annotation['score'] > threshold:
            x, y, w, h = annotation['bbox']
            draw.rectangle([x, y, x + w, y + h], outline="red")

            # Prepare the text to display
            text = f"ID: {names[annotation['category_id']]}, Score: {annotation['score']:.2f}"

            # Draw text with or without a custom font
            draw.text((x, y), text, fill="yellow")  # Add `, font=font` if using a custom font

    return image
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def plot_predictions(image_id, image_directory, annotations_json, threshold=0.3):
    """
    Visualizes object detection predictions on an image and counts detections.

    Args:
        image_id (int): The unique identifier for the image.
        image_directory (str): Path to the directory containing the images.
        annotations_json (list of dict): The JSON data containing the annotations.
        threshold (float): The score threshold for displaying annotations.

    Returns:
        PIL.Image: Image with drawn annotations.
        dict: Count of detections per category.
    """
    filtered_annotations, image_path = get_image_annotations(image_id, image_directory, annotations_json)

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found at {image_path}")

    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    category_counts = Counter()

    for annotation in filtered_annotations:
        print(annotation)
        if annotation['score'] > threshold:
            print("-- ",annotation)
            category_counts[names[annotation['category_id']]] += 1

            x, y, w, h = annotation['bbox']
            draw.rectangle([x, y, x + w, y + h], outline="red")
            text = f"{names[annotation['category_id']]}, Score: {annotation['score']:.2f}"
            draw.text((x, y), text, fill="yellow")

    return image, category_counts

def main():
    st.title("Object Detection Visualizer")

    # json_data = load_json_data('/nvmefs1/andrew.mendez/fmv_full_preds/predictions.json')
    json_data = load_json_data('/pfs/export/predictions.json')

    unique_image_ids = list(extract_unique_image_ids(json_data))

    selected_id = st.slider("Select Image ID", min(unique_image_ids), max(unique_image_ids), unique_image_ids[0])
    # image_directory = '/nvmefs1/andrew.mendez/fmv_vid/frames/'
    image_directory = '/pfs/export/frames/'

    try:
        image, counts = plot_predictions(selected_id, image_directory, json_data)
        st.image(image, caption=f"Image ID: {selected_id}", use_column_width=True)

        # Displaying the counts as a table
        st.subheader("Number of Targets Detected in Image")
        print(counts.items())
        data_dict = dict(counts.items())
        print(data_dict)
        # Create a DataFrame
        df = pd.DataFrame([data_dict])

        # Rename the columns
        df.rename(columns={'vehicle': 'Vehicle(s)', 'person': 'Person(s)'}, inplace=True)

        # Display the table in Streamlit
        st.table(df)
        # print(counts.items())
        # st.table(counts.items())

    except FileNotFoundError as e:
        st.error(f"Error: {e}")

if __name__ == "__main__":
    main()