import cv2
import pandas as pd
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from fuzzywuzzy import fuzz
import matplotlib.pyplot as plt
import torch

class WhiskeyLogoProcessor:
    def __init__(self, df_path, trocr_model_name, threshold_similarity=90):
        self.df = pd.read_csv(df_path, encoding='utf-8')
        self.processor = TrOCRProcessor.from_pretrained(trocr_model_name)
        self.model = VisionEncoderDecoderModel.from_pretrained(trocr_model_name)
        self.threshold_similarity = threshold_similarity

    def show_img(self, img):
        plt.figure(figsize=(8, 8))
        plt.imshow(img[:, :, ::-1])
        plt.axis('off')
        plt.show()

    def get_detection_text(self, img):
        pixel_values = self.processor(img, return_tensors="pt").pixel_values
        generated_ids = self.model.generate(pixel_values)
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return generated_text

    def find_similar_names(self, name):
        temp_Sr = self.df['nameEng'].apply(str.lower)
        similar_names = self.df[self.df['nameEng'].apply(lambda x: fuzz.partial_ratio(x, name) >= self.threshold_similarity)]
        similar_names = similar_names.reset_index(drop=True)
        return similar_names

    def lines_process(self, img):
        cut_line = round(img.shape[0] / 2)
        pil_image1 = Image.fromarray(img[:cut_line, :])
        pil_image2 = Image.fromarray(img[cut_line:, :])
        get_text1 = self.get_detection_text(img=pil_image1)
        get_text2 = self.get_detection_text(img=pil_image2)
        result = get_text1 + get_text2
        return result

    def line_process(self, img):
        pil_image = Image.fromarray(img)
        result = self.get_detection_text(img=pil_image)
        return result

    def result_list(self, str_text, length=5):
        target_name = str_text.lower()
        similar_names = self.find_similar_names(target_name)
        result = similar_names.loc[:length, 'nameEng'].to_list()
        return result