import os

from dotenv import load_dotenv
from pdfminer.high_level import extract_text
import textract
import docx2txt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL", None)
SENDER_APP_PASSWORD = os.getenv("SENDER_APP_PASSWORD", None)

# Function to extract text from DOCX file
def extract_text_from_docx(file):
    my_text = docx2txt.process(file)
    return my_text

# Function to extract text from PDF file
def extract_text_from_pdf(file):
    text = extract_text(file)
    os.remove(file)
    return text


# Function to extract text from DOC file
def extract_text_from_doc(file):
    text = textract.process(file)
    text = text.decode("utf-8")
    os.remove(file)
    return text
def send_email_notification(receiver_email, subject, message):

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        s.starttls()
        s.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
        s.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())