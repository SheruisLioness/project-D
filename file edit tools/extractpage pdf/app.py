import os
import fitz  # PyMuPDF
from flask import Flask, request, render_template, send_from_directory
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def extract_pages(input_pdf_path, output_pdf_path, pages_to_extract):
    pdf_document = fitz.open(input_pdf_path)
    pdf_document.select(pages_to_extract)
    
    pdf_document.save(output_pdf_path)
    pdf_document.close()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['file']

        if file.filename == '':
            return "No selected file"

        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            # Get the pages to extract from the input PDF (comma-separated)
            pages_to_extract = request.form.get('pages_to_extract')
            pages_to_extract = [int(page.strip()) for page in pages_to_extract.split(',') if page.strip()]

            # Generate the output filename with a timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            output_filename = os.path.join(app.config['UPLOAD_FOLDER'], f'output_{timestamp}.pdf')
            extract_pages(filename, output_filename, pages_to_extract)

            return send_from_directory(app.config['UPLOAD_FOLDER'], f'output_{timestamp}.pdf', as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
