from .core import DocumentDigitizer, UPLOAD_DIR, OUTPUT_DIR, FORMAT_BY_KEY, FORMAT_BY_EXT
import asyncio, json, uuid
from pathlib import Path
from fasthtml.common import *

#  VLM INTEGRATION
# =============================================================================

_digitizer_instance = None

def get_digitizer():
    global _digitizer_instance
    if _digitizer_instance is None:
        print("Initializing VLM into VRAM... (This only happens once on the first upload)")
        _digitizer_instance = DocumentDigitizer()
    return _digitizer_instance

def run_vlm(upload_path: Path, output_type: str, output_path: Path) -> None:
    """Send the uploaded image to the VLM. The VLM writes its result to output_path."""
    
    # 1. Load the model lazily on the first request
    digitizer = get_digitizer()
    
    # 2. Map app.py's format names to document_digitizer's expected format codes
    format_mapping = {
        "markdown": "md",
        "html": "html",
        "json": "json",
        "clean_text": "txt",
        "latex": "latex"
    }
    target_format = format_mapping.get(output_type, "md")
    
    # 3. The digitizer's _export_document method automatically appends the file extension.
    # We need to strip the extension from output_path so we don't end up with file.md.md
    base_output_path = str(output_path.with_suffix(""))
    
    # 4. Run the inference and save
    digitizer.process_and_save(
        image_path=str(upload_path),
        output_path=base_output_path,
        output_format=target_format
    )


def serialize(value, key: str) -> str:
    """Turn a preview value into a display string (used for JSON previews)."""
    if value is None:
        return ""
    if key == "json":
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                return value
        return json.dumps(value, indent=2, ensure_ascii=False)
    return str(value)

def _render_preview_pane(key: str, value):
    """Render a single preview pane for the given format key."""
    if value is None:
        return Pre("(empty)")

    if key == "html":
        # Render the actual HTML. NOTE: trusts the VLM's output — fine for
        # a local tool, but sanitize with bleach if exposed publicly.
        return Div(NotStr(str(value)), cls="rendered-md")

    if key == "json":
        text = serialize(value, "json")
        return Pre(text)

    # markdown / clean_text / latex — show as preformatted source
    return Pre(str(value))
