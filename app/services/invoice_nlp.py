"""
Phase 4 — NLP Invoice parsing service using HuggingFace Transformers.

Install: pip install transformers sentencepiece pytesseract Pillow pdfminer.six

Models used:
  - NER: dslim/bert-base-NER  (entity extraction)
  - OCR: pytesseract           (image-based invoices)
"""
from transformers import pipeline

_ner = pipeline('ner', model='dslim/bert-base-NER', aggregation_strategy='simple')

def parse_invoice_text(text: str) -> dict:
    entities = _ner(text)
    return {e['entity_group']: e['word'] for e in entities}

def extract_text_from_image(image_path: str) -> str:
    from PIL import Image
    import pytesseract
    return pytesseract.image_to_string(Image.open(image_path))

def extract_text_from_pdf(pdf_path: str) -> str:
    from pdfminer.high_level import extract_text
    return extract_text(pdf_path)
