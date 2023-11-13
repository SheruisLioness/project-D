# Import necessary modules
from flask import Flask, Blueprint, request, render_template, send_from_directory, Response
import os
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import datetime

pdfsplit_bp = Blueprint("pdfsplit", __name__)

# Path to the upload and output folders, and allowed file extensions
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'pdf'}

pdfsplit_bp.config = {
    'UPLOAD_FOLDER': UPLOAD_FOLDER,
    'OUTPUT_FOLDER': OUTPUT_FOLDER,
    'ALLOWED_EXTENSIONS': ALLOWED_EXTENSIONS
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in pdfsplit_bp.config['ALLOWED_EXTENSIONS']

def split_and_merge_pdf(input_pdf, start_page, end_page, original_filename):
    output_folder = pdfsplit_bp.config['OUTPUT_FOLDER']
    os.makedirs(output_folder, exist_ok=True)
    
    pdf = PdfReader(input_pdf)
    output_pdf = PdfWriter()

    for page_num, page in enumerate(pdf.pages, start=1):
        if start_page <= page_num <= end_page:
            output_pdf.add_page(page)

    # Generate a unique output filename using current date and time
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = os.path.join(output_folder, f'pages_{start_page}_to_{end_page}_{current_datetime}.pdf')
    
    with open(output_filename, 'wb') as output_file:
        output_pdf.write(output_file)

    # Create a BytesIO object to hold the PDF content
    output_pdf_bytes = BytesIO()

    # Write the PDF content to the BytesIO object
    with open(output_filename, 'rb') as pdf_file:
        output_pdf_bytes.write(pdf_file.read())

    # Seek to the beginning of the BytesIO object
    output_pdf_bytes.seek(0)

    return output_pdf_bytes

@pdfsplit_bp.route('/pdfsplit', methods=['GET', 'POST'])
def split_pdf():
    splitted_files = []  # List to hold the splitted PDF filenames

    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']
        start_page = int(request.form['start_page'])
        end_page = int(request.form['end_page'])
        
        if file.filename == '':
            return 'No selected file'
        
        if file and allowed_file(file.filename):
            # Save uploaded file
            filename = os.path.join(pdfsplit_bp.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            
            # Split and merge the PDF
            output_pdf_bytes = split_and_merge_pdf(filename, start_page, end_page, file.filename)

            # Set the appropriate response headers for PDF download
            response = Response(output_pdf_bytes, content_type='application/pdf')
            response.headers['Content-Disposition'] = f'attachment; filename={file.filename}'

            return response

    return render_template('pdfsplit.html', splitted_files=splitted_files)

@pdfsplit_bp.route('/output/<filename>')
def download_output(filename):
    return send_from_directory(pdfsplit_bp.config['OUTPUT_FOLDER'], filename, as_attachment=True, mimetype='application/pdf', attachment_filename=filename)
