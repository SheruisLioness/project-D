import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_email(sender_email, receiver_email, subject, message, pdf_path, smtp_server, smtp_port, username, password):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        body = MIMEText(message)
        msg.attach(body)

        with open(pdf_path, 'rb') as pdf_file:
            pdf_attachment = MIMEApplication(pdf_file.read(), _subtype='pdf')
            pdf_attachment.add_header('content-disposition', f'attachment; filename={os.path.basename(pdf_path)}')
            msg.attach(pdf_attachment)

        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()
        smtp.login(username, password)
        smtp.sendmail(sender_email, receiver_email, msg.as_string())
        smtp.quit()
        return True
    except Exception as e:
        print(f"Email sending error: {e}")
        return False
