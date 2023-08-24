import os
from PyPDF2 import PdfReader, PdfWriter
from flask import Flask, request, render_template, send_from_directory, make_response
from io import BytesIO

app = Flask(__name__)

# Path to the upload and output folders, and allowed file extensions
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def split_and_merge_pdf(input_pdf, start_page, end_page, original_filename):
    output_folder = app.config['OUTPUT_FOLDER']
    os.makedirs(output_folder, exist_ok=True)
    
    pdf = PdfReader(input_pdf)
    output_pdf = PdfWriter()

    for page_num, page in enumerate(pdf.pages, start=1):
        if start_page <= page_num <= end_page:
            output_pdf.add_page(page)

    output_filename = os.path.join(output_folder, f'split_{original_filename}_pages_{start_page}_to_{end_page}.pdf')
    with open(output_filename, 'wb') as output_file:
        output_pdf.write(output_file)

    return output_filename

@app.route('/', methods=['GET', 'POST'])
def upload_file():
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
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            
            # Split and merge the PDF
            merged_filename = split_and_merge_pdf(filename, start_page, end_page, file.filename)
            
            splitted_files.append(os.path.basename(merged_filename))
            
    return render_template('pdfsplit.html', splitted_files=splitted_files)

@app.route('/output/<filename>')
def download_output(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
