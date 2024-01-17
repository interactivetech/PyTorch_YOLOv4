# python train.py --device 0 --batch-size 16 --img 640 640 --data coco.yaml --cfg cfg/yolov4-pacsp.cfg --weights '' --name yolov4-pacsp --epochs 1
# export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5
python -m torch.distributed.launch \
  --nproc_per_node=6 \
  --master_port=29506 train.py \
  --device 0,1,2,3,4,5,6,7 \
  --batch-size 384 \
  --img 640 640 \
  --data coco.yaml \
  --cfg cfg/yolov4-pacsp.cfg \
  --weights '' \
  --name yolov4-pacsp-a100-300 \
  --epochs 300
  --exists-ok
  
echo "Running Evaluation..."

python test.py --img 640 \
               --conf 0.001 \
               --batch 32 \
               --device 0 \
               --data coco.yaml \
               --cfg cfg/yolov4-pacsp.cfg \
               --weights runs/train/yolov4-pacsp-a100-300/weights/best_overall.pt 

echo "Done!"