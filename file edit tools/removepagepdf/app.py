import os
import fitz  # PyMuPDF
from flask import Flask, request, render_template, send_from_directory
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def remove_pages(input_pdf_path, output_pdf_path, pages_to_remove):
    pdf_document = fitz.open(input_pdf_path)
    pdf_document.select([page_num for page_num in range(len(pdf_document)) if page_num not in pages_to_remove])
    
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

            # Get the pages to remove from the input PDF (comma-separated)
            pages_to_remove = request.form.get('pages_to_remove')
            pages_to_remove = [int(page.strip()) for page in pages_to_remove.split(',') if page.strip()]

            # Generate the output filename with a timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            output_filename = os.path.join(app.config['UPLOAD_FOLDER'], f'{timestamp}.pdf')
            remove_pages(filename, output_filename, pages_to_remove)

            return send_from_directory(app.config['UPLOAD_FOLDER'], f'{timestamp}.pdf', as_attachment=True)

    return render_template('removepage.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
