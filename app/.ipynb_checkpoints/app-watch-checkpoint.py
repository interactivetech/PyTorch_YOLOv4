import datetime as dt
import os
import uuid
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import streamlit as st
import json
from PIL import Image, ImageDraw
from collections import Counter
import pandas as pd

class Watchdog(FileSystemEventHandler):
    def __init__(self, hook):
        self.hook = hook

    def on_modified(self, event):
        self.hook()

def update_dummy_module():
    dummy_path = '/nvmefs1/andrew.mendez/deployments_watcher_dummy.py'
    with open(dummy_path, "w") as fp:
        random_uuid_string = str(uuid.uuid4())
        fp.write(f'timestamp = "{dt.datetime.now()}-{random_uuid_string}"')

@st.cache_resource
def install_monitor():
    observer = Observer()
    observer.schedule(Watchdog(update_dummy_module), path="/nvmefs1/andrew.mendez/deployments_watcher", recursive=False)
    observer.start()

def count_png_files(directory):
    return len([name for name in os.listdir(directory) if name.endswith('.png')])

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
def get_paths(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

        if len(lines) < 2:
            return "File does not contain enough paths."

        directory_path = lines[0].strip()  # First line for directory path
        json_path = lines[1].strip()  # Second line for JSON file path

        return directory_path, json_path
def print_dict_items(dict_items):
    # Convert dict_items to a dictionary if it's not already
    if not isinstance(dict_items, dict):
        dict_items = dict(dict_items)

    # Check for the keys and prepare the print statement
    vehicle_count = dict_items.get('vehicle', 0)
    person_count = dict_items.get('person', 0)
    print("vehicle_count: ",vehicle_count)
    print("person_count: ",vehicle_count)
    if vehicle_count and person_count:
        st.write(f"There are {vehicle_count} vehicles and {person_count} person(s).")
    elif vehicle_count:
        st.write(f"There are {vehicle_count} vehicles.")
    elif person_count:
        st.write(f"There is {person_count} person(s).")
    else:
        print("There are no vehicles or persons.")
            # st.table(df)
            # print(counts.items())
            # st.table(counts.items())
def read_deployment_file(path):
    with open(path, 'r') as file:
        lines = file.readlines()
        if len(lines) >= 3:
            frame_dir, predictions_json, video_path = lines[:3]
            frame_dir = frame_dir.strip()
            predictions_json = predictions_json.strip()
            video_path = video_path.strip()
            return frame_dir, predictions_json, video_path                        

def main():
    install_monitor()
    st.title("Real-Time, Energy Efficient Full Motion Video (FMV) Analysis using IBM NorthPole and HPE MLOPs Platform")
    st.markdown('''
    This is a demo that showcases how IBM's NorthPole AI Accelerator and HPE's MLOPs Platform allows
    real-time, low power AI powered FMV analysis at the edge. We use the NorthPole accelerator to process FMV video, 
    and the HPE MLOPs platform for training, tuning, and deploying AI at Scale.
    ''')

    # video_file = open('/nvmefs1/andrew.mendez/fmv_full_preds/out/output_vid.mp4', 'rb')
    # @st.cache_data
    # def read_bytes(video_file):
    #     video_bytes = video_file.read()
    # video_bytes=read_bytes(video_file)
    try:
        import os
        # directory_path, json_path = get_paths('/pfs/out/app_content.txt')
        json_path = os.environ.get('PRED_JSON')
        directory_path = os.environ.get('FRAMES_DIR')
        vid_path = os.environ.get('VID_PATH')
        directory_path, json_path, vid_path = read_deployment_file('/nvmefs1/andrew.mendez/deployments_watcher/app_content.txt')

        print("directory_path, json_path vid_path: ", directory_path, json_path, vid_path )
        
        # print("Number of frames: ",os.listdir("/pfs/export/frames/"))
    except Exception as e:
        print(e)
    
    json_data = load_json_data(json_path)
    # json_data = load_json_data('/pfs/export/predictions.json')

    unique_image_ids = list(extract_unique_image_ids(json_data))
    slider_id = st.slider("Select Image ID", min(unique_image_ids), max(unique_image_ids), unique_image_ids[0])
    col1, col2 = st.columns(2)
    with col1:
        st.header("Processed Video")
        st.video(vid_path)




    # image_directory = '/pfs/export/frames/'

    with col2:
        try:
            image_directory = directory_path
            image, counts = plot_predictions(slider_id, image_directory, json_data)
            st.header("Individual Frames")
            st.image(image, caption=f"Image ID: {slider_id}", use_column_width=True)
            

    
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

            print_dict_items(data_dict)

        except FileNotFoundError as e:
            st.error(f"Error: {e}")
    
    st.header("MLOPS Pipeline managing End to End Pipeline")
    full_screen_iframe = """
    <style>
        .iframe-container {
            position: relative;
            width: 100%;
            height: 100vh; /* Adjust the height as needed */
        }
        .iframe-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }
    </style>
    <div class="iframe-container">
        <iframe src="http://mldm-pachyderm.us.rdlabs.hpecorp.net/lineage/north-pole/"></iframe>
    </div>
"""
    st.write(
        full_screen_iframe,
        unsafe_allow_html=True,
    )
    st.header("Platform to manage resources and training for AI")
    # Define the URL and the text to display
    url = "http://mlds-determined.us.rdlabs.hpecorp.net:8080/det/experiments/7045/overview"
    link_text = "http://mlds-determined.us.rdlabs.hpecorp.net:8080/det/experiments/7045/overview"

    # Use Markdown to display the hyperlink
    st.markdown(f"[{link_text}]({url})")
#     full_screen_iframe2 = """
#     <style>
#         .iframe-container {
#             position: relative;
#             width: 100%;
#             height: 100vh; /* Adjust the height as needed */
#         }
#         .iframe-container iframe {
#             position: absolute;
#             top: 0;
#             left: 0;
#             width: 100%;
#             height: 100%;
#             border: none;
#         }
#     </style>
#     <div class="iframe-container">
#         <iframe src="http://mlds-determined.us.rdlabs.hpecorp.net:8080/det/login"></iframe>
#     </div>
# """
    # st.write(
    #     full_screen_iframe2,
    #     unsafe_allow_html=True,
    # )
    # Sidebar for tracking updates
    if 'update_list' not in st.session_state:
        st.session_state.update_list = []

    st.session_state.update_list.append(f"model deployed: {dt.datetime.now()}")

    st.sidebar.write("Model Deployment Log:")
    for update_message in st.session_state.update_list:
        st.sidebar.write(update_message)
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    
    main()