from fastapi import HTTPException, status
import smtplib
from email.message import EmailMessage
from app.core.settings import settings

def send_mail(recipientMail: str, subject: str, content: str):
    try:
        smtpServer = smtplib.SMTP(
            settings.SMTP_HOST, settings.SMTP_PORT)
        smtpServer.starttls()
        smtpServer.login(settings.SENDER_EMAIL,
                         settings.SMTP_PASSWORD)
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['from'] = settings.SENDER_EMAIL
        msg['to'] = recipientMail
        msg.set_content(content)
        smtpServer.send_message(msg)
    except Exception as e:
        print(f"sendOTPSmtp e: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send mail")


# eta dekhte hobe