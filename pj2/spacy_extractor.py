import re
import spacy
from spacy import displacy

class SpacyExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")

    def preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\b(?:llc|inc|co|ltd|corp)\b', '', text)  # Remove common company suffixes
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
        return text

    def extract_address(self, body):
        body = self.preprocess_text(body)
        doc = self.nlp(body)
        addresses = [ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC", "FAC")]
        return addresses

    def extract_phone_number(self, body):
        pattern = r"(\+?\d[\d -]{7,}\d)"
        matches = re.findall(pattern, body)
        return matches 

    def visualize_entities(self, body):
        doc = self.nlp(body)
        displacy.render(doc, style="ent")