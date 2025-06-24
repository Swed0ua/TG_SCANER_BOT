import cv2
import pytesseract

class OCRService:
    def extract_text(self, image_path: str) -> str:
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, lang='ukr+eng')
        return text