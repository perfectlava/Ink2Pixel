from fasthtml.common import *
import asyncio

css = Style("""
    body { background-color: #fcebeb; font-family: system-ui, -apple-system, sans-serif; color: #333; margin: 0; padding: 2rem; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); min-height: 100vh;}
    .container-custom { max-width: 900px; margin: 0 auto; }
    .hero-title {
        background: linear-gradient(45deg, #FF6B6B, #FF8E53, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0px 4px 15px rgba(255, 107, 107, 0.2);
    }
    .hero-subtitle { text-align: center; color: #555; font-size: 1.2rem; margin-bottom: 2.5rem; }
    .card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px; padding: 2.5rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.05); margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.4);
    }
    .mission-vision {
        background: linear-gradient(135deg, rgba(255,107,107,0.1) 0%, rgba(78,205,196,0.1) 100%);
        border-left: 6px solid #FF6B6B;
    }
    .benefits-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; }
    .benefit-item {
        padding: 1.5rem; border-radius: 16px;
        background: linear-gradient(to bottom right, #ffffff, #f0fbfa);
        border: 1px solid #e0f2f1;
        box-shadow: 0 8px 20px rgba(0,0,0,0.04);
        transition: transform 0.3s;
    }
    .benefit-item:hover { transform: translateY(-5px); }
    .benefit-item h3 { color: #FF6B6B; margin-bottom: 0.8rem; font-size: 1.3rem; }
    .upload-zone {
        border: 3px dashed #4ECDC4; padding: 4rem 2rem; text-align: center;
        border-radius: 20px; margin-bottom: 1.5rem; background: rgba(78,205,196,0.05);
        transition: all 0.3s ease; cursor: pointer; color: #4ECDC4; font-weight: bold;
    }
    .upload-zone:hover { background: rgba(78,205,196,0.15); border-color: #FF6B6B; color: #FF6B6B; }
    .btn-primary { 
        background: linear-gradient(45deg, #FF6B6B, #FF8E53); 
        color: white; border: none; padding: 1.2rem 2rem; font-size: 1.2rem; 
        border-radius: 30px; cursor: pointer; font-weight: bold; width: 100%; transition: all 0.3s; 
        box-shadow: 0 8px 20px rgba(255, 107, 107, 0.4);
    }
    .btn-primary:hover { transform: scale(1.02); box-shadow: 0 12px 25px rgba(255, 107, 107, 0.5); }
    .btn-dl-docx { background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%); color: white; border: none; padding: 1rem 1.5rem; border-radius: 12px; cursor: pointer; font-weight: bold; box-shadow: 0 5px 15px rgba(67, 206, 162, 0.4); text-decoration: none; display: inline-block; transition: transform 0.2s;}
    .btn-dl-docx:hover { transform: translateY(-2px); }
    .btn-dl-txt { background: linear-gradient(135deg, #ff9966 0%, #ff5e62 100%); color: white; border: none; padding: 1rem 1.5rem; border-radius: 12px; cursor: pointer; font-weight: bold; box-shadow: 0 5px 15px rgba(255, 153, 102, 0.4); text-decoration: none; display: inline-block; transition: transform 0.2s; margin-left: 1rem;}
    .btn-dl-txt:hover { transform: translateY(-2px); }
    
    .switch-container { display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 2rem; font-weight: 600; color: #444; background: white; padding: 1rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .switch-container input[type="checkbox"] { width: 24px; height: 24px; accent-color: #FF6B6B; cursor: pointer; }

    .skeleton-colorful { animation: pulseBg 1.5s infinite; height: 120px; border-radius: 20px; margin-bottom: 1rem; }
    @keyframes pulseBg { 0% { background: #FF6B6B; opacity: 0.2; } 50% { background: #4ECDC4; opacity: 0.5; } 100% { background: #FF6B6B; opacity: 0.2; } }
    .loader-text { font-size: 1.2rem; font-weight: bold; background: linear-gradient(45deg, #FF6B6B, #4ECDC4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center;}

    .htmx-indicator { display: none; }
    .htmx-request .htmx-indicator { display: block; }
    .htmx-request.htmx-indicator { display: block; }
    .htmx-request.upload-form { display: none; }
""")

app, rt = fast_app(hdrs=(css,))

@rt("/")
def get():
    hero = Div(
        H1("Ink2Pixel", cls="hero-title"),
        P("Bring your handwritten math notes to life.", cls="hero-subtitle")
    )

    mission = Div(
        H2("Our Mission & Vision", style="color: #FF6B6B; margin-top: 0;"),
        P(B("Mission: "), "To bridge the gap between physical handwriting and digital workflows without losing the context of complex math."),
        P(B("Vision: "), "A world where students, researchers, and professionals never have to manually type out a long LaTeX equation again."),
        cls="card mission-vision"
    )

    benefits = Div(
        Div(
            H3("Privacy First"),
            P("100% local processing; your notes never leave your machine."),
            cls="benefit-item"
        ),
        Div(
            H3("Layout Preservation"),
            P("OpenCV ensures your digital file looks just like your original page."),
            cls="benefit-item"
        ),
        Div(
            H3("Smart Math Detection"),
            P("Seamlessly converts scribbles into perfect LaTeX equations."),
            cls="benefit-item"
        ),
        cls="benefits-grid",
        style="margin-bottom: 2.5rem;"
    )

    upload_form = Form(
        Div(
            Label("Click or Drag & Drop File Here", 
                Input(type="file", name="up_file", accept="image/*,application/pdf", required=True, style="display:none;"),
                style="cursor: pointer; display: block; width: 100%; height: 100%;"
            ),
            cls="upload-zone"
        ),
        Div(
            Input(type="checkbox", name="vlm_toggle", value="true", id="vlm-toggle"),
            Label("Enable Advanced Math Detection (Beta VLM)", for_="vlm-toggle"),
            cls="switch-container"
        ),
        Button("Process Document ✨", type="submit", cls="btn-primary"),
        hx_post="/process",
        hx_target="#dashboard",
        hx_swap="innerHTML",
        hx_indicator="#indicator",
        hx_encoding="multipart/form-data",
        cls="upload-form"
    )

    loader = Div(
        Div(cls="skeleton-colorful"),
        P("AI is weaving its magic... please wait!", cls="loader-text"),
        id="indicator",
        cls="htmx-indicator"
    )

    dashboard = Div(
        upload_form,
        loader,
        id="dashboard",
        cls="card"
    )

    return Titled("Ink2Pixel",
        Div(
            hero,
            mission,
            benefits,
            dashboard,
            cls="container-custom"
        )
    )

@rt("/process")
async def post(req, vlm_toggle: bool = False):
    # 1. Image Pre-processing
    # TODO: Inject OpenCV contour logic here
    await asyncio.sleep(1)
    
    # 2. Detection & Routing
    # TODO: Custom classifier logic here
    await asyncio.sleep(0.5)
    
    # 3. Core Text OCR
    # TODO: Call EasyOCR here
    await asyncio.sleep(1.5)
    
    # 4. Math Detection (Beta VLM)
    if vlm_toggle:
        # TODO: Dynamically load the VLM into memory
        # model_instance = load_model()
        
        # Simulate heavy VLM processing
        await asyncio.sleep(2)
        
        # TODO: Delete the model from memory explicitly
        # del model_instance
    
    # 5. Reconstruction
    # TODO: Output a clean .docx or .txt file using OpenCV contours
    await asyncio.sleep(0.5)
    
    # Generate mock result files
    doc_id = "mock_doc_id"
    
    return Div(
        H2("✨ Processing Complete!", style="color: #4ECDC4; text-align: center; margin-bottom: 1rem;"),
        P("Your document has been successfully processed and reconstructed. It's ready to download!", style="text-align: center; margin-bottom: 2rem; color: #555;"),
        Div(
            A("Download .docx", href=f"/download/{doc_id}/docx", download="result.docx", cls="btn-dl-docx"),
            A("Download .txt", href=f"/download/{doc_id}/txt", download="result.txt", cls="btn-dl-txt"),
            style="display: flex; justify-content: center; gap: 15px;"
        ),
        Div(
            A("Upload Another File", href="/", style="display: block; text-align: center; margin-top: 2rem; color: #FF6B6B; text-decoration: none; font-weight: bold;")
        )
    )

@rt("/download/{doc_id}/{format}")
def get(doc_id: str, format: str):
    # Mock download endpoint
    content = "Mock file content. Real implementation will generate actual file bytes."
    headers = {"Content-Disposition": f'attachment; filename="result_{doc_id}.{format}"'}
    return Response(content, headers=headers, media_type="text/plain")

if __name__ == "__main__":
    serve()
