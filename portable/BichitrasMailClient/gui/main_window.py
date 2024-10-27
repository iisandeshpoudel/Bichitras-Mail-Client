from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QTextEdit, QLineEdit, QLabel, QMessageBox,
                           QTabWidget, QToolBar, QStatusBar, QSpacerItem, QSizePolicy,
                           QDialog, QComboBox, QDialogButtonBox, 
                           QListWidget, QSplitter, QMenu)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QUrl, QTimer
from PyQt6.QtGui import QIcon, QAction, QPixmap
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from email_handler import EmailHandler, EmailConfig
from .styles import STYLE_SHEET
from .template_manager import TemplateManager, EmailTemplate
from .loading_dialog import LoadingDialog
import requests
import io

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bichitras Mail Client")
        self.setMinimumSize(1200, 800)  # Increased minimum size
        self.resize(1400, 900)  # Default size
        self.setStyleSheet(STYLE_SHEET)
        
        self.template_manager = TemplateManager()
        
        # Initialize email handler
        self.email_config = EmailConfig(
            smtp_server="mail.privateemail.com",
            port=465,
            email="bichitras@bichitras.com",
            password="randomnessinpokhara"
        )
        self.email_handler = EmailHandler(self.email_config)
        
        self.setup_ui()
        self.setup_toolbar()
        self.setup_statusbar()
        self.load_logo()

    def load_logo(self):
        try:
            # Create a container widget for logo and text
            logo_container = QWidget()
            logo_layout = QVBoxLayout(logo_container)
            logo_layout.setSpacing(10)
            logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Download and set logo
            logo_url = "https://utfs.io/f/uCCvk88x4gvM3puo5JI2lfhitzaQJEejZDXdxGvy69UkBMr8"
            response = requests.get(logo_url)
            logo_data = response.content
            
            pixmap = QPixmap()
            pixmap.loadFromData(logo_data)
            
            # Scale logo to appropriate size
            scaled_pixmap = pixmap.scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio, 
                                        Qt.TransformationMode.SmoothTransformation)
            
            # Create and set up logo label
            self.logo_label = QLabel()
            self.logo_label.setPixmap(scaled_pixmap)
            self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.logo_label.setStyleSheet("""
                QLabel {
                    background: transparent;
                    padding: 10px;
                }
            """)
            
            # Create and set up client name label
            client_name = QLabel("Bichitras Mail Client")
            client_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
            client_name.setStyleSheet("""
                QLabel {
                    color: #9832C1;
                    font-size: 24px;
                    font-weight: bold;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    padding: 5px;
                    background: transparent;
                }
            """)
            
            # Add both to the container
            logo_layout.addWidget(self.logo_label)
            logo_layout.addWidget(client_name)
            
            # Add the container to the main layout
            self.main_layout.insertWidget(0, logo_container)
            
        except Exception as e:
            print(f"Error loading logo: {e}")

    def setup_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))
        
        # Add toolbar actions
        new_email_action = QAction("New Email", self)
        new_email_action.triggered.connect(self.clear_fields)
        toolbar.addAction(new_email_action)
        
        save_template_action = QAction("Save as Template", self)
        save_template_action.triggered.connect(self.save_as_template)
        toolbar.addAction(save_template_action)
        
        load_template_action = QAction("Load Template", self)
        load_template_action.triggered.connect(self.load_template)
        toolbar.addAction(load_template_action)
        
        self.addToolBar(toolbar)

    def setup_statusbar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Email composition area
        compose_widget = QWidget()
        compose_layout = QVBoxLayout(compose_widget)
        compose_layout.setSpacing(15)

        # Recipients
        recipients_layout = QHBoxLayout()
        recipients_label = QLabel("To:")
        recipients_label.setFixedWidth(60)
        self.recipients_input = QLineEdit()
        self.recipients_input.setPlaceholderText("Enter email addresses separated by commas")
        recipients_layout.addWidget(recipients_label)
        recipients_layout.addWidget(self.recipients_input)
        compose_layout.addLayout(recipients_layout)

        # Subject
        subject_layout = QHBoxLayout()
        subject_label = QLabel("Subject:")
        subject_label.setFixedWidth(60)
        self.subject_input = QLineEdit()
        subject_layout.addWidget(subject_label)
        subject_layout.addWidget(self.subject_input)
        compose_layout.addLayout(subject_layout)

        # Add template selector
        template_layout = QHBoxLayout()
        template_label = QLabel("Template:")
        template_label.setFixedWidth(60)
        self.template_combo = QComboBox()
        self.update_template_list()
        self.template_combo.currentTextChanged.connect(self.on_template_selected)
        template_layout.addWidget(template_label)
        template_layout.addWidget(self.template_combo)
        compose_layout.insertLayout(0, template_layout)

        # Create tabs for HTML editor and preview
        self.content_tabs = QTabWidget()
        
        # HTML Content tab
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("Enter your HTML content here...")
        self.content_edit.setMinimumHeight(300)
        self.content_edit.textChanged.connect(self.update_preview)  # Auto-update preview
        editor_layout.addWidget(self.content_edit)
        
        self.content_tabs.addTab(editor_widget, "HTML Editor")

        # Preview tab
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        
        self.preview_widget = QTextEdit()
        self.preview_widget.setReadOnly(True)
        self.preview_widget.setMinimumHeight(300)
        self.preview_widget.setStyleSheet("""
            QTextEdit {
                background-color: white;
                padding: 20px;
            }
        """)
        preview_layout.addWidget(self.preview_widget)
        
        self.content_tabs.addTab(preview_widget, "Preview")
        
        # Add tabs to compose layout
        compose_layout.addWidget(self.content_tabs)
        
        # Connect tab changed signal
        self.content_tabs.currentChanged.connect(self.on_tab_changed)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.send_button = QPushButton("Send Email")
        self.send_button.setFixedWidth(120)
        self.send_button.clicked.connect(self.send_email)
        
        self.clear_button = QPushButton("Clear")
        self.clear_button.setFixedWidth(120)
        self.clear_button.clicked.connect(self.clear_fields)
        
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.send_button)
        compose_layout.addLayout(button_layout)

        self.main_layout.addWidget(compose_widget)

    def update_template_list(self):
        self.template_combo.clear()
        self.template_combo.addItem("Select Template...")
        for template in self.template_manager.get_all_templates():
            self.template_combo.addItem(template.name)

    def on_template_selected(self, template_name):
        if template_name != "Select Template...":
            template = self.template_manager.get_template(template_name)
            if template:
                self.subject_input.setText(template.subject)
                self.content_edit.setPlainText(template.content)

    def save_as_template(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Save as Template")
        layout = QVBoxLayout(dialog)

        name_input = QLineEdit()
        name_input.setPlaceholderText("Template Name")
        layout.addWidget(name_input)

        desc_input = QTextEdit()
        desc_input.setPlaceholderText("Template Description")
        desc_input.setMaximumHeight(100)
        layout.addWidget(desc_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            template = EmailTemplate(
                name=name_input.text(),
                subject=self.subject_input.text(),
                content=self.content_edit.toPlainText(),
                description=desc_input.toPlainText()
            )
            self.template_manager.add_template(template)
            self.update_template_list()

    def load_template(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Load Template")
        layout = QVBoxLayout(dialog)

        template_list = QListWidget()
        for template in self.template_manager.get_all_templates():
            template_list.addItem(template.name)
        layout.addWidget(template_list)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected = template_list.currentItem()
            if selected:
                template = self.template_manager.get_template(selected.text())
                if template:
                    self.subject_input.setText(template.subject)
                    self.content_edit.setPlainText(template.content)
                    self.update_preview()  # Update preview when template is loaded

    def update_preview(self):
        """Update the preview whenever HTML content changes"""
        html_content = self.content_edit.toPlainText()
        
        # Add default styling for better preview
        styled_html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333333;
                    margin: 0;
                    padding: 20px;
                }}
                a {{ color: #9832C1; }}
                h1, h2, h3, h4, h5, h6 {{
                    color: #9832C1;
                    margin-top: 20px;
                    margin-bottom: 10px;
                }}
                p {{ margin-bottom: 15px; }}
                img {{ max-width: 100%; height: auto; }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-bottom: 15px;
                }}
                th, td {{
                    border: 1px solid #E0E0E0;
                    padding: 8px;
                    text-align: left;
                }}
                th {{ background-color: #F5F5F5; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        self.preview_widget.setHtml(styled_html)

    def on_tab_changed(self, index):
        """Handle tab changes"""
        if index == 1:  # Preview tab
            self.update_preview()
            self.status_bar.showMessage("Preview mode")
        else:
            self.status_bar.showMessage("Edit mode")

    def animate_button(self, button, pressed=False):
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(100)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        current_geometry = button.geometry()
        if pressed:
            animation.setEndValue(current_geometry.adjusted(0, 2, 0, 2))
        else:
            animation.setEndValue(current_geometry.adjusted(0, -2, 0, -2))
        
        animation.start()

    def send_email(self):
        self.animate_button(self.send_button, True)
        recipients = [email.strip() for email in self.recipients_input.text().split(",")]
        subject = self.subject_input.text()
        html_content = self.content_edit.toPlainText()

        if not recipients or not subject or not html_content:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            self.status_bar.showMessage("Ready")
            self.animate_button(self.send_button, False)
            return

        # Show loading dialog
        self.loading_dialog = LoadingDialog(self)
        self.loading_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.loading_dialog.center_on_parent()  # Center the dialog
        self.loading_dialog.show()
        
        # Use timer to prevent UI freeze
        QTimer.singleShot(100, lambda: self.perform_send_email(recipients, subject, html_content))

    def perform_send_email(self, recipients, subject, html_content):
        success, message = self.email_handler.send_email(recipients, subject, html_content)
        
        # Close loading dialog
        self.loading_dialog.close()
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.clear_fields()
            self.status_bar.showMessage("Email sent successfully!")
        else:
            QMessageBox.critical(self, "Error", message)
            self.status_bar.showMessage("Failed to send email")
        
        self.animate_button(self.send_button, False)

    def clear_fields(self):
        self.animate_button(self.clear_button, True)
        self.recipients_input.clear()
        self.subject_input.clear()
        self.content_edit.clear()
        self.update_preview()  # Update preview when fields are cleared
        self.status_bar.showMessage("Ready")
        self.animate_button(self.clear_button, False)

    def closeEvent(self, event):
        self.email_handler.disconnect()
        event.accept()

