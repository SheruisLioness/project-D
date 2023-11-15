# doctoimg.py
import pythoncom
from flask import Blueprint, redirect, render_template, request, send_file, url_for, flash
import os
import zipfile
import tempfile
from docx2pdf import convert
from pdf2image import convert_from_path

from email_utils import send_email

doctoimg_blueprint = Blueprint('doctoimg', __name__)

UPLOAD_FOLDER = 'uploads'

@doctoimg_blueprint.route('/doctoimg', methods=['GET', 'POST'])
def doctoimg_index():
    pythoncom.CoInitialize()  # Initialize the COM library
    if request.method == 'POST':
        action = request.form.get('action')
        if 'docx_file' not in request.files:
            return render_template('doctoimg.html', error='No file part')

        docx_file = request.files['docx_file']
        if not docx_file.filename.endswith('.docx'):
            flash('Please select a .docx file.')
            return redirect(request.url)

        if docx_file:
            temp_dir = tempfile.mkdtemp()
            docx_path = os.path.join(temp_dir, 'input.docx')
            docx_file.save(docx_path)

            pdf_path = os.path.join(temp_dir, 'output.pdf')
            convert(docx_path, pdf_path)

            images = convert_from_path(pdf_path)

            image_files = []
            for i, image in enumerate(images):
                image_path = os.path.join(temp_dir, f'page_{i}.png')
                image.save(image_path, "PNG")
                image_files.append(image_path)

            zip_file_path = os.path.join(UPLOAD_FOLDER, 'images.zip')
            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                for image_file in image_files:
                    zipf.write(image_file, os.path.basename(image_file))

            for image_file in image_files:
                os.remove(image_file)
            os.remove(pdf_path)
            os.remove(docx_path)
            os.rmdir(temp_dir)

            if action == 'send':
                recipient_email = request.form.get('email')
                smtp_username = 'dconvertz@gmail.com'  # Replace with your Gmail email address
                smtp_password = 'aicwueerhuresupz'  # The 16-digit app password you generated
                send_email(zip_file_path, recipient_email, smtp_username, smtp_password)
                return redirect(url_for('doctoimg.doctoimg_index'))
            elif action == 'download':
                return send_file(zip_file_path, as_attachment=True)

    return render_template('doctoimg.html', error=None)
