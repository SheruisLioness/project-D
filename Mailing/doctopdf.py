from flask import Flask, render_template, request, flash, send_file
from werkzeug.utils import secure_filename
from docx2pdf import convert
import os
import threading

app = Flask(__name__)

# Configure a safe folder for uploaded files 
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '2208'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_and_download(docx_path, pdf_path):
    try:
        convert(docx_path, pdf_path)
    except Exception as e:
        print(f'An error occurred while converting: {e}')

@app.route('/doctopdf', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        threads = []

        for file in request.files.getlist('file'):  # Handle multiple files
            if file and allowed_file(file.filename):
                try:
                    filename = secure_filename(file.filename)
                    docx_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    pdf_filename = filename.rsplit('.', 1)[0] + '.pdf'
                    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
                    
                    file.save(docx_path)
                    
                    # Start a new thread for conversion and download
                    thread = threading.Thread(target=convert_and_download, args=(docx_path, pdf_path))
                    thread.start()
                    threads.append((thread, pdf_path))  # Store thread and PDF path
                    
                    flash(f'{filename} conversion started!', 'success')
                except Exception as e:
                    flash(f'An error occurred while processing {filename}: {e}', 'danger')
        
        # Wait for all threads to finish
        for thread, pdf_path in threads:
            thread.join()
            
            # Automatically trigger download for the converted PDF
            if os.path.exists(pdf_path):
                return send_file(pdf_path, as_attachment=True)

    return render_template('doctopdf.html')

if __name__ == '__main__':
    app.run(debug=True)
