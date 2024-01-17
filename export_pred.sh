echo "Running Evaluation..."

python test.py --img 640 \
               --conf 0.001 \
               --batch 32 \
               --device 0 \
               --data coco.yaml \
               --cfg cfg/yolov4-pacsp.cfg \
               --weights runs/train/yolov4-pacsp-a100-48/weights/best_overall.pt\
               --save-json \
               --name export-preds
echo "Done!"