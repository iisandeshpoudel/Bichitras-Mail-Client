import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class EmailConfig:
    smtp_server: str
    port: int
    email: str
    password: str
    use_ssl: bool = True

class EmailHandler:
    def __init__(self, config: EmailConfig):
        self.config = config
        self.server = None

    def connect(self) -> tuple[bool, str]:
        try:
            if self.config.use_ssl:
                self.server = smtplib.SMTP_SSL(self.config.smtp_server, self.config.port)
            else:
                self.server = smtplib.SMTP(self.config.smtp_server, self.config.port)
                self.server.starttls()
            
            self.server.login(self.config.email, self.config.password)
            return True, "Connected successfully"
        except Exception as e:
            return False, f"Connection failed: {str(e)}"

    def send_email(self, recipients: List[str], subject: str, html_content: str) -> tuple[bool, str]:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.config.email
            msg["To"] = ", ".join(recipients)
            
            msg.attach(MIMEText(html_content, "html"))
            
            if not self.server:
                success, message = self.connect()
                if not success:
                    return False, message

            self.server.sendmail(self.config.email, recipients, msg.as_string())
            return True, "Email sent successfully!"
        except Exception as e:
            return False, f"Error sending email: {str(e)}"

    def disconnect(self):
        if self.server:
            self.server.quit()
