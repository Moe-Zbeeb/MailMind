import re
import spacy
from spacy.matcher import PhraseMatcher
from fuzzywuzzy import fuzz, process
from spacy import displacy

class SpacyExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        self.job_titles = [
            "Customer Service Agent", "Software Engineer", "Data Scientist", "Product Manager", "Project Manager", 
            "Human Resources Specialist", "Business Analyst", "Marketing Manager", "Sales Representative", 
            "Accountant", "Financial Analyst", "Operations Manager", "Graphic Designer", "UX Designer", "UI Designer",
            "Network Engineer", "Database Administrator", "System Administrator", "IT Support Specialist", "SEO Specialist",
            "Social Media Manager", "Content Writer", "Copywriter", "Editor", "Technical Writer", "Legal Assistant",
            "Paralegal", "Attorney", "Lawyer", "Consultant", "Advisor", "Counselor", "Physician", "Nurse", "Surgeon",
            "Pharmacist", "Research Scientist", "Lab Technician", "Quality Assurance Specialist", "Test Engineer",
            "Mechanical Engineer", "Electrical Engineer", "Civil Engineer", "Biomedical Engineer", "Chemical Engineer",
            "Environmental Engineer", "Industrial Engineer", "Manufacturing Engineer", "Process Engineer", "Production Engineer",
            "Safety Engineer", "Construction Manager", "Architect", "Interior Designer", "Urban Planner", "Landscape Architect",
            "Real Estate Agent", "Broker", "Property Manager", "Appraiser", "Loan Officer", "Mortgage Broker", "Bank Teller",
            "Investment Banker", "Financial Planner", "Wealth Manager", "Insurance Agent", "Actuary", "Underwriter",
            "Claims Adjuster", "Risk Manager", "Supply Chain Manager", "Logistics Coordinator", "Procurement Specialist",
            "Purchasing Agent", "Inventory Manager", "Warehouse Manager", "Shipping Coordinator", "Freight Forwarder",
            "Customs Broker", "Importer", "Exporter", "Retail Manager", "Store Manager", "Merchandiser", "Buyer",
            "Visual Merchandiser", "E-commerce Specialist", "Customer Service Representative", "Technical Support Engineer",
            "Help Desk Specialist", "Field Service Technician", "Installation Technician", "Maintenance Technician", 
            "Service Manager", "Service Coordinator", "Client Relations Manager", "Customer Success Manager",
            "Data Analyst", "UI/UX Developer", "Financial Controller", "Market Research Analyst", "Business Development Manager",
            "Public Relations Specialist", "Brand Manager", "Event Coordinator", "Supply Chain Analyst", "Logistics Manager",
            "Operations Coordinator", "Retail Sales Associate", "Business Consultant", "Investment Analyst", "Financial Adviser",
            "Tax Consultant", "Auditor", "Insurance Broker", "Underwriting Analyst", "Claims Processor", "Risk Analyst",
            "Inventory Control Specialist", "Procurement Manager", "Warehouse Supervisor", "Retail Buyer", "Visual Designer",
            "User Interface Designer", "User Experience Researcher", "Frontend Developer", "Backend Developer", "Full Stack Developer",
            "Quality Assurance Analyst", "Test Analyst", "Mechanical Designer", "Electrical Designer", "Civil Engineering Technician",
            "Biomedical Researcher", "Chemist", "Environmental Scientist", "Industrial Designer", "Manufacturing Technician",
            "Process Improvement Specialist", "Production Supervisor", "Construction Supervisor", "Real Estate Developer",
            "Real Estate Broker", "Property Developer", "Land Surveyor", "Loan Processor", "Mortgage Underwriter", "Credit Analyst",
            "Wealth Advisor", "Risk Management Analyst", "Logistics Analyst", "Purchasing Manager", "Inventory Planner",
            "Retail Merchandising Manager", "E-commerce Manager", "Technical Support Specialist", "Field Service Engineer",
            "Installation Specialist", "Maintenance Supervisor", "Client Services Manager", "Customer Experience Manager",
            "Public Health Specialist", "Clinical Research Coordinator", "Medical Laboratory Technologist", "Pharmacy Technician",
            "Healthcare Administrator", "Nurse Practitioner", "Anesthesiologist", "Radiologist", "Ophthalmologist",
            "Dermatologist", "Orthopedic Surgeon", "Pediatrician", "Cardiologist", "Endocrinologist", "Oncologist",
            "Hematologist", "Gastroenterologist", "Neurologist", "Psychiatrist", "Allergist", "Urologist", "Obstetrician",
            "Gynecologist", "Pathologist", "Family Physician", "Emergency Physician", "Hospitalist", "General Surgeon",
            "Plastic Surgeon", "Medical Examiner", "Forensic Scientist", "Clinical Psychologist", "Neuropsychologist",
            "Counseling Psychologist", "Industrial-Organizational Psychologist", "Educational Psychologist", "Sports Psychologist",
            "Developmental Psychologist", "Art Therapist", "Music Therapist", "Dance Therapist", "Drama Therapist",
            "Recreational Therapist", "Massage Therapist", "Physical Therapist", "Occupational Therapist", "Speech Therapist",
            "Respiratory Therapist", "Radiation Therapist", "Chiropractor", "Dietitian", "Nutritionist", "Clinical Social Worker",
            "Marriage and Family Therapist", "Substance Abuse Counselor", "School Counselor", "Career Counselor",
            "Rehabilitation Counselor", "Genetic Counselor", "Animal Trainer", "Veterinarian", "Zoologist", "Marine Biologist",
            "Wildlife Biologist", "Conservation Scientist", "Ecologist", "Botanist", "Entomologist", "Paleontologist",
            "Geologist", "Astronomer", "Astrophysicist", "Meteorologist", "Oceanographer", "Environmental Engineer",
            "Biomedical Engineer", "Chemical Engineer", "Industrial Engineer", "Manufacturing Engineer", "Nuclear Engineer",
            "Petroleum Engineer", "Materials Engineer", "Mining Engineer", "Agricultural Engineer", "Architectural Engineer",
            "Computer Engineer", "Software Developer", "Data Engineer", "Machine Learning Engineer", "Robotics Engineer",
            "Automation Engineer", "Electronics Engineer", "Power Engineer", "Control Systems Engineer", "Telecommunications Engineer",
            "Wireless Engineer", "Network Security Engineer", "Information Security Analyst", "Cryptography Analyst",
            "Cybersecurity Consultant", "Penetration Tester", "Ethical Hacker", "Forensic Analyst", "Incident Responder",
            "Security Auditor", "Disaster Recovery Specialist", "Disaster Relief Coordinator", "Emergency Management Specialist",
            "Firefighter", "Emergency Medical Technician", "Paramedic", "Search and Rescue Technician", "Disaster Response Team Leader",
            "Volunteer Coordinator", "Community Outreach Coordinator"
        ]
        
        self._create_matchers()

    def _create_matchers(self):
        job_title_patterns = list(self.nlp.pipe(self.job_titles))
        self.matcher.add("JOB_TITLE", None, *job_title_patterns)

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
    
    def extract_position(self, body):
        body = self.preprocess_text(body)
        doc = self.nlp(body)
        matches = self.matcher(doc)
        positions = [doc[start:end].text for match_id, start, end in matches if self.nlp.vocab.strings[match_id] == "JOB_TITLE"]
        return positions

    def extract_company_name(self, body, threshold=80):
        body = self.preprocess_text(body)
        doc = self.nlp(body)
        org_entities = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        
        # Filter confident company names using fuzzy matching
        confident_companies = []
        for entity in org_entities:
            best_match, score = process.extractOne(entity, org_entities, scorer=fuzz.ratio)
            if score >= threshold:
                confident_companies.append(best_match)
        
        return list(set(confident_companies))  # Remove duplicates

    def extract_all_entities(self, body):
        body = self.preprocess_text(body)
        doc = self.nlp(body)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities

    def visualize_entities(self, body):
        doc = self.nlp(body)
        displacy.render(doc, style="ent")

# Example usage
extractor = SpacyExtractor()
text = "Mohamad is applying for a position as a Software Engineer at Google."
print("Job Titles:", extractor.extract_position(text))
print("Company Names:", extractor.extract_company_name(text))
