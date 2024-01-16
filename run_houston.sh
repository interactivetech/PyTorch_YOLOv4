# python train.py --device 0 --batch-size 16 --img 640 640 --data coco.yaml --cfg cfg/yolov4-pacsp.cfg --weights '' --name yolov4-pacsp --epochs 1
# export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5
python -m torch.distributed.launch \
  --nproc_per_node=2 \
  --master_port=29506 train.py \
  --device 0,1,2,3,4,5 \
  --batch-size 6 \
  --img 640 640 \
  --data coco.yaml \
  --cfg cfg/yolov4-pacsp.cfg \
  --weights '' \
  --name yolov4-pacsp \
  --epochs 2