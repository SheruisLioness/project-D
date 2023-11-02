import os
import subprocess
import smtplib
from email.message import EmailMessage
import uuid
from flask import Blueprint, render_template, redirect, url_for, request, send_file

odttopdf_bp = Blueprint('odttopdf_bp', __name__)

@odttopdf_bp.route('/odttopdf', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_file = request.files['file']
        action = request.form.get('action')

        if input_file:
            unique_filename = str(uuid.uuid4()) + os.path.splitext(input_file.filename)[-1]
            input_filename = os.path.join('uploads', unique_filename)
            input_file.save(input_filename)

            try:
                pdf_filename = os.path.splitext(unique_filename)[0] + '.pdf'
                pdf_filepath = os.path.join('uploads', pdf_filename)
                subprocess.run(['C:\\Program Files\\LibreOffice\\program\\soffice.exe', '--headless', '--convert-to', 'pdf', input_filename, '--outdir', 'uploads'])

                if action == 'send':
                    recipient_email = request.form.get('email')
                    send_email(pdf_filepath, recipient_email)
                    return redirect(url_for('odttopdf_bp.index'))
                elif action == 'download':
                    return send_file(pdf_filepath, as_attachment=True, download_name=pdf_filename)
            except Exception as e:
                return f"Error converting file: {str(e)}"

    return render_template('odttopdf.html')

def send_email(pdf_filepath, recipient_email):
    try:
        msg = EmailMessage()
        msg.set_content('Please find the converted PDF file attached.')
        msg['Subject'] = 'Converted PDF File'
        msg['From'] = 'dconvertz@gmail.com'  # Replace with your Gmail email address
        msg['To'] = recipient_email

        with open(pdf_filepath, 'rb') as file:
            file_data = file.read()
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=os.path.basename(pdf_filepath))

        # SMTP server configuration for Gmail
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'dconvertz@gmail.com'  # Your Gmail email address
        smtp_password = 'aicwueerhuresupz'  # The 16-digit app password you generated

        # Establish a secure session with Gmail's outgoing SMTP server using your Gmail account
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS encryption
        server.login(smtp_username, smtp_password)  # Login to Gmail using the app password

        # Send email
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Error sending email: {str(e)}")

# Run the application
if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)
    app.register_blueprint(odttopdf_bp)

    # Ensure the existence of the 'uploads' directory
    os.makedirs('uploads', exist_ok=True)

    app.run(debug=True)
