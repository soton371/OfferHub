import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
import sys
import os

# Add the project root to sys.path so we can import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.shared.email_service import EmailService
from app.core.settings import settings

async def test_email_service_ssl():
    print("Testing SSL (Port 465)...")
    
    # Mock settings to simulate SSL config
    with patch("app.core.settings.settings.SMTP_PORT", 465), \
         patch("app.core.settings.settings.SMTP_HOST", "smtp.example.com"), \
         patch("app.core.settings.settings.SENDER_EMAIL", "test@example.com"), \
         patch("app.core.settings.settings.SMTP_PASSWORD", "secret"), \
         patch("aiosmtplib.send", new_callable=AsyncMock) as mock_send:
        
        # Mock the template rendering to avoid needing actual files
        service = EmailService()
        service._render_template = MagicMock(return_value="<html><body>Hello</body></html>")
        
        await service.send_email("recipient@example.com", "Test Subject", "test_template.html", {})
        
        # Verify aiosmtplib.send was called with use_tls=True
        mock_send.assert_called_once()
        call_kwargs = mock_send.call_args.kwargs
        
        assert call_kwargs["hostname"] == "smtp.example.com"
        assert call_kwargs["port"] == 465
        assert call_kwargs["use_tls"] is True
        print("✅ SSL (Port 465) test passed!")

async def test_email_service_starttls():
    print("Testing STARTTLS (Port 587)...")
    
    # Mock settings to simulate STARTTLS config
    with patch("app.core.settings.settings.SMTP_PORT", 587), \
         patch("app.core.settings.settings.SMTP_HOST", "smtp.example.com"), \
         patch("app.core.settings.settings.SENDER_EMAIL", "test@example.com"), \
         patch("app.core.settings.settings.SMTP_PASSWORD", "secret"), \
         patch("aiosmtplib.send", new_callable=AsyncMock) as mock_send:
        
        # Mock the template rendering
        service = EmailService()
        service._render_template = MagicMock(return_value="<html><body>Hello</body></html>")
        
        await service.send_email("recipient@example.com", "Test Subject", "test_template.html", {})
        
        # Verify aiosmtplib.send was called with use_tls=False, start_tls=True
        mock_send.assert_called_once()
        call_kwargs = mock_send.call_args.kwargs
        
        assert call_kwargs["hostname"] == "smtp.example.com"
        assert call_kwargs["port"] == 587
        assert call_kwargs["use_tls"] is False
        assert call_kwargs["start_tls"] is True
        print("✅ STARTTLS (Port 587) test passed!")

async def main():
    try:
        await test_email_service_ssl()
        await test_email_service_starttls()
        print("\n🎉 All tests passed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
