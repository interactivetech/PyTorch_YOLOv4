#!/bin/bash

#Install Kubectl
# curl -Lo /nvmefs1/andrew.mendez/kubectl "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
install -o root -g root -m 0755 /nvmefs1/andrew.mendez/kubectl /usr/local/bin/kubectl

# export ROOT_DIR=/mnt/efs/shared_fs/determined/nb_fs/dev-llm-rag-app/pipeline_notebooks/
export ROOT_DIR="/nvmefs1/shared_nb/01 - Users/andrew.mendez/2024/PyTorch_YOLOv4/app"
FRAMES_DIR=$(head -n 1 /pfs/out/app_content.txt)
export FRAMES_DIR; 
PRED_JSON=$(sed -n '2p' /pfs/out/app_content.txt)
export PRED_JSON
VID_PATH=$(sed -n '3p' /pfs/out/app_content.txt)
export VID_PATH
echo "$PRED_JSON"
echo "$FRAMES_DIR"
echo "$VID_PATH"
# Check if the pod exists
export POD_NAME=streamlit-np-pod

if kubectl get pod -n pachyderm "$POD_NAME" --ignore-not-found --output name | grep -q "$POD_NAME"; then
    echo "Pod $POD_NAME exists."
else
    sed -e "s|{{PRED_JSON}}|$PRED_JSON|g" \
        -e "s|{{FRAMES_DIR}}|$FRAMES_DIR|g" \
        -e "s|{{VID_PATH}}|$VID_PATH|g" \
        "$ROOT_DIR"/k8s-app-template.yaml > "$ROOT_DIR"/k8s-app-runner.yaml
    kubectl apply -n pachyderm -f "$ROOT_DIR"/k8s-app-runner.yaml
    kubectl wait -n pachyderm --for=condition=ready  pod/streamlit-np-pod
#     echo "Pod $POD_NAME does not exist, creating..."
#     export HOST_VOLUME2=/nvmefs1/andrew.mendez/titanml_cache
#     export HOST_VOLUME3=/nvmefs1/
#     # export TAKEOFF_MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.1
#     export TAKEOFF_MODEL_NAME=/nvmefs1/andrew.mendez/mistral_instruct_model_and_tokenizer/
#     # export TAKEOFF_MODEL_NAME=/mnt/efs/shared_fs/mistral_ckpt/mistral_model/
#     export TAKEOFF_DEVICE=cuda
#     export API_PORT=8080
#     export API_HOST=10.182.1.48
    
#     sed -e "s|{{HOST_VOLUME}}|$HOST_VOLUME2|g" \
#        -e "s|{{HOST_VOLUME2}}|$HOST_VOLUME3|g" \
#        -e "s|{{TAKEOFF_MODEL_NAME}}|$TAKEOFF_MODEL_NAME|g" \
#        -e "s|{{API_PORT}}|$API_PORT|g" \
#        -e "s|{{API_HOST}}|$API_HOST|g" \
#        -e "s|{{TAKEOFF_DEVICE}}|$TAKEOFF_DEVICE|g" \
#         "$ROOT_DIR"/titanml-pod-template.yaml > "$ROOT_DIR"/titanml-pod-runner.yaml
#     kubectl apply -f "$ROOT_DIR"/titanml-pod-runner.yaml
#     kubectl wait --for=condition=ready pod/titanml-pod

    echo "Done!"
fi