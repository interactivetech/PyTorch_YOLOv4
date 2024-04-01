#!/bin/bash

# Check if an argument was provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 path/to/video"
    exit 1
fi

# Get the full path of the video
VIDEO_PATH="$1"

# Extract the filename without the extension
FILENAME=$(basename -- "$VIDEO_PATH")
EXTENSION="${FILENAME##*.}"
FILENAME="${FILENAME%.*}"

# Create a directory with the same name as the video
DIR_PATH=$(dirname -- "$VIDEO_PATH")/"$FILENAME"
mkdir -p "$DIR_PATH"
echo "Directory created: $DIR_PATH"

# Move the video into the newly created directory
mv "$VIDEO_PATH" "$DIR_PATH"
echo "Video moved to: $DIR_PATH/$FILENAME.$EXTENSION"

# Create a frames directory inside the new directory
FRAMES_DIR="$DIR_PATH/frames"
mkdir -p "$FRAMES_DIR"
echo "Frames directory created: $FRAMES_DIR"

# Extract frames using ffmpeg
ffmpeg -i "$DIR_PATH/$FILENAME.$EXTENSION" "$FRAMES_DIR/%05d.png"
echo "Frame extraction complete. Frames saved in: $FRAMES_DIR"