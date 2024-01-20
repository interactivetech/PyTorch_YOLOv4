
# run detections

# Need to convert yolo to coco
SOURCE_DIR=/nvmefs1/andrew.mendez/fmv_vid/frames
OUTPUT_DIR=/nvmefs1/andrew.mendez/fmv_full_preds

mkdir $OUTPUT_DIR
echo "Created $OUTPUT_DIR"

python detect.py --weights /nvmefs1/andrew.mendez/yolov4_train_runs/fmv_train_exp/weights/best.pt \
  --source $SOURCE_DIR \
  --output $OUTPUT_DIR \
  --img-size 640 \
  --conf-thres 0.4 \
  --iou-thres 0.3 \
  --device 0 \
  --save-txt  \
  --cfg cfg/yolov4-pacsp-fmv.cfg \
  --names data/fmv.names \
  --save-json
  
# move .png and .txt to seperate folder
mkdir $OUTPUT_DIR/out/
echo "Creating $OUTPUT_DIR/out/..."

# Move all PNG and TXT files to the out/ directory
mv $OUTPUT_DIR/*.png $OUTPUT_DIR/*.txt $OUTPUT_DIR/out/
echo "Moved $OUTPUT_DIR/*.png OUTPUT_DIR/*.txt to $OUTPUT_DIR/out"

# Step 3: Run FFMPEG to combine PNG files in the out/ directory into a video
cd $OUTPUT_DIR
ffmpeg -framerate 30 -pattern_type glob -i 'out/*.png' -c:v libx264 -pix_fmt yuv420p out/output_vid.mp4