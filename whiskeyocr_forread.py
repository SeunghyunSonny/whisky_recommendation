import easyocr
import cv2
import matplotlib.pyplot as plt
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

img_path = r'./uploaded/*.jpg'


class TextRecognition:
    def __init__(self, languages=['ko', 'en'], threshold=0.5):
        self.reader = easyocr.Reader(languages)
        self.processor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-handwritten')
        self.model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-handwritten')
        self.threshold = threshold

    def read_and_generate_text(self, img_path):
        img = cv2.imread(img_path)
        image = Image.open(img_path).convert('RGB')

        result = self.reader.readtext(img_path)

        r = []

        for bbox, text, conf in result:
            if conf > self.threshold:
                r.append(text)
                cv2.rectangle(img, pt1=(int(bbox[0][0]), int(bbox[0][1])), pt2=(int(bbox[2][0]), int(bbox[2][1])), color=(0, 255, 0), thickness=3)

        plt.figure(figsize=(8, 8))
        plt.imshow(img[:, :, ::-1])
        plt.axis('off')
        pixel_values = self.processor(images=image, return_tensors="pt").pixel_values
        generated_ids = self.model.generate(pixel_values)
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return generated_text

# 클래스 인스턴스 생성
text_recognizer = TextRecognition()

# 이미지 경로


# 텍스트 인식 및 생성
generated_text = text_recognizer.read_and_generate_text(img_path)
print(generated_text)
