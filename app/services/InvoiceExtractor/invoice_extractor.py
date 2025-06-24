from ..ChatGPTService.chat_gpt_service import ChatGPTService
from ..OCR.ocr_service import OCRService
import json

class InvoiceExtractor:
    def __init__(self, api_key: str):
        self.ocr = OCRService()
        self.gpt = ChatGPTService(api_key=api_key)

    def extract_invoice(self, image_path: str) -> dict:
        text = self.ocr.extract_text(image_path)
        # prompt = (
        #     "Extract invoice data from the following text strictly in this JSON format:\n"
        #     "{"
        #     "\"number\": \"\", \"date\": \"\", \"supplier\": {\"name\": \"\", \"edrpou\": \"\", \"iban\": \"\", \"address\": \"\"}, "
        #     "\"buyer\": {\"name\": \"\", \"address\": \"\"}, \"items\": [{\"name\": \"\", \"quantity\": 0, \"unit\": \"\", \"price\": 0, \"total\": 0}], "
        #     "\"total\": 0, \"vat\": 0, \"city\": \"\""
        #     "}\n"
        #     "Invoice text:\n"
        #     f"{text}\n"
        #     "IMPORTANT: Return ONLY valid JSON. Do NOT add any code block markers, explanations, or comments. The response MUST be ONLY pure JSON."
        # )
        prompt = (
            "Extract invoice data from the following text strictly in this JSON format:\n"
            "{"
            "\"number\": \"\", "
            "\"date\": \"\", "
            "\"supplier\": {\"name\": \"\", \"edrpou\": \"\", \"iban\": \"\", \"address\": \"\"}, "
            "\"buyer\": {\"name\": \"\", \"address\": \"\"}, "
            "\"contract\": \"\", "
            "\"items\": [{\"name\": \"\", \"quantity\": 0, \"unit\": \"\", \"price\": 0, \"total\": 0}], "
            "\"total\": 0, "
            "\"vat\": 0, "
            "\"city\": \"\", "
            "\"responsible_person\": \"\", "
            "\"recipient\": \"\""
            "}\n"
            "If any field is missing or not found in the text, set its value to null.\n"
            "Invoice text:\n"
            f"{text}\n"
            "IMPORTANT: Return ONLY valid JSON. Do NOT add any code block markers, explanations, or comments. The response MUST be ONLY pure JSON."
        )
        messages = [{"role": "user", "content": prompt}]
        response = self.gpt.ask(messages)
        print(f"Response from GPT: {response}")
        return json.loads(response)