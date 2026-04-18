import torch
from transformers import AutoModel, AutoTokenizer
from transformers.cache_utils import DynamicCache

# --- FIX FOR TRANSFORMERS COMPATIBILITY BUG ---
# GOT-OCR relies on deprecated attributes that modern HuggingFace removed.
# We dynamically inject them back into the cache class to prevent the crash!
if not hasattr(DynamicCache, "seen_tokens"):
    DynamicCache.seen_tokens = property(lambda self: self.get_seq_length())

if not hasattr(DynamicCache, "get_max_length"):
    DynamicCache.get_max_length = lambda self: None
# ----------------------------------------------

class GotOcrDigitizer:
    def __init__(self, model_id="ucaslcl/GOT-OCR2_0"):
        print("Loading GOT-OCR 2.0... (This is very fast)")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
        
        self.model = AutoModel.from_pretrained(
            model_id,
            trust_remote_code=True,
            low_cpu_mem_usage=True,
            device_map="auto",
            torch_dtype=torch.bfloat16
        )
        self.model = self.model.eval()
        print("Model loaded successfully!")

    def process_document(self, image_path: str, output_format: str = "md") -> str:
        """
        Extracts text, math, and formatting natively.
        GOT-OCR has built-in 'type' parameters instead of using chat prompts.
        """
        
        # 'format' is the best mode for documents containing text + math equations + tables.
        extraction_type = "format" 

        try:
            with torch.no_grad():
                result = self.model.chat(
                    self.tokenizer, 
                    image_path, 
                    ocr_type=extraction_type
                )
            return result
            
        except Exception as e:
            return f"An error occurred during OCR: {str(e)}"

# --- Usage Example ---
if __name__ == "__main__":
    pipeline = GotOcrDigitizer()
    
    # Replace with the path to your raw handwriting image
    result = pipeline.process_document("handwriting.jpg", output_format="md") 
    print(result)