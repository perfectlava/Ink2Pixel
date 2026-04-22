# Ink2Pixel

**Transform Handwriting into Structured Digital Content with State-of-the-Art Vision Language Models.**

Ink2Pixel is a premium document digitization platform that bridges the gap between physical ink and digital pixels. Powered by the **Qwen2.5-VL** vision-language model, it accurately transcribes complex handwritten notes, mathematical formulas, and structured documents into clean, editable formats.

---

## Key Features

- **VLM-Powered Transcription**: Leverages Qwen2.5-VL for high-fidelity extraction of text and math, even from challenging handwriting.
- **Mathematical Excellence**: Native support for LaTeX math environments, ensuring formulas are preserved with academic precision.
- **Multi-Format Export**: Digitized content can be exported as:
  - **Markdown** (`.md`)
  - **LaTeX** (`.tex`)
  - **HTML** (`.html`)
  - **JSON** (`.json`)
  - **Microsoft Word** (`.docx`)
- **Modern FastHTML Interface**: A responsive, high-performance web UI designed for speed and clarity.
- **PDF Support**: Process multi-page documents with automatic page break handling.

---

## Quick Start

### 1. System Requirements

Ink2Pixel runs locally on your machine. For optimal performance with the 7B VLM, we recommend the following:

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **GPU**   | NVIDIA (8GB VRAM) | NVIDIA (12GB+ VRAM) |
| **RAM**   | 16GB | 32GB |
| **OS**    | Windows / macOS / Linux | Windows 11 / macOS 14+ |

> [!IMPORTANT]
> **GPU Compatibility**: 
> - **NVIDIA**: Fully supported with 4-bit hardware acceleration via CUDA.
> - **Apple Silicon (M1/M2/M3)**: Supported via MPS, though quantization may vary. 16GB+ Unified Memory recommended.
> - **AMD**: Experimental. If ROCm is not configured, the system will default to CPU mode.
> - **CPU Fallback**: If no compatible GPU is detected, Ink2Pixel will run on your CPU. This is functional but significantly slower (several minutes per page).

### 2. Prerequisites
- Python 3.9+
- [Pandoc](https://pandoc.org/) (required for `.docx` conversion)

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Application
Choose the runner for your operating system:
- **macOS/Linux**: Double-click `run_app.sh`
- **Windows**: Double-click `run_app.bat`

**Privacy & Cleanup**: Your data never leaves your machine. For extra security, Ink2Pixel automatically deletes all files in the `uploads/` and `outputs/` folders whenever the application is closed.

**Automated Access**: Your default web browser will open automatically to `http://localhost:8000` once the server is ready.

---

## Project Structure

- `app.py`: The main FastHTML application and web interface.
- `vlm/document_digitizer.py`: The core engine handling model loading and inference.
- `requirements.txt`: Project dependencies.
- `legacy/`: Historical preprocessing tools and experiments (kept for reference).

---

## Technology Stack

- **Core**: Python
- **Frontend**: [FastHTML](https://fasthtml.answer.ai/) & HTMX
- **VLM**: [Qwen2.5-VL-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct)
- **Deep Learning**: PyTorch & HuggingFace Transformers
- **Optimization**: BitsAndBytes (4-bit quantization)
- **Document Handling**: PyMuPDF & Pandoc

---

## License

This project is intended for research and personal digitization. Please refer to the Qwen2.5-VL model license for usage terms related to the underlying VLM.

---

*Ink2Pixel — Bridging the analog-digital divide.*