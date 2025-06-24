import pytesseract
from PIL import Image
import cv2
import pandas as pd

from app.services.OCR.base import OCRBase

class TesseractOCR(OCRBase):
    def extract_text(self, image_path: str) -> str:
        image = Image.open(image_path)
        return pytesseract.image_to_string(image, lang='ukr')
