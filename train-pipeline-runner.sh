#!/bin/bash

# Define the directory
DIR="/pfs/data/train/"
echo "Installing Determined Client..."
pip install determined==0.26.1
echo "Done!"
# Count the number of .png files in the directory
PNG_COUNT=$(find $DIR -name "*.png" | wc -l)

# Check if the count is greater than 20
if [ $PNG_COUNT -gt 20 ]; then
    # If more than 20 .png files, run python -c "print(1)"
    echo "Running train-det-runner-full.py..."
    python /nvmefs1/shared_nb/01\ -\ Users/andrew.mendez/2024/PyTorch_YOLOv4/train-det-runner-full.py
    echo "Done!"
else
    # If 20 or fewer .png files, run python -c "print(0)"
    echo "Running train-det-runner-subset.py..."
    python /nvmefs1/shared_nb/01\ -\ Users/andrew.mendez/2024/PyTorch_YOLOv4/train-det-runner-subset.py
    echo "Done!"
fi

