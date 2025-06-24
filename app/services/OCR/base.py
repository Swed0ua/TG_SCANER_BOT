from abc import ABC, abstractmethod
import cv2

class OCRBase(ABC):
    def preprocess_image(self, image_path, binary_threshold=150, invert=False):
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        _, binary = cv2.threshold(image, binary_threshold, 255, cv2.THRESH_BINARY)
        if invert:
            binary = cv2.bitwise_not(binary)
        return binary
