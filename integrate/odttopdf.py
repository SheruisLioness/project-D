import os
import subprocess
import uuid
from flask import Blueprint, render_template, redirect, url_for, request, send_file, flash
from werkzeug.utils import secure_filename
from email_utils import send_email

odttopdf_bp = Blueprint('odttopdf_bp', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'odt'}

@odttopdf_bp.route('/odttopdf', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_file = request.files['file']
        action = request.form.get('action')

        if input_file:
            filename = secure_filename(input_file.filename)
            file_extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
            if file_extension in ALLOWED_EXTENSIONS:
                unique_filename = str(uuid.uuid4()) + os.path.splitext(filename)[-1]
                input_filename = os.path.join(UPLOAD_FOLDER, unique_filename)
                input_file.save(input_filename)

                try:
                    pdf_filename = os.path.splitext(unique_filename)[0] + '.pdf'
                    pdf_filepath = os.path.join(UPLOAD_FOLDER, pdf_filename)
                    subprocess.run(['C:\\Program Files\\LibreOffice\\program\\soffice.exe', '--headless', '--convert-to', 'pdf', input_filename, '--outdir', UPLOAD_FOLDER])

                    if action == 'send':
                        recipient_email = request.form.get('email')
                        smtp_username = 'dconvertz@gmail.com'  
                        smtp_password = 'aicwueerhuresupz'  
                        send_email(pdf_filepath, recipient_email, smtp_username, smtp_password)
                        return redirect(url_for('odttopdf_bp.index'))
                    elif action == 'download':
                        return send_file(pdf_filepath, as_attachment=True, download_name=pdf_filename)
                except Exception as e:
                    return f"Error converting file: {str(e)}"
            else:
                flash('Only ODT files are supported', 'danger')

    return render_template('odttopdf.html')
