from ..ChatGPTService.chat_gpt_service import ChatGPTService
from ..OCR.ocr_service import OCRService
import json

class InvoiceExtractor:
    def __init__(self, api_key: str):
        self.ocr = OCRService()
        self.gpt = ChatGPTService(api_key=api_key)

    def extract_invoice(self, image_path: str) -> dict:
        prompt = (
            "You are a strict document parser. Extract all invoice or receipt data from this image. "
            "Return ONLY valid JSON using this structure:\n\n"
            "{\n"
            "  \"type\": \"invoice\" or \"receipt\",\n"
            "  \"number\": \"\",\n"
            "  \"date\": \"\",\n"
            "  \"supplier\": {\"name\": \"\", \"edrpou\": \"\", \"iban\": null, \"address\": \"\"},\n"
            "  \"buyer\": {\"name\": null, \"address\": null},\n"
            "  \"cashier\": \"\",\n"
            "  \"payment_method\": \"\",\n"
            "  \"payment_system\": \"\",\n"
            "  \"card_last4\": \"\",\n"
            "  \"items\": [\n"
            "    {\"name\": \"\", \"quantity\": 0, \"unit\": \"шт\", \"price\": 0, \"total\": 0}\n"
            "  ],\n"
            "  \"discount\": 0,\n"
            "  \"rounding\": 0,\n"
            "  \"total\": 0,\n"
            "  \"vat\": 0,\n"
            "  \"city\": \"\",\n"
            "  \"responsible_person\": null,\n"
            "  \"recipient\": null\n"
            "}\n\n"
            "STRICT RULES:\n"
            "- Extract only what's clearly visible in the image.\n"
            "- No assumptions or inventions.\n"
            "- If any field is missing, set it to null or 0.\n"
            "- Round numbers to 2 decimals.\n"
            "- Match quantity × price = total if possible.\n"
            "- Return ONLY JSON. No explanations, comments or markdown formatting."
        )

        print(f"Sending image to GPT for Vision-based extraction: {image_path}")
        response = self.gpt.ask_with_image(image_path, prompt)
        print(f"Response from GPT Vision: {response}")
        return json.loads(response)