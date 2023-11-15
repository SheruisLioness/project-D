#email_utils.py
import smtplib
from email.message import EmailMessage
import os

def send_email(pdf_filepath, recipient_email, smtp_username, smtp_password):
    try:
        msg = EmailMessage()
        msg.set_content('Please find the converted PDF file attached.')
        msg['Subject'] = 'Converted PDF File'
        msg['From'] = 'dconvertz@gmail.com'  
        msg['To'] = recipient_email

        with open(pdf_filepath, 'rb') as file:
            file_data = file.read()
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=os.path.basename(pdf_filepath))

        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  
        server.login(smtp_username, smtp_password)  

        # Send email
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Error sending email: {str(e)}")
