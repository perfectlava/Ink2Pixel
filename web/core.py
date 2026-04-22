from fasthtml.common import *
import asyncio
import os
import json
import uuid
# import html as html_lib
import re
from pathlib import Path
from vlm.document_digitizer import DocumentDigitizer


# ---------- Storage paths ----------
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Supported formats — (key, label, file extension, media type)
FORMATS = [
    ("markdown",   "Markdown",   "md",    "text/markdown; charset=utf-8"),
    ("html",       "HTML",       "html",  "text/html; charset=utf-8"),
    ("json",       "JSON",       "json",  "application/json; charset=utf-8"),
    ("clean_text", "Clean text", "txt",   "text/plain; charset=utf-8"),
    ("latex",      "Raw LaTeX",  "tex",   "text/plain; charset=utf-8"),
]
FORMAT_BY_KEY = {k: (label, ext, media) for k, label, ext, media in FORMATS}
FORMAT_BY_EXT = {ext: (k, label, media) for k, label, ext, media in FORMATS}


from .styles import fonts, css
app, rt = fast_app(hdrs=(fonts, css))