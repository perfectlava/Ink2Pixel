import uvicorn
import webbrowser
import shutil
import os
from threading import Timer
from web.core import app, UPLOAD_DIR, OUTPUT_DIR
# Import routes to register them with the app
import web.routes 

def open_browser():
    webbrowser.open("http://localhost:8000")

def cleanup():
    """Remove all files in the upload and output directories."""
    print("\nCleaning up temporary files...")
    for folder in [UPLOAD_DIR, OUTPUT_DIR]:
        if folder.exists():
            for filename in os.listdir(folder):
                file_path = folder / filename
                try:
                    if file_path.is_file() or file_path.is_symlink():
                        os.unlink(file_path)
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")

if __name__ == "__main__":
    Timer(1.5, open_browser).start()
    try:
        uvicorn.run(app, host='0.0.0.0', port=8000)
    finally:
        cleanup()