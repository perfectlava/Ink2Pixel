#!/bin/bash
# Ink2Pixel Runner for macOS/Linux

# Navigate to the script's directory
cd "$(dirname "$0")"

clear
echo "===================================================="
echo "          INK2PIXEL: DOCUMENT DIGITIZER             "
echo "===================================================="
echo ""

# 1. Check for virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# 2. Check Dependencies (Quietly)
echo "Checking system requirements..."
python3 -c "import torch, transformers, fasthtml, uvicorn, qwen_vl_utils" &> /dev/null
if [ $? -ne 0 ]; then
    echo "----------------------------------------------------"
    echo "NOTICE: Some required components are missing."
    echo "Installing now (this may take a minute)..."
    pip install -r requirements.txt > /dev/null
    echo "✓ Installation complete."
else
    echo "✓ System requirements met."
fi

# 3. Check for GPU / Model Capability
echo "Checking hardware capability..."
GPU_STATUS=$(python3 -c "import torch; print('CUDA' if torch.cuda.is_available() else 'CPU')")
if [ "$GPU_STATUS" == "CUDA" ]; then
    echo "✓ NVIDIA GPU detected. Model will run at high speed."
else
    echo "----------------------------------------------------"
    echo "WARNING: No NVIDIA GPU detected."
    echo "The model will run on your CPU, which will be SIGNIFICANTLY slower."
    echo "For the best experience, an NVIDIA GPU with 12GB+ VRAM is recommended."
    echo "----------------------------------------------------"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 4. Model Download Warning
# We check if the model is already in the cache (simplified check)
MODEL_DIR="$HOME/.cache/huggingface/hub/models--Qwen--Qwen2.5-VL-7B-Instruct"
if [ ! -d "$MODEL_DIR" ]; then
    echo ""
    echo "===================================================="
    echo "⚠️  FIRST-TIME SETUP: MODEL DOWNLOAD"
    echo "===================================================="
    echo "Ink2Pixel is about to download the Qwen2.5-VL model."
    echo "- Size: ~15 GB"
    echo "- Required Disk Space: ~20 GB"
    echo "- Time: 5-30 minutes (depending on your internet speed)"
    echo "----------------------------------------------------"
    read -p "Start download and launch? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Launch cancelled."
        exit 1
    fi
fi

echo ""
echo "Starting application..."
echo "Please wait, the first load takes a moment to initialize the VLM."
echo ""
echo ">>> Access the app at: http://localhost:8000"
echo "----------------------------------------------------"
python3 app.py
