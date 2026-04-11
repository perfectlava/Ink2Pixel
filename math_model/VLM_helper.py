import torch
from transformers import AutoProcessor, Qwen2VLForConditionalGeneration, BitsAndBytesConfig
from qwen_vl_utils import process_vision_info
from PIL import Image
import matplotlib.pyplot as plt
from IPython.display import display, Markdown, HTML

class MathVLMHelper:
    def __init__(self, model_id="Qwen/Qwen2-VL-7B-Instruct", use_4bit=True):
        """
        Initializes the VLM. 
        use_4bit=True is recommended to leave plenty of VRAM on your RTX 5080 
        for context window and image processing.
        """
        print(f"Loading {model_id}...")
        self.processor = AutoProcessor.from_pretrained(model_id)
        
        # Load model with quantization if requested
        kwargs = {"device_map": "cuda"}
        if use_4bit:
            kwargs["quantization_config"] = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.bfloat16
            )
        else:
            kwargs["torch_dtype"] = torch.bfloat16

        self.model = Qwen2VLForConditionalGeneration.from_pretrained(model_id, **kwargs)
        self.model.eval()
        print("Model loaded successfully!")

    def process_image(self, image_path, custom_prompt=None):
        """
        Sends the image and prompt to the VLM.
        """
        # Default prompt heavily optimized for Math to LaTeX
        prompt = custom_prompt or (
            "You are an expert transcriber of mathematical notes. "
            "Please transcribe the handwriting in the image into a clean markdown document. "
            "Convert all mathematical equations, symbols, and formulas into proper LaTeX formats. "
            "Use single $ for inline math and double $$ for block math equations. "
            "Preserve the structural layout (headers, bullet points) as best as you can. "
            "Ignore any non-text/non-math diagrams, just transcribe the text and math."
        )

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image_path},
                    {"type": "text", "text": prompt},
                ],
            }
        ]

        # Process inputs
        text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        image_inputs, video_inputs = process_vision_info(messages)
        
        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        ).to("cuda")

        # Generate output
        print("Generating transcription... (this might take a few seconds)")
        with torch.no_grad():
            generated_ids = self.model.generate(
                **inputs, 
                max_new_tokens=1024, # Adjust based on document length
                temperature=0.1,     # Low temperature for factual transcription
                do_sample=False
            )

        # Trim the input prompt from the generated output
        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        
        output_text = self.processor.batch_decode(
            generated_ids_trimmed, 
            skip_special_tokens=True, 
            clean_up_tokenization_spaces=False
        )[0]

        return output_text

    def visualize_result(self, image_path, output_text):
        """
        Displays the original image next to the rendered Markdown/LaTeX output 
        inside the Jupyter Notebook.
        """
        # 1. Show the original image
        img = Image.open(image_path)
        plt.figure(figsize=(10, 8))
        plt.imshow(img)
        plt.axis('off')
        plt.title("Original Scanned Image")
        plt.show()

        # 2. Show the raw LaTeX/Text
        print("-" * 50)
        print("RAW OUTPUT (To be saved to .txt / .docx):")
        print("-" * 50)
        print(output_text)
        print("-" * 50)

        # 3. Render the output as Markdown with LaTeX formatting in Jupyter
        display(HTML("<h3>Rendered Output:</h3>"))
        display(Markdown(output_text))