import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

sender_email = os.environ["EMAIL_ADDRESS"]
sender_password = os.environ["EMAIL_PASSWORD"]
receiver_email = sender_email


subject = "Automated Email from GitHub Actions"
body = "Hey! This is a test email sent by a Python script via GitHub Actions."

# Create the email message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

# Send the email using Gmail SMTP
try:
    with smtplib.SMTP_SSL("smtps.platon.sk", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully.")
except Exception as e:
    print(f"Error sending email: {e}")
