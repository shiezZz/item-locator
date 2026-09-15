"""
email_utils.py
Sends verification codes via Gmail SMTP.
"""

import smtplib
import ssl
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.environ.get("GMAIL_SENDER")
APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD") 


def send_verification_email(to_email: str, code: str):
    msg = MIMEText(f"Your Item Locator verification code is: {code}")
    msg["Subject"] = "Verify your Item Locator account"
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())