import subprocess
from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

# Define the upload and compressed folder paths
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
COMPRESSED_FOLDER = os.path.join(app.root_path, 'compressed')

# Full path to the Ghostscript executable
GHOSTSCRIPT_PATH = r"C:\Program Files\gs\gs10.02.0\bin\gswin64c.exe"  # Update with the correct path and executable name

@app.route('/', methods=['GET', 'POST'])
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
         "-dPDFSETTINGS=/ebook",
        "-dNOPAUSE",
        "-dBATCH",
        "-dQUIET",
        f"-sOutputFile={output_path}",
        input_path
    ]
    
    subprocess.call(gs_command)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(COMPRESSED_FOLDER, exist_ok=True)
    app.run(debug=True)
