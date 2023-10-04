from flask import Blueprint, render_template, request, flash, send_file
from werkzeug.utils import secure_filename
from docx2pdf import convert
import os
import threading

doctopdf_blueprint = Blueprint('doctopdf', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx'}

doctopdf_blueprint.config = {}  
doctopdf_blueprint.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_and_download(docx_path, pdf_path):
    try:
        convert(docx_path, pdf_path)
    except Exception as e:
        print(f'An error occurred while converting: {e}')

@doctopdf_blueprint.route('/doctopdf', methods=['GET', 'POST'])
def doctopdf_index():
    if request.method == 'POST':
        threads = []

        for file in request.files.getlist('file'):  
            if file and allowed_file(file.filename):
                try:
                    filename = secure_filename(file.filename)
                    docx_path = os.path.join(doctopdf_blueprint.config['UPLOAD_FOLDER'], filename)
                    pdf_filename = filename.rsplit('.', 1)[0] + '.pdf'
                    pdf_path = os.path.join(doctopdf_blueprint.config['UPLOAD_FOLDER'], pdf_filename)
                    
                    file.save(docx_path)
                    
                    # Start a new thread for conversion and download
                    thread = threading.Thread(target=convert_and_download, args=(docx_path, pdf_path))
                    thread.start()
                    threads.append((thread, pdf_path))  # Store thread and PDF path
                    
                    # flash(f'{filename} conversion started!', 'success')
                except Exception as e:
                    flash(f'An error occurred while processing {filename}: {e}', 'danger')
        
        # Wait for all threads to finish
        for thread, pdf_path in threads:
            thread.join()
            
            # Automatically trigger download for the converted PDF
            if os.path.exists(pdf_path):
                return send_file(pdf_path, as_attachment=True)

    return render_template('doctopdf.html')
