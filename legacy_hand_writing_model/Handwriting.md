# Handwriting Model

## Results 

![Demo Image](results/results.png)

This model achieved a ~87% character-level accuracy for a mixed set of images from the internet, and actual handwriting images from multiple friends.

## Tech Stack
 - **OCR Library**: [EasyOCR](https://github.com/jaidedai/easyocr)
 - **Dataset**: [IAM Handwriting Dataset](https://huggingface.co/datasets/Teklia/IAM-line)
 - **GPU used for Training**: Google Colab T4 GPU

## Pipeline
 1. **Dataset**: Loads dataset, cleans Labels
 2. **TinyOCR**: Custom OCR Model, 2 CNN Layers --> 1 RNN layer. Finds the shape and sequence of characters
 3. **Decoder**: Used both Greedy and Beam Search, Greedy to find the most likely character and Beam Search to find the most likely sequence 
 4. **Randomize**: Creates noise in dataset by rotating images
 5. **Train & Test**: Trained for 110 epochs using Google Colab, and incorporated preprocessing into testing
 6. **Inference**: Wrapper around model for predictions, sets up preprocessing and loading model


The model worked well with images that were 36 x 300 px, and the preprocessing resized the dimensions to 32 x 240 px and then added padding to become 32 x 256 px before inputting it into the model. While there was some variation in the results, we found that it performed poorly with sentences that were too long, had too many capitals, or excessive punctuation. However, it did well with most other images and was surprisingly fast as well, taking about 8 - 10 seconds per image. The model struggled with full size images, not because of the model but due to the preprocessing struggling to find and crop lines according to the model's strict dimensions, which happened because the IAM Handwriting Dataset that we trained with lacked variety in font, contrast, and size, and was the only one both free and somewhat large. Ultimately, we made considerable progress, especially since the model was trained for only 110 epochs to prevent overfitting and the limitations with our dataset. 