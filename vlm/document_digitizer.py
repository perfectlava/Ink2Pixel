import torch
import os
import tempfile
import re
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor, BitsAndBytesConfig
from qwen_vl_utils import process_vision_info

class DocumentDigitizer:
    def __init__(self, model_id="Qwen/Qwen2.5-VL-7B-Instruct"):
        print("Loading Qwen2.5-VL in 4-bit mode into VRAM... Please wait.")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        compute_dtype = torch.bfloat16 if (torch.cuda.is_available() and torch.cuda.is_bf16_supported()) else torch.float16
        
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=compute_dtype
        )
        
        self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            model_id, 
            device_map="auto",
            torch_dtype=compute_dtype,
            quantization_config=quantization_config
        )
        self.processor = AutoProcessor.from_pretrained(model_id)
        print("Model loaded successfully!")

    def _get_prompt_for_format(self, output_format: str) -> str:
        base_instruction = (
            "You are an expert document transcriber. Extract all text, math formulas, and document structure. "
            "CRITICAL RULES: "
            "1. Layout: Preserve all structural line breaks exactly as they appear in the image. "
            "If there is a numbered list (e.g., 1., 2.), you MUST put each item on a brand new line. "
            "2. Math: Extract all formulas accurately using standard math environments."
        )
        
        format_instructions = {
            "md": "Output strictly in cleanly formatted Markdown.",
            "latex": (
                "Output strictly as raw LaTeX code for the document body. "
                "Do NOT output \\documentclass, \\usepackage, or \\begin{document}...\\end{document}. I will handle the preamble. "
                "CRITICAL: Ensure ALL equations, variables, and matrices (like \\begin{bmatrix}...) are strictly wrapped in valid math mode "
                "(e.g., \\[ ... \\] for block math, or \\( ... \\) for inline math). NEVER place a matrix outside of math mode."
            ),
            "html": "Output strictly as clean HTML5.",
            "json": "Output strictly as a JSON object with a single key 'document_text'.",
            "docx": "Output strictly in cleanly formatted Markdown. I will handle the Word conversion."
        }
        
        specific_instruction = format_instructions.get(output_format, format_instructions["md"])
        return f"{base_instruction} {specific_instruction}"

    def _fix_math_delimiters(self, text: str) -> str:
        """
        Safely enforces Markdown math delimiters.
        Crucially strips spaces just inside inline $ delimiters, as Pandoc fails to render `$ math $`.
        """
        text = text.replace(r"\[", "$$").replace(r"\]", "$$")
        
        text = re.sub(r"\\\(\s*(.*?)\s*\\\)", r"$\1$", text, flags=re.DOTALL)
        
        text = re.sub(r'\$\s+([^$\n]+?)\s+\$', r'$\1$', text)
        
        return text
        

    def _run_vlm(self, image_path: str, prompt: str) -> str:
        """Helper to process a single image through the model."""
        messages = [{"role": "user", "content": [{"type": "image", "image": image_path}, {"type": "text", "text": prompt}]}]
        
        text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        image_inputs, video_inputs = process_vision_info(messages)

        inputs = self.processor(
            text=[text], images=image_inputs, videos=video_inputs, padding=True, return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            generated_ids = self.model.generate(**inputs, max_new_tokens=4096)

        generated_ids_trimmed = [out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)]
        extracted_text = self.processor.batch_decode(generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

        if extracted_text.startswith("```"):
            lines = extracted_text.split("\n")
            if len(lines) > 2:
                extracted_text = "\n".join(lines[1:-1])
                
        return extracted_text

    def process_and_save(self, image_path: str, output_path: str, output_format: str = "md") -> str:
        """Processes the image/PDF and saves it. Handles PDFs page-by-page to insert breaks and save VRAM."""
        prompt = self._get_prompt_for_format(output_format)
        extracted_texts = []

        if image_path.lower().endswith(".pdf"):
            try:
                import fitz  
            except ImportError:
                raise ImportError("Processing PDFs requires PyMuPDF. Install via: pip install pymupdf")
            
            doc = fitz.open(image_path)
            temp_dir = tempfile.TemporaryDirectory()
            
            for i in range(len(doc)):
                print(f"Processing PDF page {i+1} of {len(doc)}...")
                page = doc.load_page(i)
                pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
                temp_img_path = os.path.join(temp_dir.name, f"page_{i}.png")
                pix.save(temp_img_path)
                
                text = self._run_vlm(temp_img_path, prompt)
                extracted_texts.append(text)
                
            temp_dir.cleanup()
        else:
            print("Processing image...")
            text = self._run_vlm(image_path, prompt)
            extracted_texts.append(text)

        full_document_text = "\n\n=== PAGE BREAK ===\n\n".join(extracted_texts)

        if output_format != "latex":
            full_document_text = self._fix_math_delimiters(full_document_text)

        return self._export_document(full_document_text, output_path, output_format)

    def _export_document(self, text: str, base_filename: str, output_format: str) -> str:
        """Handles file creation, page breaks, and rendering Math in Word."""
        file_path = f"{base_filename}.{output_format}"
        
        if output_format == "docx":
            try:
                import pypandoc
                
                docx_page_break = '\n\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n'
                pandoc_text = text.replace("=== PAGE BREAK ===", docx_page_break)
                
                pypandoc.convert_text(pandoc_text, 'docx', format='markdown', outputfile=file_path)
                print(f"Successfully saved cleanly formatted Word document with rendered Math to {file_path}")
                
            except (ImportError, OSError):
                print("WARNING: pypandoc/pandoc not found. Falling back to basic python-docx. Math will NOT be rendered.")
                import docx
                doc = docx.Document()
                pages = text.split("=== PAGE BREAK ===")
                
                for idx, page_text in enumerate(pages):
                    if idx > 0:
                        doc.add_page_break()
                    for para in page_text.split("\n\n"):
                        if para.strip():
                            doc.add_paragraph(para.strip())
                doc.save(file_path)

        elif output_format in ["md", "html"]:
            text = text.replace("=== PAGE BREAK ===", '\n\n<div style="page-break-after: always;"></div>\n\n')
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
                
        elif output_format == "latex":
            file_path = f"{base_filename}.tex"
            body_text = text.replace("=== PAGE BREAK ===", "\n\n\\newpage\n\n")
            
            latex_document = (
                "\\documentclass{article}\n"
                "\\usepackage{amsmath, amssymb}\n"
                "\\begin{document}\n\n"
                f"{body_text}\n\n"
                "\\end{document}"
            )
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(latex_document)
                
        else:
            file_path = f"{base_filename}.txt"
            text = text.replace("=== PAGE BREAK ===", "\n\n--------------------\n\n")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
                
        return file_path