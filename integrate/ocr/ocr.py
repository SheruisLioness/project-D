import os
import ocrmypdf
from flask import Blueprint, render_template, request, send_file, flash, redirect, current_app
from werkzeug.utils import secure_filename
import threading

ocr_blueprint = Blueprint('ocr', __name__)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ocr_pdf(input_path, output_path):
    try:
        ocrmypdf.ocr(input_path, output_path, skip_text=True)
    except Exception as e:
        print(f'Error during OCR: {e}')

@ocr_blueprint.route('/ocrindex')
def index():
    return render_template('ocr.html', download_link=None)

@ocr_blueprint.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)

    file = request.files['file']

    if file.filename is None or file.filename == '':
        flash('No selected file', 'danger')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        output_filename = filename.rsplit('.', 1)[0] + '_ocr.pdf'
        output_path = os.path.join(current_app.config['DOWNLOAD_FOLDER'], output_filename)
        file.save(input_path)

        thread = threading.Thread(target=ocr_pdf, args=(input_path, output_path))
        thread.start()
        thread.join()

        if os.path.exists(output_path):
            flash('OCR', 'success')
            return send_file(output_path, as_attachment=True)

    flash('File upload or OCR failed.', 'danger')
    return redirect(request.url)
