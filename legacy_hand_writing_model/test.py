from inference import HandwritingPredictor, predict_handwriting
import os
from PIL import Image

predictor = HandwritingPredictor()

def predict_image(img_path):
    # Maintain the slight crop if it's important for the specific test images
    img = Image.open(img_path).convert("L")
    w, h = img.size
    img = img.crop((int(w * 0.015), 0, w, h))
    return predictor.predict(img)


# =========testing_images==========

test_images = [
    ("testing_images/first.png",  "this is a handwritten"),
    ("testing_images/second.png", "Write as good as you can."),
    ("testing_images/third.png",  "Plants to buy"),
    ("testing_images/fourth.png", "How to improve your handwriting"),
    ("testing_images/fifth.png", "HELLO, MY NAME IS"),
    ("testing_images/sixth.png", "to us human is what water to"),
    ("testing_images/seventh.png", "fish.Love shines the"),
    ("testing_images/eight.png", "light of humanity,we born in it,we live by it.Too"),
    ("testing_images/ninth.png", "take it as granted,but we should know love is a"),
    ("testing_images/tenth.png", "saying the quickest way to receive love is to give"),
    ("testing_images/eleventh.png",  "stest way to lose love is to hold it too tightly the best"),
    ("testing_images/twelfth.png",  "was anything left in the world that could possibly give"),
    ("testing_images/thirteenth.png",  "Haroun-al-Raschid merely turned his head and looked at him"),
    ("testing_images/fourteenth.png",  "course, I failed. But Mrs. Wang cheered me up and said"),
    ("testing_images/fifteenth.png",  "new software also brings the November 2022 security patch")
]

for val, (img_path, gt_text) in enumerate(test_images):
    if not os.path.exists(img_path):
        print(f"⚠ Image not found: {img_path}")
        continue
    pr_text = predict_image(img_path)
    print(f"Image #{val + 1}:")
    print(f"GT : {gt_text}")
    print(f"PR : {pr_text}\n")
    
print("-------------------------------------------------------------")    
controlled_images = [
    ("controlled_images/first.png", "Edna goes to the ocean"),
    ("controlled_images/second.png", "This is one of the few"),
    ("controlled_images/third.png", "It consists of 12 regional"),
    ("controlled_images/fourth.png", "must hold, and the ways"),
    ("controlled_images/fifth.png", "some nonmarket forces include"),
    ("controlled_images/sixth.png", "discrimination, and government action"),
    ("controlled_images/seventh.png", "S. A. Nigosan, World Religions, A"),
    ("controlled_images/eighth.png", 'Evidence: "Most people delude'),
    ("controlled_images/ninth.png", "They are the same when the function of"),
    ("controlled_images/tenth.png", "Because consumers are loyal towards the")
]

for val, (img_path, gt_text) in enumerate(controlled_images):
    if not os.path.exists(img_path):
        print(f"⚠ Image not found: {img_path}")
        continue
    pr_text = predict_image(img_path)
    print(f"Image #{val + 1}:")
    print(f"GT : {gt_text}")
    print(f"PR : {pr_text}\n")


# =========end_testing==========