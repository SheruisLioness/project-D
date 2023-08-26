from flask import Flask, render_template, request, flash, send_file
from werkzeug.utils import secure_filename
from docx2pdf import convert
import os
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '2208'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_and_download(docx_path, pdf_path):
    try:
        convert(docx_path, pdf_path)
    except Exception as e:
        flash(f'An error occurred while converting {docx_path} to PDF: {e}', 'danger')

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
@app.route('/')
@app.route('/doctopdf', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        threads = []

        for file in request.files.getlist('file'):
            if file and allowed_file(file.filename):
                try:
                    filename = secure_filename(file.filename)
                    docx_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    pdf_filename = filename.rsplit('.', 1)[0] + '.pdf'
                    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)

                    file.save(docx_path)

                    thread = threading.Thread(target=convert_and_download, args=(docx_path, pdf_path))
                    thread.start()
                    threads.append((thread, pdf_path))

                    flash(f'{filename} conversion started!', 'success')
                except Exception as e:
                    flash(f'An error occurred while processing {filename}: {e}', 'danger')

        for thread, pdf_path in threads:
            thread.join()

            if os.path.exists(pdf_path):
                receiver_email = request.form["receiver_email"]
                email_subject = "Converted PDF"
                email_message = "Here's the converted PDF file."

                smtp_server = "smtp.gmail.com"
                smtp_port = 587

                sender_email = "dconvertz@gmail.com"  # Replace with your sender email
                username = "Dconvertz@gmail.com"
                password = "hsqbsglmyyxwwgzb"  # Use the generated app password or your Gmail password
        
                if send_email(sender_email, receiver_email, email_subject, email_message, pdf_path, smtp_server, smtp_port, username, password):
                    flash(f'Email sent to {receiver_email} with the converted PDF!', 'success')
                else:
                    flash('Email could not be sent. Please try again later.', 'danger')

                return send_file(pdf_path, as_attachment=True)

    return render_template('doctopdf.html')

if __name__ == '__main__':
    app.run(debug=True)
