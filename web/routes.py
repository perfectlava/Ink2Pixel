import re, json, uuid, asyncio
from pathlib import Path
from fasthtml.common import *
from .core import rt, UPLOAD_DIR, OUTPUT_DIR, FORMAT_BY_KEY, FORMAT_BY_EXT
from .vlm_logic import run_vlm, _render_preview_pane
from .ui_components import nav_bar, footer, home_content, upload_content

@rt("/static/{fname:path}")
def get(fname: str):
    from pathlib import Path
    p = Path("static") / fname
    if p.exists():
        return FileResponse(p)
    return Response("Not found", status_code=404)

@rt("/")
def get():
    hero, preview, mission, results = home_content()
    return Titled(
        "Ink2Pixel · StackHacks",
        Div(
            nav_bar("home"),
            hero,
            preview,
            mission,
            results,
            footer(),
            cls="page-shell",
        ),
    )

@rt("/upload")
def upload_page():
    upload_form, loader, dashboard = upload_content()
    return Titled(
        "Upload · Ink2Pixel",
        Div(
            nav_bar("upload"),
            Div(
                Div(Span(cls="pulse"), "Step One", cls="hero-eyebrow", style="margin-bottom:24px;"),
                H1(
                    Span("Upload", cls="t-ink"),
                    " ",
                    Span("your notes", style="font-style:normal; color:var(--yellow); font-weight:400;"),
                    ".",
                    cls="hero-title",
                    style="font-size:clamp(2.8rem, 6.5vw, 5rem); text-align:center;",
                ),
                P(
                    "Drop an image or PDF below. Toggle the beta VLM if your page is heavy on equations.",
                    cls="hero-sub",
                    style="text-align:center;",
                ),
                style="text-align:center; margin-bottom:12px;",
                cls="fade-up",
            ),
            dashboard,
            footer(),
            cls="page-shell",
        ),
    )

@rt("/process")
async def post(req, agree: str = "", fmt: str = "markdown"):
    if agree != "on":
        return Div(
            P(
                "✕  You must accept the liability warning before proceeding.",
                style="color:var(--yellow); text-align:center; font-family:'JetBrains Mono',monospace; letter-spacing:0.15em; margin:0;",
            ),
            cls="warning-box",
            style="margin-top:0;",
        )

    form = await req.form()

    # --- File ---
    up_file = form.get("up_file")
    if up_file is None or not getattr(up_file, "filename", ""):
        return Div(
            P("✕  No file received. Please choose an image and try again.",
              style="color:var(--yellow); text-align:center; font-family:'JetBrains Mono',monospace; letter-spacing:0.15em; margin:0;"),
            cls="warning-box", style="margin-top:0;",
        )

    # --- Format pick (radio — single value) ---
    chosen = form.get("fmt") or fmt
    if chosen not in FORMAT_BY_KEY:
        return Div(
            P("✕  Invalid output format selected.",
              style="color:var(--yellow); text-align:center; font-family:'JetBrains Mono',monospace; letter-spacing:0.15em; margin:0;"),
            cls="warning-box", style="margin-top:0;",
        )

    # --- Save upload ---
    doc_id = uuid.uuid4().hex[:12]
    file_ext = Path(up_file.filename).suffix.lower() or ".png"
    upload_path = UPLOAD_DIR / f"{doc_id}{file_ext}"
    content = await up_file.read()
    upload_path.write_bytes(content)

    # --- Build the destination path the VLM will write to ---
    _, out_ext, _ = FORMAT_BY_KEY[chosen]
    output_path = OUTPUT_DIR / f"{doc_id}.{out_ext}"

    # --- Call teammate's VLM: (upload_path, output_type, output_path) ---
    #     Their function writes the result file at output_path.
    try:
        await asyncio.to_thread(run_vlm, upload_path, chosen, output_path)
    except Exception as e:
        return Div(
            Div("✕  VLM call failed",
                style="color:var(--yellow); font-family:'JetBrains Mono',monospace; letter-spacing:0.2em; font-weight:700; margin-bottom:10px;"),
            P(f"{type(e).__name__}: {e}",
              style="color:var(--ink-soft); white-space:pre-wrap; font-family:'JetBrains Mono',monospace; font-size:0.82rem; margin:0;"),
            cls="warning-box", style="margin-top:0;",
        )

    # --- Confirm the VLM actually wrote something ---
    if not output_path.exists() or output_path.stat().st_size == 0:
        return Div(
            P("✕  The VLM did not produce an output file. Check the VLM's output_path handling.",
              style="color:var(--yellow); text-align:center; font-family:'JetBrains Mono',monospace; letter-spacing:0.15em; margin:0;"),
            cls="warning-box", style="margin-top:0;",
        )

    # --- Read the file back for inline preview ---
    vlm_output = output_path.read_text(encoding="utf-8")

    # For JSON, parse it so the preview pretty-prints nicely
    if chosen == "json":
        try:
            vlm_output = json.loads(vlm_output)
        except json.JSONDecodeError:
            pass  # leave as raw string, preview will show it

    fmt_label, fmt_ext, _ = FORMAT_BY_KEY[chosen]

    # --- Preview pane ---
    preview = _render_preview_pane(chosen, vlm_output)

    return Div(
        Div("PROCESSED · OK", cls="result-stamp"),
        H2("Your page is ", Em("ready"), ".", cls="result-title"),
        P(
            f"Output generated as ",
            Span(f".{fmt_ext}", style="color:var(--yellow); font-family:'JetBrains Mono',monospace; font-weight:700;"),
            ". Preview below, then download.",
            cls="result-sub",
        ),

        Div(
            Div(
                Span(f"PREVIEW · {fmt_label.upper()}",
                     style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; letter-spacing:0.22em; color:var(--yellow); font-weight:700;"),
                Span(f".{fmt_ext}",
                     style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; letter-spacing:0.15em; color:var(--ink-mute); margin-left:auto;"),
                style="display:flex; align-items:center; padding:14px 20px; background:var(--bg-2); border-bottom:1px solid var(--hair);",
            ),
            Div(preview, cls="preview-pane active"),
            cls="preview-panel",
        ),

        Div(
            A(
                Span("↓", cls="ext"),
                f"Download .{fmt_ext}",
                href=f"/download/{doc_id}/{fmt_ext}",
                download=f"ink2pixel_{doc_id}.{fmt_ext}",
                cls="btn-dl",
            ),
            cls="dl-row",
        ),
        Div(
            A("↺  Upload another page", href="/upload", cls="upload-again"),
            style="text-align:center;",
        ),
        cls="result-card",
    )

@rt("/download/{doc_id}/{fmt}")
def get(doc_id: str, fmt: str):
    if fmt not in FORMAT_BY_EXT:
        return Response("Unsupported format", status_code=400)

    # Guard against path traversal — doc_id should be hex only
    if not re.fullmatch(r"[a-f0-9]{6,32}", doc_id):
        return Response("Invalid doc id", status_code=400)

    path = OUTPUT_DIR / f"{doc_id}.{fmt}"
    if not path.exists():
        return Response("File expired or not found", status_code=404)

    _, _, media = FORMAT_BY_EXT[fmt]
    headers = {"Content-Disposition": f'attachment; filename="ink2pixel_{doc_id}.{fmt}"'}
    return Response(path.read_bytes(), headers=headers, media_type=media)
