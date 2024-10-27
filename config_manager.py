import json
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class EmailSettings:
    smtp_server: str
    port: int
    email: str
    password: str
    use_ssl: bool = True

class ConfigManager:
    def __init__(self):
        self.config_file = "config.json"
        self.default_settings = {
            "smtp_server": "mail.privateemail.com",
            "port": 465,
            "email": "bichitras@bichitras.com",
            "password": "",  # Don't store password in default settings
            "use_ssl": True
        }
        self.settings = self.load_settings()

    def load_settings(self) -> EmailSettings:
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    return EmailSettings(**data)
            return EmailSettings(**self.default_settings)
        except Exception as e:
            print(f"Error loading settings: {e}")
            return EmailSettings(**self.default_settings)

    def save_settings(self, settings: EmailSettings):
        try:
            with open(self.config_file, 'w') as f:
                json.dump({
                    "smtp_server": settings.smtp_server,
                    "port": settings.port,
                    "email": settings.email,
                    "password": settings.password,
                    "use_ssl": settings.use_ssl
                }, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")
