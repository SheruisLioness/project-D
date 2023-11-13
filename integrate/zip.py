from flask import Blueprint, Flask, redirect, render_template, request, send_file, url_for
import os
import zipfile

from email_utils import send_email

file_upload_bp = Blueprint('file_upload_bp', __name__)

file_upload_bp.config = {'UPLOAD_FOLDER': 'uploads', 'DOWNLOAD_FOLDER': 'downloads'}

if not os.path.exists(file_upload_bp.config['UPLOAD_FOLDER']):
    os.makedirs(file_upload_bp.config['UPLOAD_FOLDER'])

if not os.path.exists(file_upload_bp.config['DOWNLOAD_FOLDER']):
    os.makedirs(file_upload_bp.config['DOWNLOAD_FOLDER'])

@file_upload_bp.route('/zip')
def index():
    return render_template('zip.html')

@file_upload_bp.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist('files')
    zip_filename = os.path.join(file_upload_bp.config['DOWNLOAD_FOLDER'], 'result.zip')
    action = request.form.get('action')
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in uploaded_files:
            if file:
                file_path = os.path.join(file_upload_bp.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                zipf.write(file_path, os.path.basename(file_path))
                os.remove(file_path)

    if action == 'send':
                recipient_email = request.form.get('email')
                smtp_username = 'dconvertz@gmail.com'  
                smtp_password = 'aicwueerhuresupz'  
                send_email(zip_filename, recipient_email, smtp_username, smtp_password)
                return redirect(url_for('file_upload_bp.index'))
    elif action == 'download':
                return send_file(zip_filename, as_attachment=True)


