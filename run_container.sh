
docker run --gpus all \
           --name yolov4 -it \
           -v /home/andrew/coco/:/coco/ \
           -v /home/andrew/PyTorch_YOLOv4:/yolo -p 8000:8000 \
           --shm-size=64g nvcr.io/nvidia/pytorch:20.11-py3

