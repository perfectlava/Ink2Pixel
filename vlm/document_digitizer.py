import torch
import os
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
import docx  # For saving Word documents

class DocumentDigitizer:
    def __init__(self, model_id="Qwen/Qwen2.5-VL-7B-Instruct"):
        print("Loading Qwen2.5-VL into VRAM... Please wait.")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            model_id, 
            torch_dtype=torch.bfloat16, 
            device_map="auto"
        )
        self.processor = AutoProcessor.from_pretrained(model_id)
        print("Model loaded successfully!")

    def _get_prompt_for_format(self, output_format: str) -> str:
        """Dynamically adjusts the AI's prompt based on the user's requested format."""
        base_instruction = (
            "You are an expert document transcriber. Extract all the handwritten text, "
            "math formulas, and structure from this image. "
            "Critically: visually replicate the original layout, paragraphs, and indentations as closely as possible."
        )
        
        format_instructions = {
            "md": "Output the transcription strictly in cleanly formatted Markdown.",
            "latex": "Output the transcription strictly as a compilable LaTeX document. Use appropriate math environments ($ or $$) for formulas. Start with \\documentclass{article}.",
            "html": "Output the transcription strictly as clean HTML5. Use semantic tags like <p>, <h1>, <ul>, and preserve line breaks with <br>.",
            "json": "Output the transcription strictly as a JSON object with a single key 'document_text' containing the extracted text.",
            "docx": "Output the transcription in plain text with clear paragraph breaks. I will convert this to a Word document."
        }
        
        # Default to Markdown if an unknown format is passed
        specific_instruction = format_instructions.get(output_format, format_instructions["md"])
        
        return f"{base_instruction} {specific_instruction}"

    def process_and_save(self, image_path: str, output_path: str, output_format: str = "md") -> str:
        """
        Processes the image and saves it directly to the desired file format.
        """
        prompt = self._get_prompt_for_format(output_format)

        messages = [
            {
                "role": "user",
                "content":[
                    {"type": "image", "image": image_path},
                    {"type": "text", "text": prompt},
                ],
            }
        ]

        # Prepare inputs for the VLM
        text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        image_inputs, video_inputs = process_vision_info(messages)

        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt"
        ).to(self.device)

        # Generate output
        with torch.no_grad():
            generated_ids = self.model.generate(**inputs, max_new_tokens=2048)

        # Trim the prompt out of the generation
        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]

        extracted_text = self.processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )[0]
        
        # Strip markdown code block wrappers (like ```latex ... ```) if the AI adds them
        if extracted_text.startswith("```"):
            lines = extracted_text.split("\n")
            if len(lines) > 2:
                extracted_text = "\n".join(lines[1:-1])

        # Save to the requested file format
        return self._export_document(extracted_text, output_path, output_format)

    def _export_document(self, text: str, base_filename: str, output_format: str) -> str:
        """Handles file creation based on the format."""
        
        file_path = f"{base_filename}.{output_format}"
        
        if output_format == "docx":
            # Native Word Document generation
            doc = docx.Document()
            
            # Split AI output by double newlines to create natural Word paragraphs
            paragraphs = text.split("\n\n")
            for para in paragraphs:
                if para.strip():
                    doc.add_paragraph(para.strip())
                    
            doc.save(file_path)
            
        elif output_format in ["md", "html", "json"]:
            # Plain text based formats
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
                
        elif output_format == "latex":
            # Ensure the extension is .tex for LaTeX
            file_path = f"{base_filename}.tex"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
                
        else:
            # Fallback
            file_path = f"{base_filename}.txt"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
                
        print(f"Successfully saved to {file_path}")
        return file_path

# --- Usage Example ---
if __name__ == "__main__":
    pipeline = DocumentDigitizer()
    
    # Example 1: Extract as Markdown
    # pipeline.process_and_save("../testing_images/note_page.jpg", output_path="output_markdown", output_format="md")
    
    # Example 2: Extract as LaTeX (Great for math notes)
    pipeline.process_and_save("/home/aidev/Projects/Stack-Hack-AI-Team/Ink2Pixel/testing_images/math.jpg", output_path="output_math", output_format="latex")
    
    # Example 3: Extract directly to a Microsoft Word document
    # pipeline.process_and_save("meeting_notes.jpg", output_path="output_word", output_format="docx")