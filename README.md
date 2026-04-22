# Ink2Pixel

**Transform Handwriting into Structured Digital Content with State-of-the-Art Vision Language Models.**

Ink2Pixel is a premium document digitization platform that bridges the gap between physical ink and digital pixels. Powered by the **Qwen2.5-VL** vision-language model, it accurately transcribes complex handwritten notes, mathematical formulas, and structured documents into clean, editable formats.

---

## ✨ Key Features

- **🧠 VLM-Powered Transcription**: Leverages Qwen2.5-VL for high-fidelity extraction of text and math, even from challenging handwriting.
- **🔢 Mathematical Excellence**: Native support for LaTeX math environments, ensuring formulas are preserved with academic precision.
- **📄 Multi-Format Export**: Digitized content can be exported as:
  - **Markdown** (`.md`)
  - **LaTeX** (`.tex`)
  - **HTML** (`.html`)
  - **JSON** (`.json`)
  - **Microsoft Word** (`.docx`)
- **⚡ Modern FastHTML Interface**: A responsive, high-performance web UI designed for speed and clarity.
- **📚 PDF Support**: Process multi-page documents with automatic page break handling.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+
- NVIDIA GPU (recommended for 4-bit quantization via `bitsandbytes`)
- [Pandoc](https://pandoc.org/) (required for `.docx` conversion)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
Choose the runner for your operating system:
- **macOS/Linux**: Double-click `run_app.sh` (or run `./run_app.sh` in terminal)
- **Windows**: Double-click `run_app.bat`

The app will be available at `http://localhost:8000`.

---

## 🛠️ Project Structure

- `app.py`: The main FastHTML application and web interface.
- `vlm/document_digitizer.py`: The core engine handling model loading and inference.
- `requirements.txt`: Project dependencies.
- `legacy/`: Historical preprocessing tools and experiments (kept for reference).

---

## 🏗️ Technology Stack

- **Core**: Python
- **Frontend**: [FastHTML](https://fasthtml.answer.ai/) & HTMX
- **VLM**: [Qwen2.5-VL-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct)
- **Deep Learning**: PyTorch & HuggingFace Transformers
- **Optimization**: BitsAndBytes (4-bit quantization)
- **Document Handling**: PyMuPDF & Pandoc

---

## 📝 License

This project is intended for research and personal digitization. Please refer to the Qwen2.5-VL model license for usage terms related to the underlying VLM.

---

*Ink2Pixel — Bridging the analog-digital divide.*