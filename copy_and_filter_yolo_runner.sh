python copy_and_filter_yolo.py \
  --yolo-dir /nvmefs1/andrew.mendez/virat-aerial-156-frames-v2-coco-yolov5/ \
  --new-yolo-dir /nvmefs1/andrew.mendez/virat-aerial-156-frames-v2-coco-yolov5-subset

rm /nvmefs1/andrew.mendez/virat-aerial-156-frames-v2-coco-yolov5-subset/*.cache3 -v