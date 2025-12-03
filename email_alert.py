import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure info email
EMAIL_SENDER = ""
EMAIL_PASSWORD = ""
EMAIL_RECEIVER = ""

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email_alert(subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print("Warning email has sent!")
    except Exception as e:
        print(f"Error sending email: {e}")
