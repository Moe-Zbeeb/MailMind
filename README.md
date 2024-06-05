# MailMind

## Overview

The Email Information Extractor is a tool designed to extract important information from `.msg` email files. It uses natural language processing (NLP) techniques to identify and extract key details such as:

- Sender
- Recipients
- Subject
- Date
- Address
- Phone Number
- Position
- Company Name
- Label Entity

## Key Features

1. **Natural Language Processing (NLP)**:
   - Utilizes the spaCy library to process email bodies and extract addresses, phone numbers, positions, and company names.

2. **Integration with OpenAI GPT-3.5-turbo**:
   - Enhances extraction capabilities, especially for job titles and company names, by leveraging the power of the GPT-3.5-turbo model.

3. **Processing of `.msg` Files**:
   - Reads and processes `.msg` files to extract the necessary information.

## Workflow

1. **Initialize the Application**:
   - The application is initialized with a directory path containing `.msg` files, an output CSV file path, and a label entity.

2. **Create CSV File**:
   - A CSV file is created to store the extracted information, with columns for sender, recipients, subject, date, address, phone number, position, company name, and label entity.

3. **Extract Information from Emails**:
   - The application iterates through the `.msg` files in the specified directory, extracting relevant details using spaCy and OpenAI's GPT-3.5-turbo.

4. **Natural Language Processing**:
   - spaCy is used to process the email body text and extract addresses and phone numbers.
   - OpenAI GPT-3.5-turbo is used to extract job titles and company names by analyzing the email body text.

5. **Save Extracted Information**:
   - The extracted information is saved to the CSV file for further analysis or processing.

## Usage

1. **Set Up Environment**:
   - Ensure that the necessary dependencies (spaCy, OpenAI API client, etc.) are installed.
   - Export the OpenAI API key as an environment variable.

2. **Run the Application**:
   - Execute the driver script to start processing the emails and extracting information.

## Example

To run the application, follow these steps:

1. Export your OpenAI API key:
    ```sh
    export OPENAI_API_KEY='your-api-key-here'
    ```

2. Run the driver script:
    ```sh
    /bin/python3 /path/to/driver.py
    ```

