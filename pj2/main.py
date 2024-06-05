import re
import os
from openai import OpenAI
import spacy
import extract_msg
import csv
from spacy_extractor import SpacyExtractor

# Set your OpenAI API key directly

class Main:
    def __init__(self, directory_path, output_csv_path, label):
        self.directory_path = directory_path
        self.output_csv_path = output_csv_path
        self.label = label
        self.column_names = ["Sender", "Recipients", "Subject", "Date", "Address", "Phone Number", "Position", "Company Name", "Links", "Contains Photo", "Label Entity"]
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

    def nlp_extract(self, sender, recipients, subject, date, body):
        address = self.spacy_extractor.extract_address(body)
        phone_number = self.spacy_extractor.extract_phone_number(body)
        position, company_name = self.extract_with_chatgpt(body)
        links = self.extract_links(body)
        contains_photo = self.check_for_photos(body)
        
        data = [sender, recipients, subject, date, address, phone_number, position, company_name, links, contains_photo, self.label]
        self.write(data)

    def extract_with_chatgpt(self, body):  
        client = OpenAI(api_key="sk-proj-9I75H8XxKPVJxD42kLlWT3BlbkFJBgZT78wsiQcYfasbRZfq")
        prompt = f"""
        Extract the job title and company name from the following text:
        
        {body}
        
        Provide the output in the following format:
        Job Title: [Extracted Job Title]
        Company Name: [Extracted Company Name]
        """  
        completion = client.chat.completions.create( 
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a data extraction assistant, skilled in extracting job titles and company names from text."},
                {"role": "user", "content": prompt}
            ]
        )
        extracted_text = completion.choices[0].message.content
        formatted_text = extracted_text.split("\n") 
        position = formatted_text[0].split(": ")[1] 
        company_name = formatted_text[1].split(": ")[1]  
        return position, company_name
        

    def extract_links(self, body):
        links = re.findall(r'(https?://\S+)', body)
        return ", ".join(links) if links else "-"

    def check_for_photos(self, body):
        # Simple check for common photo file extensions
        photo_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
        contains_photo = any(ext in body for ext in photo_extensions)
        return "Yes" if contains_photo else "No"

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