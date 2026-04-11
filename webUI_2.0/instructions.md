# System Context: Ink2Pixel Web Application

## Project Overview
You are building the web interface and backend routing for **Ink2Pixel**. The goal of this tool is to convert scanned or handwritten math notes into editable digital files (.docx or .txt) while preserving the original layout. 

The user wants a "single-click" executable vibe with a highly engaging, colorful frontend. You are acting as an expert Python developer specializing in **FastHTML** and **HTMX**.

## Core Tech Stack & Strict Constraints
* **Framework:** FastHTML (Python)
* **Interactivity:** HTMX (Native to FastHTML, do not write custom JS unless absolutely necessary)
* **Environment Restrictions:** * NO Docker. 
  * NO Node.js. 
  * NO separate frontend/backend repositories. 
* **Architecture:** Everything web-related must be contained in a single `app.py` file or a tightly coupled `routes` folder.

## Styling & Design Direction (CRITICAL)
* **Vibe:** Lively, vibrant, and highly colorful. Absolutely DO NOT make it a dry, sterile, black-and-white corporate tool.
* **Colors & Elements:** Use rich CSS gradients for backgrounds or text, playful but professional color palettes, rounded corners, soft colorful shadows, and interactive hover effects.
* **Implementation:** Utilize FastHTML's styling integrations (like PicoCSS or inline Tailwind utilities if configured) to inject life into the UI. Every section should feel distinct and visually appealing.

## AI & Processing Pipeline Logic
The backend logic utilizes the following workflow. The web app must integrate these without freezing:
1.  **Image Pre-processing:** Handled by OpenCV.
2.  **Detection & Routing:** A custom classifier detects regions as handwritten text, math symbols, or images.
3.  **Core Text OCR:** Uses EasyOCR (or equivalent). Loaded on app startup.
4.  **Math Detection (Beta):** Uses a heavy VLM. **CRITICAL:** This model must NOT be loaded on startup.
5.  **Reconstruction:** OpenCV contours preserve layout and output a clean `.docx` or `.txt` file.

## Page Structure & Content Requirements

### 1. The Hero Section
* A vibrant, eye-catching header with the app's title ("Ink2Pixel").
* Use a colorful gradient text effect for the title.

### 2. Mission & Vision Section
* Add a visually distinct block (like a styled card or colored panel).
* **Mission:** To bridge the gap between physical handwriting and digital workflows without losing the context of complex math.
* **Vision:** A world where students, researchers, and professionals never have to manually type out a long LaTeX equation again.

### 3. Benefits of the Code Section
* Create a lively grid or flexbox showcasing the technical perks of Ink2Pixel:
  * **Privacy First:** 100% local processing; your notes never leave your machine.
  * **Layout Preservation:** OpenCV ensures your digital file looks just like your original page.
  * **Smart Math Detection:** Seamlessly converts scribbles into perfect LaTeX.

### 4. Main Upload Interface & The "Beta" VLM Toggle
* Implement a styled, colorful drag-and-drop file upload zone accepting images and PDFs.
* Include a prominent, stylized toggle switch labeled "Enable Advanced Math Detection (Beta VLM)".
* **Memory Management Rule:** If toggled ON, the app must dynamically load the VLM into memory, process the math regions, and then explicitly delete the model from memory (`del model_instance`) to protect users with low-end PCs. If OFF, fallback to the core pipeline.

### 5. Asynchronous UI Updates (Non-Blocking)
* When a file is uploaded, use HTMX to immediately swap the upload box with a sleek, pulsing, colorful progress indicator or skeleton loader.
* You must never block the main thread. Run the actual OCR/VLM processing asynchronously.

### 6. Results Dashboard
* Upon completion, use HTMX to swap the loader with the final extracted results.
* Provide distinct, brightly colored download buttons for the `.docx` and `.txt` files.

## Developer Instructions for Current Session
1. Read these constraints carefully.
2. Generate the `app.py` file using FastHTML.
3. Implement mock functions using `asyncio.sleep()` for the OpenCV and OCR/VLM steps so the colorful UI transitions can be tested immediately.
4. Leave clear inline comments where the core machine learning pipeline will be imported later.