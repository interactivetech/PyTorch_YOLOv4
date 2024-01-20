#!/bin/bash

# Define the directory
DIR="/pfs/data/train/"
echo "Installing Determined Client..."
echo "Done!"
# Count the number of .png files in the directory
PNG_COUNT=$(find $DIR -name "*.png" | wc -l)

# Check if the count is greater than 20
if [ $PNG_COUNT -gt 20 ]; then
    # If more than 20 .png files, run python -c "print(1)"
    echo "Exporting fmv_train_exp/weights/best.pt..."
    MODEL_DIR=/nvmefs1/andrew.mendez/yolov4_train_runs/fmv_train_exp/weights/best.pt
    sleep 3 # Placeholder, this simulates exporting the pytorch model for the IBM Accelerator
    echo "$(openssl rand -base64 12)" > /pfs/out/random_file.txt # Bash Command to ensure pachyderm sees a new output is completed, and doesnt skip
    cp /nvmefs1/andrew.mendez/fmv_full_preds/predictions.json /pfs/out/ -v
    cp -R /nvmefs1/andrew.mendez/fmv_vid/frames/ /pfs/out/ -v
    echo "Done!"
else
    # If 20 or fewer .png files, run python -c "print(0)"
    MODEL_DIR=/nvmefs1/andrew.mendez/yolov4_train_runs/fmv_train_subset_exp/weights/best.pt
    echo "Exporting fmv_train_subset_exp/weights/best.pt..."
    sleep 3 # Placeholder, this simulates exporting the pytorch model for the IBM Accelerator
    echo "$(openssl rand -base64 12)" > /pfs/out/random_file.txt # Bash Command to ensure pachyderm sees a new output is completed, and doesnt skip
    cp /nvmefs1/andrew.mendez/fmv_subset_preds/predictions.json /pfs/out/ -v
    cp -R /nvmefs1/andrew.mendez/fmv_vid/frames/ /pfs/out/ -v
    echo "Done!"
fi
