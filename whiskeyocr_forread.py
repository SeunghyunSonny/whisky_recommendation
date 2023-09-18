import easyocr
import cv2
import matplotlib.pyplot as plt
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import pickle
import torch
from dataclasses import dataclass

@dataclass(frozen=True)
class ModelConfig:
    MODEL_NAME: str = 'microsoft/trocr-large-handwritten'
    MODEL_STATE_PATH: str = "model_state_dict.pkl"

class TextRecognition:
    def __init__(self, languages=['ko', 'en'], threshold=0.5):
        self.reader = easyocr.Reader(languages)
        self.processor = TrOCRProcessor.from_pretrained(ModelConfig.MODEL_NAME)
        self.model = VisionEncoderDecoderModel.from_pretrained(ModelConfig.MODEL_NAME)
        self.threshold = threshold
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._load_model_state_from_file()

    def _load_model_state_from_file(self):
        with open(ModelConfig.MODEL_STATE_PATH, "rb") as file:
            loaded_state_dict = pickle.load(file)
        self.model.load_state_dict(loaded_state_dict)
        self.model.to(self.device)

    def ocr_on_image(self, image_path):
        image = Image.open(image_path).convert("RGB")
        pixel_values = self.processor(images=image, return_tensors="pt").pixel_values
        generated_ids = self.model.generate(pixel_values)
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return generated_text

    def display_image_with_boxes(self, img_path, result):#수정필요 - 이미지 인식단 해미님
        img = cv2.imread(img_path)
        for bbox, text, conf in result:
            if conf > self.threshold:
                cv2.rectangle(img, pt1=(int(bbox[0][0]), int(bbox[0][1])), pt2=(int(bbox[2][0]), int(bbox[2][1])), color=(0, 255, 0), thickness=3)

        plt.figure(figsize=(8, 8))
        plt.imshow(img[:, :, ::-1])
        plt.axis('off')
        plt.show()

    def read_and_generate_text(self, img_path):
        result = self.reader.readtext(img_path)
        self.display_image_with_boxes(img_path, result)
        generated_text = self.ocr_on_image(img_path)
        return generated_text

# Example Usage:
if __name__ == "__main__":
    img_path = r'./uploaded/*.jpg'  # Provide your image path here.
    text_recognizer = TextRecognition()
    generated_text = text_recognizer.read_and_generate_text(img_path)
    print(generated_text)
