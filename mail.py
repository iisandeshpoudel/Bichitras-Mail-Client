import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email credentials and settings
sender_email = "bichitras@bichitras.com"
password = "randomnessinpokhara"
recipient_email = "recipient@example.com"  # Replace with the actual recipient's email
smtp_server = "mail.privateemail.com"
port = 465  # SSL port for SMTP

# Create email message
msg = MIMEMultipart("alternative")
msg["Subject"] = "Bichitras - Modern Art & Design"
msg["From"] = sender_email
msg["To"] = recipient_email

# HTML content
html_content = """
<!DOCTYPE html>
<html>
<head>
    <!-- Your HTML code goes here -->
</head>
<body>
    <!-- The rest of your HTML content goes here -->
</body>
</html>
"""

# Attach the HTML content to the email
msg.attach(MIMEText(html_content, "html"))

# Connect to the server and send the email
try:
    server = smtplib.SMTP_SSL(smtp_server, port)
    server.login(sender_email, password)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")
finally:
    server.quit()
