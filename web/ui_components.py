from fasthtml.common import *
from .vlm_logic import serialize

def nav_bar(active: str = "home"):
    return Div(
    A(
        Span("SH", cls="mark"),
        Span(
            Span("Ink", cls="txt"),
            Span("2", cls="two"),
            Span("Pixel", cls="txt"),
        ),
        href="/",
        cls="nav-brand",
    ),
    Div(
        A("Home",   href="/",       cls=("active" if active == "home"   else "")),
        A("Upload", href="/upload", cls=("active" if active == "upload" else "")),
        A("Docs",   href="#"),
        A("GitHub", href="#"),
        A("Upload ↗", href="/upload", cls="nav-cta"),
        cls="nav-links",
    ),
    cls="nav",
    )


def footer():
    return Div(
    Div(
        Span("A ", cls="by"),
        Span("StackHacks", cls="brand"),
        Span(" project · v0.4", cls="by"),
    ),
    Span("Local-first · Open source · 2026"),
    cls="foot",
    )


def home_content():
    hero = Div(
        Div(Span("EST · 2026", cls="acc"), " · VER. 0.4 · STACKHACKS", cls="hero-stamp"),
        Div(
            Div(Span(cls="pulse"), "A Notebook, Translated", cls="hero-eyebrow"),
            H1(
                Span("Ink", cls="t-ink"),
                Span("2", cls="t-two"),
                Span("Pixel", cls="t-pix"),
                cls="hero-title",
            ),
            P(
                "Hand-drawn equations, margin scribbles, and messy proofs — rendered into ",
                Span("clean, typeset LaTeX", cls="hl"),
                " without ever leaving your machine.",
                cls="hero-sub",
            ),
            Div(
                Span(Span(cls="dot"), "100% Local"),
                Span(Span(cls="dot"), "OpenCV + EasyOCR"),
                Span(Span(cls="dot"), "LaTeX Output"),
                Span(Span(cls="dot"), "Beta VLM"),
                cls="hero-meta",
            ),
            cls="hero-center fade-up",
        ),
        Div("HANDWRITING", Br(), "↓", Br(), "TYPESET", cls="hero-stamp right"),
        cls="hero",
    )
    
    preview = Div(
        Div(
            Div("Input ", Span("· 001", cls="num"), " · handwritten", cls="preview-label"),
            Div(
                "Prove that for all n ∈ ℕ,",
                Br(),
                Span("∑ₖ₌₁ⁿ k  =  n(n+1)/2", cls="eq"),
                cls="scrawl",
            ),
            cls="preview-side ink",
        ),
        Div("⇢", cls="preview-arrow"),
        Div(
            Div("Output ", Span("· 001", cls="num"), " · typeset", cls="preview-label"),
            Div(
                Span("Theorem. ", style="color:var(--yellow);"),
                Em("For all n ∈ ℕ:"),
                Br(),
                Span(r"\sum_{k=1}^{n} k = \frac{n(n+1)}{2}", cls="tex"),
                cls="rendered",
            ),
            cls="preview-side pix",
        ),
        cls="preview fade-up d2",
    )
    
    mission = Div(
        Div(Span("01", cls="num"), " / About", cls="section-label"),
        H2(
            "The margin is where ",
            Em("thinking"),
            " happens — but it rarely survives the jump to a document.",
            cls="section-title",
        ),
        Div(
            Div(
                H3("Mission"),
                P(
                    "To bridge the gap between physical handwriting and digital workflows ",
                    Em("without"),
                    " losing the context of complex mathematics.",
                    cls="big-quote",
                ),
                cls="manuscript-col",
            ),
            Div(
                H3("Vision"),
                P(
                    "A world where students, researchers, and engineers never have to manually type out a long ",
                    Em("LaTeX equation"),
                    " again.",
                    cls="big-quote",
                ),
                cls="manuscript-col",
            ),
            cls="manuscript",
        ),
    
        # --- Team block ---
        Div(
            # Photo side. If /static/team_photo.jpg is missing the placeholder shows
            # — swap it out by dropping your own file in that path.
            Div(
                Img(
                    src="/static/team_photo.jpg",
                    alt="The StackHacks team at work",
                    onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';",
                ),
                Div(
                    Span("◆", cls="icon"),
                    Span("Team photo"),
                    Span("/static/team_photo.jpg", style="color:var(--ink-dim); font-size:0.62rem;"),
                    cls="team-photo-placeholder",
                    style="display:none;",
                ),
                Div(
                    Span(Span("📍 ", cls="loc"), "StackHacks HQ"),
                    Span("· 2026 ·"),
                    cls="team-photo-caption",
                ),
                cls="team-photo-frame",
            ),
            # Copy side
            Div(
                H3("About the team"),
                P(
                    "Ink2Pixel is built by ",
                    Em("StackHacks"),
                    " — a small team of engineers who got tired of retyping their own handwriting.",
                    cls="team-lede",
                ),
                P(
                    "We started this during a weekend hackathon after watching a friend spend four hours "
                    "converting a single page of scratch-paper proofs into LaTeX. There had to be a better way — "
                    "one that didn't ship your private notes off to someone else's server. So we built it.",
                    cls="team-body",
                ),
                Ul(
                    Li(
                        Span("01", cls="tag"),
                        Span("— The Team —", cls="name"),
                        Span("StackHacks", cls="role"),
                    ),
                    Li(
                        Span("02", cls="tag"),
                        Span("Computer Vision", cls="name"),
                        Span("OpenCV · EasyOCR", cls="role"),
                    ),
                    Li(
                        Span("03", cls="tag"),
                        Span("Math Detection", cls="name"),
                        Span("VLM · Classifier", cls="role"),
                    ),
                    Li(
                        Span("04", cls="tag"),
                        Span("Frontend & UX", cls="name"),
                        Span("FastHTML · HTMX", cls="role"),
                    ),
                    cls="team-roster",
                ),
                cls="team-copy",
            ),
            cls="team-wrap",
            style="margin-top: 56px;",
        ),
    
        cls="section fade-up d3",
    )
    
    # --- Results Preview: before / after ---
    results = Div(
        Div(Span("02", cls="num"), " / Results", cls="section-label"),
        H2("From ", Em("ink"), " to ", Em("pixel"), " — a real page, converted.", cls="section-title"),
        P(
            "Here's what Ink2Pixel does with a single handwritten page. Left: the original scan. "
            "Right: the reconstructed .docx output, layout and equations intact.",
            cls="section-text",
        ),
    
        Div(
            # BEFORE — handwritten scan
            Div(
                Div(
                    Span(Span("01", cls="num"), " ", "Input"),
                    Span("IMG · 2.4MB", cls="fmt"),
                    cls="result-page-head",
                ),
                Div(
                    Div(
                        Span("Proof — Sum of first n", cls="title"),
                        "Claim: for all ", Span("n ∈ ℕ", cls="eq"), ",", Br(),
                        Br(),
                        Span("∑ₖ₌₁ⁿ k  =  n(n+1)/2", cls="eq"), Br(),
                        Br(),
                        "Proof by induction.", Br(),
                        Span("Base: n = 0, LHS = 0 ✓", cls="note"), Br(),
                        Br(),
                        "Inductive step — assume true", Br(),
                        "for ", Span("n", cls="eq"), ". Then", Br(),
                        Br(),
                        Span("∑ₖ₌₁ⁿ⁺¹ k = (n+1)(n+2)/2", cls="eq"), Br(),
                        Br(),
                        Span("by algebra", cls="note"),
                        " ", Span("→", cls="arrow"), " ",
                        Span("QED", cls="note"),
                        cls="hw",
                    ),
                    cls="result-page-body",
                ),
                cls="result-page scan",
            ),
            # AFTER — rendered .docx
            Div(
                Div(
                    Span(Span("02", cls="num"), " ", "Output"),
                    Span(".DOCX · 18KB", cls="fmt"),
                    cls="result-page-head",
                ),
                Div(
                    Div(
                        H4("Proof — Sum of the First n Naturals"),
                        P(Span("Claim. ", cls="theorem"), "For all n ∈ ℕ,"),
                        Span("∑ₖ₌₁ⁿ k = n(n+1) / 2", Span("(1)", cls="num"), cls="eqline"),
                        P(Span("Proof. ", cls="proof-label"), "By induction on n."),
                        P(Span("Base case (n = 0). ", cls="theorem"),
                          "The left-hand side is the empty sum, which equals 0. "
                          "The right-hand side equals 0. ✓"),
                        P(Span("Inductive step. ", cls="theorem"),
                          "Assume (1) holds for some n. Then"),
                        Span("∑ₖ₌₁ⁿ⁺¹ k = (n+1)(n+2) / 2", Span("(2)", cls="num"), cls="eqline"),
                        P("follows by algebra, completing the induction.", Span(cls="qed")),
                        cls="docx-doc",
                    ),
                    cls="result-page-body",
                ),
                cls="result-page docx",
            ),
            cls="results-stack",
        ),
    
        Div(
            Span(Span(cls="ok"), "✓ Layout preserved"),
            Span(Span(cls="ok"), "✓ Equations typeset"),
            Span(Span(cls="ok"), "✓ Processed in 3.1s"),
            Span(Span(cls="ok"), "✓ 100% local"),
            cls="results-meta",
        ),
    
        # CTA tail
        Div(
            A("Try it with your own page  →", href="/upload", cls="cta-btn"),
            style="text-align:center; margin-top: 40px;",
        ),
    
        cls="section fade-up d4",
    )
    return hero, preview, mission, results

def upload_content():
    upload_form = Form(
        Div(
            Label(
                Span("↑  DROP FILE HERE", cls="ico"),
                "Click, or drag a page to translate",
                Span("IMG · JPG · PNG · ≤ 25 MB", cls="hint"),
                Input(
                    type="file",
                    name="up_file",
                    accept="image/*",
                    required=True,
                    style="display:none;",
                ),
                style="cursor:pointer; display:block; width:100%;",
            ),
            cls="upload-zone",
        ),
        Div(
            Div("Choose your output format", cls="format-picker-label"),
            P("Pick one. The VLM will generate your page in this format.",
              cls="format-picker-hint"),
            Div(
                Label(
                    Input(type="radio", name="fmt", value="markdown", checked=True),
                    Div(
                        Span(cls="check"),
                        Span("Markdown", cls="name"),
                        Span(".md", cls="ext"),
                        cls="box",
                    ),
                    cls="fmt-opt",
                ),
                Label(
                    Input(type="radio", name="fmt", value="html"),
                    Div(
                        Span(cls="check"),
                        Span("HTML", cls="name"),
                        Span(".html", cls="ext"),
                        cls="box",
                    ),
                    cls="fmt-opt",
                ),
                Label(
                    Input(type="radio", name="fmt", value="json"),
                    Div(
                        Span(cls="check"),
                        Span("JSON", cls="name"),
                        Span(".json", cls="ext"),
                        cls="box",
                    ),
                    cls="fmt-opt",
                ),
                Label(
                    Input(type="radio", name="fmt", value="clean_text"),
                    Div(
                        Span(cls="check"),
                        Span("Clean text", cls="name"),
                        Span(".txt", cls="ext"),
                        cls="box",
                    ),
                    cls="fmt-opt",
                ),
                Label(
                    Input(type="radio", name="fmt", value="latex"),
                    Div(
                        Span(cls="check"),
                        Span("Raw LaTeX", cls="name"),
                        Span(".tex", cls="ext"),
                        cls="box",
                    ),
                    cls="fmt-opt",
                ),
                cls="format-grid",
            ),
            cls="format-picker",
        ),
        Div(
            P(
                "Experimental tool — Results may vary, "
                "and the VLM path is still learning its way around unusual notation."
            ),
            cls="warning-box",
        ),
        Div(
            Input(type="checkbox", name="agree", required=True, id="agree"),
            Label("I understand and accept the risks", for_="agree"),
            cls="agreement-box",
        ),
        Button("Process Document", type="submit", cls="btn-primary"),
        hx_post="/process",
        hx_target="#dashboard",
        hx_swap="innerHTML",
        hx_indicator="#indicator",
        hx_encoding="multipart/form-data",
    )
    
    loader = Div(
        Div(Span(), Span(), Span(), Span(), cls="skeleton-lines"),
        P("Qwen2.5-VL is reading the page…", cls="loader-text"),
        id="indicator",
        cls="htmx-indicator loader-wrap",
    )
    
    dashboard = Div(upload_form, loader, id="dashboard", cls="upload-frame")
    return upload_form, loader, dashboard