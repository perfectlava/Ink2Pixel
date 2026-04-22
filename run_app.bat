@echo off
title Ink2Pixel Runner
setlocal enabledelayedexpansion

:: Navigate to script directory
cd /d "%~dp0"

cls
echo ====================================================
echo           INK2PIXEL: DOCUMENT DIGITIZER             
echo ====================================================
echo.

:: 1. Check for virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

:: 2. Check Dependencies
echo Checking system requirements...
python -c "import torch, transformers, fasthtml, uvicorn, qwen_vl_utils" >nul 2>&1
if %errorlevel% neq 0 (
    echo ----------------------------------------------------
    echo NOTICE: Some required components are missing.
    echo Installing now (this may take a minute)...
    pip install -r requirements.txt >nul 2>&1
    echo [OK] Installation complete.
) else (
    echo [OK] System requirements met.
)

:: 3. Check for GPU
echo Checking hardware capability...
python -c "import torch; exit(0 if torch.cuda.is_available() else 1)" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] NVIDIA GPU detected. Model will run at high speed.
) else (
    echo ----------------------------------------------------
    echo WARNING: No NVIDIA GPU detected.
    echo The model will run on your CPU, which will be SIGNIFICANTLY slower.
    echo For the best experience, an NVIDIA GPU with 12GB+ VRAM is recommended.
    echo ----------------------------------------------------
    set /p choice="Continue anyway? (y/n): "
    if /i "!choice!" neq "y" exit /b 1
)

:: 4. Model Download Warning
:: Approximate path for Windows HF cache
set MODEL_DIR=%USERPROFILE%\.cache\huggingface\hub\models--Qwen--Qwen2.5-VL-7B-Instruct
if not exist "%MODEL_DIR%" (
    echo.
    echo ====================================================
    echo ^^!  FIRST-TIME SETUP: MODEL DOWNLOAD
    echo ====================================================
    echo Ink2Pixel is about to download the Qwen2.5-VL model.
    echo - Size: ~15 GB
    echo - Required Disk Space: ~20 GB
    echo - Time: 5-30 minutes (depending on your internet speed)
    echo ----------------------------------------------------
    set /p download="Start download and launch? (y/n): "
    if /i "!download!" neq "y" (
        echo Launch cancelled.
        pause
        exit /b 1
    )
)

echo.
echo Starting application...
echo Please wait, the first load takes a moment to initialize the VLM.
echo.
echo ^>^>^> Access the app at: http://localhost:8000
echo ----------------------------------------------------
python app.py

if %errorlevel% neq 0 (
    echo.
    echo Application crashed or failed to start.
    pause
)
