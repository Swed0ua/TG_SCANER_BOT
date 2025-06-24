import os
import pytest
from app.services.OCR.tesseract_ocr import TesseractOCR

FIXTURE_IMAGE = "tests/fixtures/test_read_text_1.jpg"

FIXTURE_IMAGES = [
    ("tests/fixtures/test_read_text_1.jpg", "<Hello World/>")
]


@pytest.mark.parametrize("image_path, expected_text", FIXTURE_IMAGES)
def test_ocr_extract_text(image_path, expected_text):
    ocr = TesseractOCR()
    text = ocr.extract_text(image_path)

    assert isinstance(text, str)
    assert expected_text in text