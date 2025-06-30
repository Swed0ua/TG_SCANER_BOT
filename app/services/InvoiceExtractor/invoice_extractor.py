from ..ChatGPTService.chat_gpt_service import ChatGPTService
from ..OCR.ocr_service import OCRService
import json

class InvoiceExtractor:
    def __init__(self, api_key: str):
        self.ocr = OCRService()
        self.gpt = ChatGPTService(api_key=api_key)

    def extract_invoice(self, image_path: str) -> dict:
        text = self.ocr.extract_text(image_path)

        prompt = (
            "Extract all invoice data from the following text strictly in this JSON format:\n"
            "{\n"
            "\"number\": \"\", \n"
            "\"date\": \"\", \n"
            "\"supplier\": {\"name\": \"\", \"edrpou\": \"\", \"iban\": \"\", \"address\": \"\"}, \n"
            "\"buyer\": {\"name\": \"\", \"address\": \"\"}, \n"
            "\"contract\": \"\", \n"
            "\"items\": [\n"
            "    {\"name\": \"\", \"quantity\": 0, \"unit\": \"\", \"price\": 0, \"total\": 0}\n"
            "], \n"
            "\"total\": 0, \n"
            "\"vat\": 0, \n"
            "\"city\": \"\", \n"
            "\"responsible_person\": \"\", \n"
            "\"recipient\": \"\"\n"
            "}\n\n"
            "💡 Notes:\n"
            "- Always extract full list of items from the invoice. DO NOT leave `items` as [null].\n"
            "- Each item must contain:\n"
            "  * `name`: name of the product or service\n"
            "  * `quantity`: numerical amount\n"
            "  * `unit`: unit of measure (e.g., 'шт', 'kg')\n"
            "  * `price`: unit price including VAT\n"
            "  * `total`: total cost for this item (quantity × price)\n"
            "- If the unit is not clearly mentioned, default to `\"шт\"`.\n"
            "- Extract values exactly as shown in the invoice text.\n"
            "- Do NOT include subtotals, totals or any row that is not an actual product or service.\n"
            "- If a field is completely missing in the invoice, set it to `null`.\n\n"
            "Invoice text:\n"
            f"{text}\n"
            "Return ONLY valid JSON. Do NOT include any code block markers, explanations or extra text."
        )

        
        messages = [{"role": "user", "content": prompt}]
        response = self.gpt.ask(messages)
        print(f"Response from GPT: {response}") 
        return json.loads(response)