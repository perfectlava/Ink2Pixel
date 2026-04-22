from fasthtml.common import *

# ---------- Fonts ----------
# Display: Fraunces (characterful serif with excellent italic)
# Mono: JetBrains Mono (technical, matches the "pixel" side)
# Body: Inter Tight (clean, slightly condensed)
# Handwriting: Caveat (for the demo preview only)
fonts = Link(
    rel="stylesheet",
    href=(
        "https://fonts.googleapis.com/css2?"
        "family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,800;0,9..144,900;1,9..144,400;1,9..144,600;1,9..144,800&"
        "family=Inter+Tight:wght@400;500;600;700&"
        "family=JetBrains+Mono:wght@400;500;700&"
        "family=Caveat:wght@400;600&"
        "display=swap"
    ),
)

css = Style(r"""
    :root {
        --bg:         #0a0a0a;
        --bg-2:       #111111;
        --bg-3:       #161616;
        --hair:       rgba(255,255,255,0.08);
        --hair-2:     rgba(255,255,255,0.14);
        --ink:        #f5f5f5;
        --ink-soft:   #c8c8c8;
        --ink-mute:   #8a8a8a;
        --ink-dim:    #555555;
        --yellow:     #FFD60A;
        --yellow-dim: #d4b008;
        --yellow-soft:rgba(255,214,10,0.12);
    }

    * { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; }

    body {
        font-family: 'Inter Tight', system-ui, sans-serif;
        color: var(--ink);
        background: var(--bg);
        min-height: 100vh;
        overflow-x: hidden;
        background-image:
            radial-gradient(ellipse 80% 50% at 50% -10%, rgba(255,214,10,0.08), transparent 60%),
            radial-gradient(ellipse 60% 40% at 100% 100%, rgba(255,214,10,0.04), transparent 60%),
            linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
        background-size: auto, auto, 40px 40px, 40px 40px;
        background-attachment: fixed;
    }

    /* Yellow vertical rule (echoes logo split bar) */
    body::before {
        content: "";
        position: fixed;
        top: 0; bottom: 0;
        left: 72px;
        width: 1px;
        background: linear-gradient(to bottom,
            transparent 0%,
            rgba(255,214,10,0.35) 15%,
            rgba(255,214,10,0.35) 85%,
            transparent 100%);
        pointer-events: none;
        z-index: 0;
    }
    @media (max-width: 820px) { body::before { left: 20px; } }

    .page-shell {
        position: relative;
        z-index: 1;
        padding: 28px 32px 80px;
        max-width: 1120px;
        margin: 0 auto;
    }

    /* ---------- Nav ---------- */
    .nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 88px;
        padding-bottom: 20px;
        border-bottom: 1px solid var(--hair);
    }
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: 'Fraunces', serif;
        font-weight: 900;
        font-size: 1.25rem;
        letter-spacing: -0.02em;
        color: var(--ink);
        text-decoration: none;
    }
    .nav-brand .mark {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 26px; height: 26px;
        background: var(--yellow);
        color: var(--bg);
        border-radius: 2px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
    }
    .nav-brand .txt { font-style: italic; }
    .nav-brand .two { color: var(--yellow); font-style: normal; }

    .nav-links { display: flex; gap: 32px; align-items: center; }
    .nav-links a {
        color: var(--ink-soft);
        text-decoration: none;
        font-size: 0.88rem;
        font-weight: 500;
        position: relative;
        padding: 6px 0;
        transition: color .2s ease;
    }
    .nav-links a:hover { color: var(--ink); }
    .nav-links a::after {
        content: "";
        position: absolute;
        left: 0; right: 0; bottom: 0;
        height: 2px;
        background: var(--yellow);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform .25s ease;
    }
    .nav-links a:hover::after,
    .nav-links a.active::after { transform: scaleX(1); }
    .nav-links a.active { color: var(--ink); }

    .nav-cta {
        padding: 9px 16px;
        background: var(--yellow);
        color: var(--bg) !important;
        border-radius: 2px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    .nav-cta::after { display: none !important; }
    .nav-cta:hover { background: #fff; }

    /* ---------- Hero ---------- */
    .hero {
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        align-items: center;
        gap: 24px;
        margin-bottom: 24px;
        min-height: 60vh;
    }
    .hero-stamp {
        justify-self: end;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: var(--ink-mute);
        text-transform: uppercase;
        letter-spacing: 0.28em;
        writing-mode: vertical-rl;
        transform: rotate(180deg);
        border-left: 1px solid var(--hair-2);
        padding: 12px 0 12px 12px;
    }
    .hero-stamp.right {
        justify-self: start;
        transform: none;
        border-left: none;
        border-right: 1px solid var(--hair-2);
        padding: 12px 12px 12px 0;
    }
    .hero-stamp .acc { color: var(--yellow); }

    .hero-center { text-align: center; }

    .hero-eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--yellow);
        letter-spacing: 0.3em;
        text-transform: uppercase;
        margin-bottom: 28px;
        padding: 8px 14px;
        border: 1px solid var(--yellow-dim);
        border-radius: 2px;
        background: var(--yellow-soft);
    }
    .hero-eyebrow .pulse {
        width: 6px; height: 6px;
        border-radius: 50%;
        background: var(--yellow);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%   { box-shadow: 0 0 0 0 rgba(255,214,10,0.6); }
        70%  { box-shadow: 0 0 0 10px rgba(255,214,10,0); }
        100% { box-shadow: 0 0 0 0 rgba(255,214,10,0); }
    }

    .hero-title {
        font-family: 'Fraunces', serif;
        font-weight: 900;
        font-size: clamp(3.4rem, 9vw, 7.5rem);
        line-height: 0.9;
        letter-spacing: -0.05em;
        margin: 0;
    }
    .hero-title .t-ink { font-style: italic; }
    .hero-title .t-two {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 0.5em;
        font-style: normal;
        vertical-align: 0.28em;
        margin: 0 0.12em;
        color: var(--yellow);
        letter-spacing: 0;
    }
    .hero-title .t-pix {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 0.68em;
        letter-spacing: -0.02em;
        background: var(--yellow);
        color: var(--bg);
        padding: 0.06em 0.22em 0.12em;
        border-radius: 6px;
        display: inline-block;
        transform: translateY(-0.06em);
        box-shadow: 0 0 0 1px rgba(255,214,10,0.4), 0 20px 60px -10px rgba(255,214,10,0.35);
    }

    .hero-sub {
        font-family: 'Fraunces', serif;
        font-style: italic;
        font-size: clamp(1.1rem, 1.7vw, 1.35rem);
        color: var(--ink-soft);
        max-width: 620px;
        margin: 32px auto 0;
        line-height: 1.5;
    }
    .hero-sub .hl {
        font-style: normal;
        font-family: 'Inter Tight', sans-serif;
        font-weight: 500;
        color: var(--yellow);
    }

    .hero-meta {
        display: inline-flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 14px;
        margin-top: 36px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--ink-mute);
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }
    .hero-meta span {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 7px 12px;
        border: 1px solid var(--hair);
        border-radius: 999px;
        background: var(--bg-2);
    }
    .hero-meta .dot {
        width: 6px; height: 6px; border-radius: 50%;
        background: var(--yellow);
    }

    /* ---------- Preview ---------- */
    .preview {
        margin-top: 64px;
        display: grid;
        grid-template-columns: 1fr 56px 1fr;
        border: 1px solid var(--hair-2);
        border-radius: 4px;
        overflow: hidden;
        min-height: 280px;
        background: var(--bg-2);
        position: relative;
    }
    .preview::before {
        content: "SPECIMEN · 001";
        position: absolute;
        top: -11px; left: 28px;
        background: var(--yellow);
        color: var(--bg);
        padding: 3px 12px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.28em;
        z-index: 2;
    }
    .preview-side {
        padding: 42px 36px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .preview-side.ink {
        background:
            repeating-linear-gradient(to bottom,
                transparent 0, transparent 27px,
                rgba(255,255,255,0.04) 27px, rgba(255,255,255,0.04) 28px),
            var(--bg-2);
    }
    .preview-side.pix {
        background: var(--bg-3);
        background-image:
            linear-gradient(rgba(255,214,10,0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,214,10,0.05) 1px, transparent 1px);
        background-size: 20px 20px;
    }
    .preview-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.28em;
        text-transform: uppercase;
        color: var(--ink-mute);
        margin-bottom: 18px;
    }
    .preview-label .num { color: var(--yellow); }

    .scrawl {
        font-family: 'Caveat', cursive;
        font-size: 1.9rem;
        line-height: 1.5;
        color: var(--ink);
    }
    .scrawl .eq {
        display: inline-block;
        transform: rotate(-1.2deg);
        border-bottom: 1.5px dashed var(--yellow);
        padding: 0 4px 2px;
    }

    .rendered {
        font-family: 'Fraunces', serif;
        font-size: 1.25rem;
        line-height: 1.55;
        color: var(--ink);
    }
    .rendered em { font-style: italic; color: var(--ink-soft); }
    .rendered .tex {
        display: inline-block;
        margin-top: 10px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.88rem;
        color: var(--yellow);
        background: rgba(255,214,10,0.08);
        border: 1px solid rgba(255,214,10,0.22);
        padding: 6px 10px;
        border-radius: 3px;
    }

    .preview-arrow {
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--bg);
        border-left: 1px solid var(--hair);
        border-right: 1px solid var(--hair);
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        color: var(--yellow);
        font-size: 1.3rem;
    }

    /* ---------- Section primitives ---------- */
    .section { margin-top: 112px; }

    .section-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: var(--ink-mute);
        letter-spacing: 0.3em;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 22px;
    }
    .section-label::before {
        content: "§";
        font-family: 'Fraunces', serif;
        font-size: 1.3rem;
        font-style: italic;
        color: var(--yellow);
    }
    .section-label .num { color: var(--yellow); }

    .section-title {
        font-family: 'Fraunces', serif;
        font-weight: 800;
        font-size: clamp(2.2rem, 4.5vw, 3.1rem);
        line-height: 1.02;
        letter-spacing: -0.03em;
        margin: 0 0 28px 0;
        max-width: 820px;
    }
    .section-title em {
        font-style: italic;
        color: var(--yellow);
        font-weight: 400;
    }

    .section-text {
        font-size: 1.05rem;
        line-height: 1.75;
        color: var(--ink-soft);
        max-width: 640px;
        margin: 0;
    }

    /* ---------- Manuscript ---------- */
    .manuscript {
        display: grid;
        grid-template-columns: 1fr 1fr;
        margin-top: 40px;
        border-top: 1px solid var(--hair-2);
        border-bottom: 1px solid var(--hair-2);
    }
    .manuscript-col {
        padding: 44px 44px 44px 0;
        border-right: 1px solid var(--hair);
    }
    .manuscript-col:last-child {
        padding: 44px 0 44px 44px;
        border-right: none;
    }
    .manuscript-col h3 {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.28em;
        text-transform: uppercase;
        color: var(--yellow);
        margin: 0 0 20px 0;
        font-weight: 500;
    }
    .manuscript-col h3::before { content: "→ "; color: var(--ink-mute); }
    .manuscript-col .big-quote {
        font-family: 'Fraunces', serif;
        font-size: 1.6rem;
        line-height: 1.35;
        letter-spacing: -0.015em;
        color: var(--ink);
        margin: 0;
    }
    .manuscript-col .big-quote em {
        font-style: italic;
        color: var(--yellow);
    }

    /* ---------- Benefits ---------- */
    .benefits-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin-top: 40px;
    }
    .benefit {
        position: relative;
        background: var(--bg-2);
        border: 1px solid var(--hair);
        border-radius: 3px;
        padding: 32px 26px 28px;
        transition: transform .35s cubic-bezier(.2,.7,.2,1),
                    border-color .25s, background .25s;
        overflow: hidden;
    }
    .benefit::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: var(--yellow);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform .35s ease;
    }
    .benefit:hover {
        transform: translateY(-6px);
        border-color: var(--hair-2);
        background: var(--bg-3);
    }
    .benefit:hover::before { transform: scaleX(1); }
    .benefit .num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: var(--ink-mute);
        letter-spacing: 0.28em;
        display: block;
        margin-bottom: 20px;
    }
    .benefit .num span { color: var(--yellow); }
    .benefit h3 {
        font-family: 'Fraunces', serif;
        font-style: italic;
        font-weight: 600;
        font-size: 1.55rem;
        line-height: 1.15;
        color: var(--ink);
        margin: 0 0 12px 0;
        letter-spacing: -0.015em;
    }
    .benefit h3 .mark {
        background: linear-gradient(180deg, transparent 58%, var(--yellow) 58%, var(--yellow) 92%, transparent 92%);
        color: var(--ink);
        padding: 0 2px;
    }
    .benefit p {
        margin: 0;
        color: var(--ink-soft);
        line-height: 1.65;
        font-size: 0.96rem;
    }

    /* ---------- Upload ---------- */
    .upload-frame {
        margin-top: 36px;
        background: var(--bg-2);
        border: 1px solid var(--hair-2);
        border-radius: 4px;
        padding: 40px;
        position: relative;
    }
    .upload-frame::before,
    .upload-frame::after {
        content: "";
        position: absolute;
        width: 22px; height: 22px;
        border: 2px solid var(--yellow);
    }
    .upload-frame::before {
        top: -1px; left: -1px;
        border-right: none; border-bottom: none;
    }
    .upload-frame::after {
        bottom: -1px; right: -1px;
        border-left: none; border-top: none;
    }

    .upload-zone {
        border: 2px dashed var(--hair-2);
        background:
            repeating-linear-gradient(45deg,
                transparent 0, transparent 14px,
                rgba(255,214,10,0.03) 14px, rgba(255,214,10,0.03) 15px),
            var(--bg-3);
        padding: 68px 24px;
        text-align: center;
        border-radius: 3px;
        color: var(--ink-soft);
        font-family: 'Fraunces', serif;
        font-style: italic;
        font-size: 1.3rem;
        cursor: pointer;
        transition: border-color .25s, color .25s;
    }
    .upload-zone:hover {
        border-color: var(--yellow);
        color: var(--ink);
    }
    .upload-zone .ico {
        display: block;
        font-family: 'JetBrains Mono', monospace;
        font-style: normal;
        font-size: 0.72rem;
        letter-spacing: 0.32em;
        color: var(--yellow);
        margin-bottom: 14px;
        text-transform: uppercase;
    }
    .upload-zone .hint {
        display: block;
        font-family: 'JetBrains Mono', monospace;
        font-style: normal;
        font-size: 0.68rem;
        letter-spacing: 0.18em;
        color: var(--ink-mute);
        margin-top: 14px;
        text-transform: uppercase;
    }

    .switch-container {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 18px 20px;
        margin-top: 22px;
        background: var(--bg-3);
        border: 1px solid var(--hair);
        border-left: 3px solid var(--yellow);
        border-radius: 2px;
    }
    .switch-container label {
        font-size: 0.95rem;
        color: var(--ink);
        font-weight: 500;
    }
    .switch-container label span {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--yellow);
        letter-spacing: 0.15em;
        margin-left: 6px;
    }
    .switch-container input[type="checkbox"] {
        accent-color: var(--yellow);
        width: 16px; height: 16px;
    }

    /* ---------- Format picker ---------- */
    .format-picker {
        margin-top: 22px;
        padding: 22px;
        background: var(--bg-3);
        border: 1px solid var(--hair);
        border-radius: 2px;
    }
    .format-picker-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        color: var(--yellow);
        margin-bottom: 14px;
        font-weight: 700;
    }
    .format-picker-label::before { content: "◆ "; }
    .format-picker-hint {
        font-size: 0.88rem;
        color: var(--ink-mute);
        margin: 0 0 18px 0;
    }
    .format-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 10px;
    }
    .fmt-opt {
        position: relative;
        cursor: pointer;
        display: block;
    }
    .fmt-opt input { position: absolute; opacity: 0; pointer-events: none; }
    .fmt-opt .box {
        display: flex;
        flex-direction: column;
        gap: 4px;
        padding: 14px 14px 12px;
        border: 1px solid var(--hair);
        background: var(--bg-2);
        border-radius: 2px;
        transition: border-color .2s, background .2s, transform .15s;
    }
    .fmt-opt:hover .box { border-color: var(--hair-2); transform: translateY(-1px); }
    .fmt-opt input:checked + .box {
        border-color: var(--yellow);
        background: rgba(255,214,10,0.08);
    }
    .fmt-opt .name {
        font-family: 'Inter Tight', sans-serif;
        font-size: 0.95rem;
        font-weight: 600;
        color: var(--ink);
    }
    .fmt-opt .ext {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: var(--ink-mute);
        letter-spacing: 0.12em;
    }
    .fmt-opt input:checked + .box .ext { color: var(--yellow); }
    .fmt-opt .check {
        position: absolute;
        top: 10px; right: 10px;
        width: 14px; height: 14px;
        border: 1px solid var(--hair-2);
        border-radius: 2px;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.7rem;
        color: var(--bg);
        background: var(--bg-3);
    }
    .fmt-opt input:checked + .box .check {
        background: var(--yellow);
        border-color: var(--yellow);
    }
    .fmt-opt input:checked + .box .check::after { content: "✓"; font-weight: 700; }

    /* ---------- Result preview tabs ---------- */
    .preview-panel {
        margin: 0 auto 28px;
        max-width: 780px;
        border: 1px solid var(--hair);
        border-radius: 3px;
        background: var(--bg-3);
        overflow: hidden;
        text-align: left;
    }
    .preview-tabs {
        display: flex;
        background: var(--bg-2);
        border-bottom: 1px solid var(--hair);
        overflow-x: auto;
    }
    .preview-tabs button {
        flex-shrink: 0;
        background: none;
        border: none;
        color: var(--ink-mute);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        padding: 14px 20px;
        cursor: pointer;
        border-bottom: 2px solid transparent;
        transition: color .2s, border-color .2s, background .2s;
    }
    .preview-tabs button:hover { color: var(--ink); background: var(--bg-3); }
    .preview-tabs button.active {
        color: var(--yellow);
        border-bottom-color: var(--yellow);
    }
    .preview-pane {
        padding: 22px 24px;
        max-height: 420px;
        overflow: auto;
        display: none;
    }
    .preview-pane.active { display: block; }
    .preview-pane pre {
        margin: 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        line-height: 1.6;
        color: var(--ink-soft);
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .preview-pane .rendered-md {
        font-family: 'Fraunces', serif;
        font-size: 1rem;
        line-height: 1.65;
        color: var(--ink);
    }
    .preview-pane .rendered-md h1,
    .preview-pane .rendered-md h2,
    .preview-pane .rendered-md h3 {
        font-weight: 700;
        color: var(--ink);
        margin: 0.8em 0 0.4em;
    }
    .preview-pane .rendered-md code {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85em;
        background: var(--bg-2);
        padding: 1px 5px;
        border-radius: 2px;
        color: var(--yellow);
    }

    .warning-box {
        margin-top: 20px;
        padding: 18px 20px;
        background: rgba(255,214,10,0.05);
        border: 1px solid rgba(255,214,10,0.2);
        border-left: 3px solid var(--yellow);
        color: var(--ink-soft);
        font-size: 0.92rem;
        line-height: 1.6;
        border-radius: 2px;
    }
    .warning-box::before {
        content: "▲  MARGIN NOTE";
        display: block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.28em;
        color: var(--yellow);
        margin-bottom: 8px;
        font-weight: 700;
    }
    .warning-box p { margin: 0; }

    .agreement-box {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 18px;
        padding: 12px 4px;
        color: var(--ink-soft);
        font-size: 0.93rem;
    }
    .agreement-box input {
        accent-color: var(--yellow);
        width: 16px; height: 16px;
    }

    .btn-primary {
        display: block;
        width: 100%;
        margin-top: 24px;
        border: 1px solid var(--yellow);
        background: var(--yellow);
        color: var(--bg);
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        padding: 18px 20px;
        cursor: pointer;
        transition: background .2s, transform .15s, box-shadow .2s;
        border-radius: 2px;
    }
    .btn-primary:hover {
        background: #fff;
        border-color: #fff;
        transform: translateY(-2px);
        box-shadow: 0 20px 40px -12px rgba(255,214,10,0.5);
    }
    .btn-primary::after {
        content: "  →";
        transition: transform .2s;
        display: inline-block;
    }
    .btn-primary:hover::after { transform: translateX(4px); }

    /* ---------- Loader ---------- */
    .loader-wrap { margin-top: 24px; text-align: center; }
    .skeleton-lines {
        display: flex; flex-direction: column; gap: 12px;
        padding: 24px;
        background: var(--bg-3);
        border: 1px solid var(--hair);
        border-radius: 3px;
    }
    .skeleton-lines span {
        height: 12px;
        background: linear-gradient(90deg,
            rgba(255,255,255,0.04) 25%,
            rgba(255,214,10,0.18) 50%,
            rgba(255,255,255,0.04) 75%);
        background-size: 200% 100%;
        animation: shimmer 1.6s infinite linear;
        border-radius: 2px;
    }
    .skeleton-lines span:nth-child(1) { width: 92%; }
    .skeleton-lines span:nth-child(2) { width: 68%; }
    .skeleton-lines span:nth-child(3) { width: 84%; }
    .skeleton-lines span:nth-child(4) { width: 55%; }
    @keyframes shimmer {
        from { background-position: 200% 0; }
        to   { background-position: -200% 0; }
    }
    .loader-text {
        margin-top: 16px;
        font-family: 'Fraunces', serif;
        font-style: italic;
        color: var(--ink-soft);
    }

    /* ---------- Result ---------- */
    .result-card { text-align: center; padding: 24px 8px; }
    .result-stamp {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.3em;
        color: var(--yellow);
        border: 1.5px solid var(--yellow);
        padding: 7px 16px;
        transform: rotate(-2deg);
        margin-bottom: 22px;
        text-transform: uppercase;
    }
    .result-title {
        font-family: 'Fraunces', serif;
        font-style: italic;
        font-weight: 600;
        font-size: 2.2rem;
        margin: 0 0 12px 0;
        letter-spacing: -0.02em;
        color: var(--ink);
    }
    .result-title em { font-style: normal; color: var(--yellow); }
    .result-sub {
        color: var(--ink-soft);
        margin: 0 0 30px 0;
    }
    .dl-row {
        display: flex;
        justify-content: center;
        gap: 14px;
        flex-wrap: wrap;
    }
    .btn-dl {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 14px 22px;
        border: 1px solid var(--hair-2);
        background: var(--bg-3);
        color: var(--ink);
        text-decoration: none;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        font-weight: 700;
        border-radius: 2px;
        transition: background .2s, color .2s, border-color .2s;
    }
    .btn-dl:hover {
        background: var(--yellow);
        color: var(--bg);
        border-color: var(--yellow);
    }
    .btn-dl .ext { color: var(--yellow); font-size: 0.9rem; }
    .btn-dl:hover .ext { color: var(--bg); }

    .upload-again {
        display: inline-block;
        margin-top: 30px;
        font-family: 'Fraunces', serif;
        font-style: italic;
        color: var(--yellow);
        text-decoration: none;
        font-size: 1.05rem;
        border-bottom: 1px solid var(--yellow-dim);
        padding-bottom: 2px;
    }
    .upload-again:hover { color: #fff; border-bottom-color: #fff; }

    /* ---------- CTA ---------- */
    .cta-btn {
        display: inline-flex;
        align-items: center;
        gap: 12px;
        margin-top: 28px;
        padding: 18px 30px;
        background: var(--yellow);
        color: var(--bg);
        text-decoration: none;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        letter-spacing: 0.24em;
        text-transform: uppercase;
        font-weight: 700;
        border: 1px solid var(--yellow);
        border-radius: 2px;
        transition: background .2s, transform .15s, box-shadow .2s;
    }
    .cta-btn:hover {
        background: #fff;
        border-color: #fff;
        transform: translateY(-2px);
        box-shadow: 0 20px 40px -12px rgba(255,214,10,0.4);
    }

    /* ---------- Footer ---------- */
    .foot {
        margin-top: 128px;
        padding-top: 28px;
        border-top: 1px solid var(--hair);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 14px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: var(--ink-mute);
    }
    .foot .by { color: var(--ink-soft); }
    .foot .brand { color: var(--yellow); font-weight: 700; }

    /* ---------- HTMX ---------- */
    .htmx-indicator { display: none; }
    .htmx-request .htmx-indicator,
    .htmx-request.htmx-indicator { display: block; }

    /* ---------- Entrance ---------- */
    .fade-up {
        opacity: 0;
        transform: translateY(20px);
        animation: fadeUp .95s cubic-bezier(.2,.7,.2,1) forwards;
    }
    .fade-up.d1 { animation-delay: .08s; }
    .fade-up.d2 { animation-delay: .22s; }
    .fade-up.d3 { animation-delay: .36s; }
    .fade-up.d4 { animation-delay: .50s; }
    @keyframes fadeUp {
        to { opacity: 1; transform: translateY(0); }
    }

    /* ---------- Team block ---------- */
    .team-wrap {
        display: grid;
        grid-template-columns: 1.1fr 1fr;
        gap: 48px;
        margin-top: 40px;
        align-items: start;
    }

    .team-photo-frame {
        position: relative;
        border: 1px solid var(--hair-2);
        border-radius: 4px;
        overflow: hidden;
        background: var(--bg-2);
        aspect-ratio: 4 / 3;
    }
    .team-photo-frame::before {
        content: "TEAM · STACKHACKS";
        position: absolute;
        top: 14px; left: 14px;
        background: var(--yellow);
        color: var(--bg);
        padding: 4px 10px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.62rem;
        font-weight: 700;
        letter-spacing: 0.25em;
        z-index: 2;
    }
    .team-photo-frame::after {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(to bottom, transparent 60%, rgba(0,0,0,0.55) 100%);
        pointer-events: none;
        z-index: 1;
    }
    .team-photo-frame img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
        filter: grayscale(0.15) contrast(1.05);
        transition: filter .4s ease, transform .6s cubic-bezier(.2,.7,.2,1);
    }
    .team-photo-frame:hover img {
        filter: grayscale(0) contrast(1);
        transform: scale(1.02);
    }
    .team-photo-caption {
        position: absolute;
        bottom: 14px; left: 14px; right: 14px;
        z-index: 2;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: var(--ink-soft);
        letter-spacing: 0.12em;
        display: flex;
        justify-content: space-between;
    }
    .team-photo-caption .loc { color: var(--yellow); }

    /* Photo placeholder (shown if /static/team_photo.jpg isn't there yet) */
    .team-photo-placeholder {
        width: 100%; height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        gap: 12px;
        background:
            repeating-linear-gradient(45deg,
                transparent 0, transparent 20px,
                rgba(255,214,10,0.04) 20px, rgba(255,214,10,0.04) 21px),
            var(--bg-3);
        color: var(--ink-mute);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
    }
    .team-photo-placeholder .icon {
        font-size: 2.4rem;
        color: var(--yellow);
        font-family: 'Fraunces', serif;
        font-style: italic;
    }

    .team-copy h3 {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.28em;
        text-transform: uppercase;
        color: var(--yellow);
        margin: 0 0 16px 0;
        font-weight: 500;
    }
    .team-copy h3::before { content: "→ "; color: var(--ink-mute); }

    .team-lede {
        font-family: 'Fraunces', serif;
        font-size: 1.4rem;
        line-height: 1.4;
        color: var(--ink);
        margin: 0 0 20px 0;
        letter-spacing: -0.01em;
    }
    .team-lede em {
        font-style: italic;
        color: var(--yellow);
    }

    .team-body {
        color: var(--ink-soft);
        font-size: 1rem;
        line-height: 1.75;
        margin: 0 0 24px 0;
    }

    .team-roster {
        list-style: none;
        padding: 0;
        margin: 0;
        border-top: 1px solid var(--hair);
    }
    .team-roster li {
        display: grid;
        grid-template-columns: auto 1fr auto;
        gap: 16px;
        padding: 14px 0;
        border-bottom: 1px solid var(--hair);
        align-items: baseline;
    }
    .team-roster .tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: var(--yellow);
        letter-spacing: 0.22em;
        text-transform: uppercase;
    }
    .team-roster .name {
        font-family: 'Fraunces', serif;
        font-style: italic;
        font-weight: 600;
        font-size: 1.1rem;
        color: var(--ink);
    }
    .team-roster .role {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--ink-mute);
        letter-spacing: 0.08em;
        text-align: right;
    }

    /* ---------- Results preview (before / after page) ---------- */
    .results-stack {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 28px;
        margin-top: 44px;
    }

    .result-page {
        position: relative;
        border: 1px solid var(--hair-2);
        border-radius: 3px;
        overflow: hidden;
        background: var(--bg-2);
        min-height: 520px;
        box-shadow: 0 30px 80px -30px rgba(0,0,0,0.7);
        transition: transform .4s cubic-bezier(.2,.7,.2,1);
    }
    .result-page:hover { transform: translateY(-4px); }

    .result-page-head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 18px;
        border-bottom: 1px solid var(--hair);
        background: var(--bg-3);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: var(--ink-mute);
    }
    .result-page-head .step {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        color: var(--ink-soft);
    }
    .result-page-head .step .num {
        background: var(--yellow);
        color: var(--bg);
        padding: 2px 7px;
        font-weight: 700;
        border-radius: 2px;
    }
    .result-page-head .fmt { color: var(--yellow); }

    /* Handwritten "scan" look */
    .result-page.scan .result-page-body {
        padding: 32px 36px 40px;
        background:
            repeating-linear-gradient(to bottom,
                transparent 0, transparent 31px,
                rgba(255,255,255,0.05) 31px, rgba(255,255,255,0.05) 32px),
            var(--bg-2);
        min-height: 460px;
        position: relative;
    }
    .result-page.scan .result-page-body::before {
        /* red margin line */
        content: "";
        position: absolute;
        top: 0; bottom: 0;
        left: 48px;
        width: 1px;
        background: rgba(255,214,10,0.35);
    }
    .hw {
        font-family: 'Caveat', cursive;
        font-size: 1.35rem;
        line-height: 32px; /* snap to ruled lines */
        color: var(--ink);
        padding-left: 14px;
    }
    .hw .title {
        font-size: 1.7rem;
        color: var(--yellow);
        font-weight: 600;
        display: block;
        margin-bottom: 4px;
    }
    .hw .eq {
        display: inline-block;
        padding: 0 4px;
        border-bottom: 1.5px dashed rgba(255,214,10,0.6);
        transform: rotate(-0.8deg);
    }
    .hw .crossed {
        text-decoration: line-through;
        text-decoration-color: rgba(255,214,10,0.7);
        color: var(--ink-mute);
    }
    .hw .arrow {
        color: var(--yellow);
        font-size: 1.5rem;
        display: inline-block;
        transform: rotate(-4deg);
    }
    .hw .note {
        font-size: 1rem;
        color: var(--ink-mute);
        transform: rotate(-1.5deg);
        display: inline-block;
    }

    /* Rendered .docx look */
    .result-page.docx .result-page-body {
        padding: 44px 52px 48px;
        background: #faf8f2;
        color: #1a1a1a;
        font-family: 'Fraunces', serif;
        min-height: 460px;
        position: relative;
    }
    .result-page.docx .result-page-body::after {
        /* subtle paper edge */
        content: "";
        position: absolute;
        left: 0; right: 0; bottom: 0;
        height: 40px;
        background: linear-gradient(to bottom, transparent, rgba(0,0,0,0.04));
        pointer-events: none;
    }
    .docx-doc h4 {
        font-family: 'Fraunces', serif;
        font-weight: 800;
        font-size: 1.25rem;
        margin: 0 0 14px 0;
        color: #0a0a0a;
        letter-spacing: -0.01em;
        border-bottom: 2px solid #0a0a0a;
        padding-bottom: 6px;
    }
    .docx-doc p {
        margin: 0 0 10px 0;
        font-size: 0.98rem;
        line-height: 1.6;
        color: #2a2a2a;
    }
    .docx-doc .theorem {
        font-style: italic;
        color: #0a0a0a;
        font-weight: 500;
    }
    .docx-doc .eqline {
        display: block;
        text-align: center;
        margin: 16px 0;
        font-size: 1.15rem;
        color: #0a0a0a;
    }
    .docx-doc .eqline .num {
        float: right;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #888;
    }
    .docx-doc .proof-label {
        font-weight: 600;
        font-style: italic;
    }
    .docx-doc .qed {
        display: inline-block;
        width: 8px; height: 8px;
        background: #0a0a0a;
        vertical-align: middle;
        margin-left: 6px;
    }

    .results-meta {
        margin-top: 28px;
        display: flex;
        flex-wrap: wrap;
        gap: 14px;
        justify-content: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--ink-mute);
    }
    .results-meta span {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 14px;
        border: 1px solid var(--hair);
        background: var(--bg-2);
        border-radius: 2px;
    }
    .results-meta .ok { color: var(--yellow); font-weight: 700; }

    /* ---------- Responsive ---------- */
    @media (max-width: 820px) {
        .page-shell { padding: 20px 20px 60px; }
        .nav { margin-bottom: 56px; }
        .nav-links { gap: 16px; }
        .nav-links a:not(.nav-cta) { display: none; }
        .hero { grid-template-columns: 1fr; min-height: auto; }
        .hero-stamp { display: none; }
        .benefits-grid { grid-template-columns: 1fr; }
        .manuscript { grid-template-columns: 1fr; }
        .manuscript-col { padding: 32px 0; border-right: none; border-bottom: 1px solid var(--hair); }
        .manuscript-col:last-child { border-bottom: none; padding-bottom: 0; }
        .preview { grid-template-columns: 1fr; }
        .preview-arrow {
            border: none;
            border-top: 1px solid var(--hair);
            border-bottom: 1px solid var(--hair);
            padding: 12px;
        }
        .upload-frame { padding: 28px 20px; }
        .section { margin-top: 72px; }
        .foot { justify-content: center; text-align: center; }
        .team-wrap { grid-template-columns: 1fr; gap: 32px; }
        .results-stack { grid-template-columns: 1fr; }
        .result-page.scan .result-page-body,
        .result-page.docx .result-page-body { padding: 28px 24px; }
    }
""")