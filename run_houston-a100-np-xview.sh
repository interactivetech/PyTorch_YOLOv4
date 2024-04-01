# python train.py --device 0 --batch-size 16 --img 640 640 --data coco.yaml --cfg cfg/yolov4-pacsp.cfg --weights '' --name yolov4-pacsp --epochs 1
# export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5
MODEL_CFG=yolov4-csp-leaky-xview37class.cfg
echo cfg/$MODEL_CFG
EXP_DIR=yolov4-csp-leaky-a100-300-xview
EXP_DIR_test=${EXP_DIR}_test
# DATASET_CFG=get_xview.yaml
DATASET_CFG=xview_37.yaml

# NEED TO DO 299 + how many epochs you want to additionally train from weights

# python -m torch.distributed.launch \
#   --nproc_per_node=2 \
#   --master_port=29506 train.py \
#   --device 0,1 \
#   --batch-size 32 \
#   --img 1280 1280 \
#   --data $DATASET_CFG \
#   --cfg cfg/$MODEL_CFG \
#   --weights ./runs/train/yolov4-csp-leaky-a100-300-319/weights/best_overall.pt \
#   --name $EXP_DIR \
#   --epochs 600
  python -m torch.distributed.launch \
  --nproc_per_node=2 \
  --master_port=29506 train.py \
  --device 0,1 \
  --batch-size 32 \
  --img 1280 1280 \
  --data $DATASET_CFG \
  --cfg cfg/$MODEL_CFG \
  --weights  ./runs/train/yolov4-csp-leaky-a100-300-319/weights/best_overall.pt \
  --name $EXP_DIR \
  --epochs 600
# python train.py \
#   --batch-size 32 \
#   --img 640 640 \
#   --data $DATASET_CFG \
#   --cfg cfg/$MODEL_CFG \
#   --weights ''  \
#   --name $EXP_DIR \
#   --epochs 1   

echo "Running Evaluation..."

python test.py --img 1280 \
               --conf 0.001 \
               --batch 2 \
               --device 0 \
               --data $DATASET_CFG \
               --cfg cfg/$MODEL_CFG \
               --weights runs/train/$EXP_DIR/weights/best_overall.pt \
               --names xview_cfg/xview37.names \
               --name  $EXP_DIR_test

echo "Done!"