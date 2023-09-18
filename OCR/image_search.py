from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from PIL import Image
from io import BytesIO
import base64

class ImageSearch:
    def __init__(self, driver_path):
        self.driver_path = driver_path

    def fetch_image_with_selenium(self, search_query):
        chrome_options = Options()
        # If you want to run chrome in headless mode (without opening a UI window)
        chrome_options.add_argument("--headless")

        service = Service(self.driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Google 이미지 검색으로 이동
        driver.get(f"https://images.google.com/search?q={search_query}&tbm=isch")

        try:
            # 첫 번째 이미지 요소 가져오기
            image_element = driver.find_element(By.CSS_SELECTOR, "img.rg_i")
            image_url = image_element.get_attribute("src")
            return image_url
        except NoSuchElementException:
            print("No image found for the query")
            return None
        finally:
            driver.quit()

    def save_image(self, image_data, save_path="downloaded_image.jpg"):
        """ 이미지 데이터를 받아서 파일로 저장하고 저장 경로를 반환합니다. """
        if "base64" in image_data:
            base64_data = image_data.split(',', 1)[1]
            image = Image.open(BytesIO(base64.b64decode(base64_data)))
            image.save(save_path)
            return save_path
        else:
            print("Image is not in base64 format")
            return None

    def search_and_save_query(self, query):
        query += " 데일리샷"
        image_data = self.fetch_image_with_selenium(query)
        if image_data:
            saved_path = self.save_image(image_data)
            return saved_path
        else:
            return None
