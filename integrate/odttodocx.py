from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for
import os
from odf import text, teletype
from odf.opendocument import load
from docx import Document
import smtplib
from email.message import EmailMessage

odttodocx_bp = Blueprint('odttodocx', __name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'downloads'
ALLOWED_EXTENSIONS = {'odt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_odt_to_docx(odt_file, docx_file):
    document = load(odt_file)
    content = ""

    for paragraph in document.getElementsByType(text.P):
        content += teletype.extractText(paragraph)

    doc = Document()
    doc.add_paragraph(content)
    doc.save(docx_file)

def send_email(sender_email, recipient_email, subject, body, attachment_path):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    
    with open(attachment_path, 'rb') as file:
        file_data = file.read()
        file_name = os.path.basename(attachment_path)
    
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    smtp_server = 'smtp.gmail.com'  # Gmail SMTP server address
    smtp_port = 587  # Gmail SMTP server port
    smtp_username = 'dconvertz@gmail.com'  # Your Gmail email address
    smtp_password = 'aicwueerhuresupz'  # Your Gmail password or app-specific password
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

@odttodocx_bp.route('/odttodocx')
def index():
    return render_template('odttodocx.html')

@odttodocx_bp.route('/odttodocxconvert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        odt_path = os.path.join(UPLOAD_FOLDER, 'input.odt')
        docx_path = os.path.join(OUTPUT_FOLDER, 'output.docx')
        file.save(odt_path)
        convert_odt_to_docx(odt_path, docx_path)

        if request.form.get('send_email'):  
            recipient_email = request.form['email']
            email_subject = request.form['subject']  
            smtp_username = 'dconvertz@gmail.com' 
            smtp_password = 'aicwueerhuresupz'
            send_email(send_email,recipient_email," "," ",docx_path)
            return redirect(url_for('odttodocx.index'))
        else:  
            return send_file(docx_path, as_attachment=True, download_name='output.docx')
    else:
        return 'Invalid file format. Allowed format is .odt'
