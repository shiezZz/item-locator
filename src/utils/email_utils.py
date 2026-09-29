"""
email_utils.py
Sends verification codes via Gmail SMTP.
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from src.config import GMAIL_SENDER, GMAIL_APP_PASSWORD


def send_verification_email(to_email: str, code: str):
    msg = MIMEText(f"Your Item Locator verification code is: {code}")
    msg["Subject"] = "Verify your Item Locator account"
    msg["From"] = GMAIL_SENDER
    msg["To"] = to_email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(GMAIL_SENDER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_SENDER, to_email, msg.as_string())