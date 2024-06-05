import os
import extract_msg
import csv
import re
from urllib.parse import urlparse
from spacy_extractor import SpacyExtractor

class Main:
    def __init__(self, directory_path, output_csv_path, label):
        self.directory_path = directory_path
        self.output_csv_path = output_csv_path
        self.label = label
        self.column_names = ["Sender", "Recipients", "Subject", "Date", "Address", "Phone Number", "Fax Number", "Position", "Company Name", "Links", "Label Entity"]
        self.spacy_extractor = SpacyExtractor()

        print("The directory path is:", self.directory_path)
        print("Extracting information from the emails")

    def create_csv(self):
        try:
            with open(self.output_csv_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.column_names)
            print(f"CSV file created successfully at {self.output_csv_path} with columns {self.column_names}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def extract_msg_info(self):
        for filename in os.listdir(self.directory_path):
            if filename.endswith(".msg"):
                msg_path = os.path.join(self.directory_path, filename)
                msg = extract_msg.Message(msg_path)
                sender = msg.sender
                recipients = self.extract_recipients(msg.recipients)
                subject = msg.subject
                date = msg.date
                body = msg.body
                self.nlp_extract(sender, recipients, subject, date, body)

    def extract_recipients(self, recipients):
        if not recipients:
            return "-"
        recipient_list = []
        for recipient in recipients:
            recipient_list.append(recipient.email)
        return ", ".join(recipient_list)

    def extract_links(self, text):
        pattern = r'(https?://[^\s]+)'
        links = re.findall(pattern, text)
        return links

    def infer_company_from_links(self, links):
        for link in links:
            domain = urlparse(link).netloc
            if domain:
                # Extract the second-level domain as a simple heuristic for the company name
                parts = domain.split('.')
                if len(parts) >= 2:
                    return parts[-2]
        return ""

    def infer_company_from_email(self, email):
        domain = email.split('@')[-1]
        parts = domain.split('.')
        if len(parts) >= 2:
            return parts[-2]
        return ""

    def extract_phone_and_fax(self, text):
        phone_pattern = r"(\+?\d[\d -]{7,}\d)"
        fax_pattern = r"(fax[:\s]*\+?\d[\d -]{7,}\d)"
        
        phone_numbers = re.findall(phone_pattern, text)
        fax_numbers = re.findall(fax_pattern, text, re.IGNORECASE)

        # Clean and differentiate fax numbers from phone numbers
        fax_numbers = [fax.replace("fax", "").strip() for fax in fax_numbers]
        phone_numbers = [phone for phone in phone_numbers if phone not in fax_numbers]

        phone_number = phone_numbers[0] if phone_numbers else ""
        fax_number = fax_numbers[0] if fax_numbers else ""

        return phone_number, fax_number

    def nlp_extract(self, sender, recipients, subject, date, body):
        address = self.spacy_extractor.extract_address(body)
        phone_number, fax_number = self.extract_phone_and_fax(body)
        position = self.spacy_extractor.extract_position(body)
        company_name = self.spacy_extractor.extract_company_name(body)
        links = self.extract_links(body)
        links_str = ", ".join(links)

           
        
        data = [sender, recipients, subject, date, address, phone_number, fax_number, position, company_name, links_str, self.label]
        self.write(data)

    def write(self, data):
        try:
            with open(self.output_csv_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data)
        except Exception as e:
            print(f"An error occurred while writing data: {e}")

    def extract(self):
        self.create_csv()
        self.extract_msg_info()