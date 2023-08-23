import os
import zipfile
from flask import Flask, render_template, request, send_file
from pdf2image import convert_from_bytes
import tempfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def pdf_to_images(pdf_bytes):
    images = convert_from_bytes(pdf_bytes)
    return images

def create_image_files(images, output_dir):
    image_files = []
    
    for i, image in enumerate(images):
        image_path = os.path.join(output_dir, f'image_{i}.png')
        image.save(image_path, 'PNG')
        image_files.append(image_path)
    
    return image_files

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return render_template('pdftoimg.html', error='No file part')

        pdf_file = request.files['pdf_file']
        
        if pdf_file.filename == '':
            return render_template('pdftoimg.html', error='No selected file')

        if pdf_file:
            pdf_bytes = pdf_file.read()
            images = pdf_to_images(pdf_bytes)
            
            temp_dir = tempfile.mkdtemp()  # Create a temporary directory
            image_files = create_image_files(images, temp_dir)

            # Create a zip folder containing the image files
            zip_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'images.zip')
            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                for image_file in image_files:
                    zipf.write(image_file, os.path.basename(image_file))
            
            # Clean up temporary directory
            for image_file in image_files:
                os.remove(image_file)
            os.rmdir(temp_dir)
            
            return send_file(zip_file_path, as_attachment=True)
    
    return render_template('pdftoimg.html', error=None)

if __name__ == '__main__':
    app.run(debug=True)
