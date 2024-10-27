import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class EmailTemplate:
    name: str
    subject: str
    content: str
    description: Optional[str] = None

class TemplateManager:
    def __init__(self):
        self.templates_file = "templates.json"
        self.templates: Dict[str, EmailTemplate] = {}
        self.load_templates()

    def load_templates(self):
        if os.path.exists(self.templates_file):
            with open(self.templates_file, 'r') as f:
                data = json.load(f)
                self.templates = {
                    name: EmailTemplate(**template_data)
                    for name, template_data in data.items()
                }

    def save_templates(self):
        with open(self.templates_file, 'w') as f:
            data = {
                name: {
                    'name': template.name,
                    'subject': template.subject,
                    'content': template.content,
                    'description': template.description
                }
                for name, template in self.templates.items()
            }
            json.dump(data, f, indent=4)

    def add_template(self, template: EmailTemplate):
        self.templates[template.name] = template
        self.save_templates()

    def get_template(self, name: str) -> Optional[EmailTemplate]:
        return self.templates.get(name)

    def get_all_templates(self) -> List[EmailTemplate]:
        return list(self.templates.values())

    def delete_template(self, name: str):
        if name in self.templates:
            del self.templates[name]
            self.save_templates()
