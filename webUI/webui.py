import gradio as gr
import cv2
import numpy as np
from PIL import Image
import io

def convert_to_bw(input_image):
    image_np = np.array(input_image)
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    output_image = Image.fromarray(bw)
    return output_image


with gr.Blocks() as demo:
    gr.Markdown("# Basic Handwritten Notes Converter")
    input_img = gr.Image(type="pil", label="Upload Image")
    output_img = gr.Image(label="Black and White Version")
    process_btn = gr.Button("Convert")
    process_btn.click(convert_to_bw, inputs=input_img, outputs=output_img)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)