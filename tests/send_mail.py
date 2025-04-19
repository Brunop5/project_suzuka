import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Your email and app password
sender_email = "bruno@platek.sk"
sender_password = "2ZSsATNUnr"
receiver_email = "bruno@platek.sk"  # or someone else's

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
