import subprocess
import os
from flask import Blueprint, render_template, request, send_file

pdf_compressor_bp = Blueprint('pdf_compressor_bp', __name__)

# Define the upload and compressed folder paths
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
COMPRESSED_FOLDER = os.path.join(os.getcwd(), 'compressed')

# Full path to the Ghostscript executable
GHOSTSCRIPT_PATH = r"C:\Users\byris\OneDrive\Documents\project-D\ReqPackages\gs10.02.0\bin\gswin64c.exe"  # Update with the correct path and executable name

@pdf_compressor_bp.route('/pdfcompress', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            input_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(input_path)

            output_path = os.path.join(COMPRESSED_FOLDER, 'compressed_' + uploaded_file.filename)
            compress_pdf(input_path, output_path)

            compressed_filename = 'compressed_' + uploaded_file.filename
            return send_file(output_path, as_attachment=True, download_name=compressed_filename)

    return render_template('pdf.html')

def compress_pdf(input_path, output_path):
    gs_command = [
        GHOSTSCRIPT_PATH,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/printer",  # Use /printer for better quality
        "-dNOPAUSE",
        "-dBATCH",
        "-dQUIET",
        f"-sOutputFile={output_path}",
        input_path
    ]
    
    subprocess.call(gs_command)
