from flask import Blueprint, render_template, request, flash, send_file
from werkzeug.utils import secure_filename
from pdf2docx import Converter
import os
import threading

pdftodocx_blueprint = Blueprint('pdftodocx', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

pdftodocx_blueprint.config = {}  # Create a configuration dictionary for the blueprint
pdftodocx_blueprint.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_and_download(pdf_path, docx_path):
    try:
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=0, end=None)
        cv.close()
    except Exception as e:
        print(f'An error occurred while converting: {e}')

@pdftodocx_blueprint.route('/pdftodocx', methods=['GET', 'POST'])
def pdftodocx_index():
    if request.method == 'POST':
        threads = []

        for file in request.files.getlist('file'):  # Handle multiple files
            if file and allowed_file(file.filename):
                try:
                    filename = secure_filename(file.filename)
                    pdf_path = os.path.join(pdftodocx_blueprint.config['UPLOAD_FOLDER'], filename)
                    docx_filename = filename.rsplit('.', 1)[0] + '.docx'
                    docx_path = os.path.join(pdftodocx_blueprint.config['UPLOAD_FOLDER'], docx_filename)
                    
                    file.save(pdf_path)
                    
                    # Start a new thread for conversion and download
                    thread = threading.Thread(target=convert_and_download, args=(pdf_path, docx_path))
                    thread.start()
                    threads.append((thread, docx_path))  # Store thread and DOCX path
                    
                    # flash(f'{filename} conversion started!', 'success')
                except Exception as e:
                    flash(f'An error occurred while processing {filename}: {e}', 'danger')
        
        # Wait for all threads to finish
        for thread, docx_path in threads:
            thread.join()
            
            # Automatically trigger download for the converted DOCX
            if os.path.exists(docx_path):
                return send_file(docx_path, as_attachment=True)

    return render_template('pdftodocx.html')
