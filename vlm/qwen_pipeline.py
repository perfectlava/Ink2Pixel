import torch
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info

class QwenDocumentDigitizer:
    def __init__(self, model_id="Qwen/Qwen2.5-VL-7B-Instruct"):
        print("Loading Qwen2.5-VL... This may take a moment.")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Loaded in bfloat16 to use ~14GB VRAM, fitting safely in your 5080 16GB
        self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            model_id, 
            torch_dtype=torch.bfloat16, 
            device_map="auto"
        )
        self.processor = AutoProcessor.from_pretrained(model_id)
        print("Model loaded successfully!")

    def process_document(self, image_path: str, output_format: str = "md") -> str:
        """
        Reads handwritten documents and outputs formatted text.
        output_format is a placeholder for future logic (e.g., json, plain text, md).
        """
        
        # You can tweak this prompt later depending on the output_format requested by the user.
        # For now, it defaults to a clean Markdown extraction.
        prompt = (
            "You are an expert document transcriber. Extract all the handwritten text "
            "from this image. Maintain the original paragraphs, line breaks, and formatting. "
            "Output the transcription cleanly in Markdown format."
        )

        messages = [
            {
                "role": "user",
                "content":[
                    {"type": "image", "image": image_path},
                    {"type": "text", "text": prompt},
                ],
            }
        ]

        # Prepare inputs
        text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        image_inputs, video_inputs = process_vision_info(messages)

        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt"
        ).to(self.device)

        # Generate (max_new_tokens=2048 allows for very long pages of text)
        with torch.no_grad():
            generated_ids = self.model.generate(**inputs, max_new_tokens=2048)

        # Trim the prompt tokens out of the output
        generated_ids_trimmed =[
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]

        output_text = self.processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        
        return output_text[0]

# --- Usage Example ---
# if __name__ == "__main__":
#     pipeline = QwenDocumentDigitizer()
#     result = pipeline.process_document("raw_handwriting.jpg", output_format="md")
#     print(result)