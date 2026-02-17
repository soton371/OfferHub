import aiosmtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from app.core.settings import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.template_dir = Path(__file__).parent.parent / "templates"
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def _render_template(self, template_name: str, context: dict) -> str:
        template = self.env.get_template(template_name)
        return template.render(**context)

    async def send_email(self, recipient_email: str, subject: str, template_name: str, context: dict):
        """
        Send an email using aiosmtplib with HTML content rendered from a Jinja2 template.
        Automatically handles SSL (port 465) vs STARTTLS (port 587).
        """
        try:
            html_content = self._render_template(template_name, context)
            
            message = EmailMessage()
            message["From"] = settings.SENDER_EMAIL
            message["To"] = recipient_email
            message["Subject"] = subject
            message.set_content(html_content, subtype="html")

            # Determine connection security based on port
            use_tls = settings.SMTP_PORT == 465
            start_tls = settings.SMTP_PORT == 587

            # Create a secure SSL context using certifi to avoid "unable to get local issuer certificate" errors on macOS
            import ssl
            import certifi
            
            # Create a default context but load CA certificates from certifi
            tls_context = ssl.create_default_context(cafile=certifi.where())

            if use_tls:
                await aiosmtplib.send(
                    message,
                    hostname=settings.SMTP_HOST,
                    port=settings.SMTP_PORT,
                    username=settings.SENDER_EMAIL,
                    password=settings.SMTP_PASSWORD,
                    use_tls=True,
                    tls_context=tls_context,
                )
            else:
                # For port 587 (STARTTLS) or others (25, 2525), we connect first then upgrade
                await aiosmtplib.send(
                    message,
                    hostname=settings.SMTP_HOST,
                    port=settings.SMTP_PORT,
                    username=settings.SENDER_EMAIL,
                    password=settings.SMTP_PASSWORD,
                    use_tls=False,
                    start_tls=start_tls,
                    tls_context=tls_context,
                )
                
            logger.info(f"Email sent successfully to {recipient_email}")
            
        except aiosmtplib.SMTPException as e:
            logger.error(f"SMTP error sending email to {recipient_email}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send email"
            )
        except Exception as e:
            logger.error(f"Unexpected error sending email to {recipient_email}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send email"
            )

email_service = EmailService()
