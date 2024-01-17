python test.py --img 640 \
               --conf 0.001 \
               --batch 32 \
               --device 0 \
               --data cocoy.yaml \
               --cfg cfg/yolov4-pacsp.cfg \
               --weights runs/train/yolov4-pacsp-a100-48/weights/best_overall.pt \
               --name yolov4-pacsp-export-2 \
               --save-json