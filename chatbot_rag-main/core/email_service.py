#!/usr/bin/env python3
"""
Email Service Module
Handles sending emails for password reset and other notifications
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the parent directory
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email = os.getenv('GMAIL_EMAIL')
        self.password = os.getenv('GMAIL_APP_PASSWORD')
        self.frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
        
        if not self.email or not self.password:
            logger.warning("Gmail credentials not configured. Email functionality will be disabled.")
    
    def send_password_reset_email(self, recipient_email: str, reset_token: str, user_name: str = None) -> bool:
        """Send password reset email"""
        if not self.email or not self.password:
            logger.error("Gmail credentials not configured")
            return False
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = "Password Reset - Coffee AI"
            message["From"] = self.email
            message["To"] = recipient_email
            
            # Create reset URL
            reset_url = f"{self.frontend_url}/reset-password?token={reset_token}"
            
            # Create the plain-text and HTML version of your message
            text = f"""
            Hello {user_name or 'there'},
            
            You requested a password reset for your Coffee AI account.
            
            Click the following link to reset your password:
            {reset_url}
            
            This link will expire in 1 hour for security reasons.
            
            If you didn't request this password reset, please ignore this email.
            
            Best regards,
            Coffee AI Team
            """
            
            html = f"""
            <html>
              <body>
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                  <h2 style="color: #8B4513;">Password Reset - Coffee AI</h2>
                  
                  <p>Hello {user_name or 'there'},</p>
                  
                  <p>You requested a password reset for your Coffee AI account.</p>
                  
                  <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_url}" 
                       style="background-color: #8B4513; color: white; padding: 12px 24px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                      Reset Password
                    </a>
                  </div>
                  
                  <p style="color: #666; font-size: 14px;">
                    This link will expire in 1 hour for security reasons.
                  </p>
                  
                  <p style="color: #666; font-size: 14px;">
                    If you didn't request this password reset, please ignore this email.
                  </p>
                  
                  <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                  
                  <p style="color: #999; font-size: 12px;">
                    Best regards,<br>
                    Coffee AI Team
                  </p>
                </div>
              </body>
            </html>
            """
            
            # Turn these into plain/html MIMEText objects
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            
            # Add HTML/plain-text parts to MIMEMultipart message
            message.attach(part1)
            message.attach(part2)
            
            # Create secure connection with server and send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email, self.password)
                server.sendmail(self.email, recipient_email, message.as_string())
            
            logger.info(f"Password reset email sent successfully to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send password reset email to {recipient_email}: {str(e)}")
            return False
    
    def send_password_reset_confirmation_email(self, recipient_email: str, user_name: str = None) -> bool:
        """Send password reset confirmation email"""
        if not self.email or not self.password:
            logger.error("Gmail credentials not configured")
            return False
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = "Password Reset Successful - Coffee AI"
            message["From"] = self.email
            message["To"] = recipient_email
            
            # Create the plain-text and HTML version of your message
            text = f"""
            Hello {user_name or 'there'},
            
            Your password has been successfully reset for your Coffee AI account.
            
            If you didn't make this change, please contact our support team immediately.
            
            Best regards,
            Coffee AI Team
            """
            
            html = f"""
            <html>
              <body>
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                  <h2 style="color: #8B4513;">Password Reset Successful - Coffee AI</h2>
                  
                  <p>Hello {user_name or 'there'},</p>
                  
                  <p>Your password has been successfully reset for your Coffee AI account.</p>
                  
                  <div style="background-color: #d4edda; border: 1px solid #c3e6cb; 
                              color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <strong>✓ Password Reset Complete</strong><br>
                    You can now log in with your new password.
                  </div>
                  
                  <p style="color: #dc3545; font-weight: bold;">
                    If you didn't make this change, please contact our support team immediately.
                  </p>
                  
                  <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                  
                  <p style="color: #999; font-size: 12px;">
                    Best regards,<br>
                    Coffee AI Team
                  </p>
                </div>
              </body>
            </html>
            """
            
            # Turn these into plain/html MIMEText objects
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            
            # Add HTML/plain-text parts to MIMEMultipart message
            message.attach(part1)
            message.attach(part2)
            
            # Create secure connection with server and send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email, self.password)
                server.sendmail(self.email, recipient_email, message.as_string())
            
            logger.info(f"Password reset confirmation email sent successfully to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send password reset confirmation email to {recipient_email}: {str(e)}")
            return False
