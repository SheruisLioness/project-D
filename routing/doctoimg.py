from flask import Blueprint, render_template, request, send_file
import os
import zipfile
import tempfile
from docx2txt import process
from PIL import Image
from pdftoimg import create_image_files

doctoimg_blueprint = Blueprint('doctoimg', __name__)

UPLOAD_FOLDER = 'uploads'

def docx_to_images(docx_file):
    text = process(docx_file)
    image = Image.new('RGB', (800, 600), color='white')
    images = [image]
    return images

@doctoimg_blueprint.route('/doctoimg', methods=['GET', 'POST'])
def doctoimg_index():
    if request.method == 'POST':
        if 'docx_file' not in request.files:
            return render_template('doctoimg.html', error='No file part')

        docx_file = request.files['docx_file']
        
        if docx_file.filename == '':
            return render_template('doctoimg.html', error='No selected file')

        if docx_file:
            images = docx_to_images(docx_file)
            
            temp_dir = tempfile.mkdtemp()
            image_files = create_image_files(images, temp_dir)

            zip_file_path = os.path.join(UPLOAD_FOLDER, 'images.zip')
            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                for image_file in image_files:
                    zipf.write(image_file, os.path.basename(image_file))
            
            for image_file in image_files:
                os.remove(image_file)
            os.rmdir(temp_dir)
            
            return send_file(zip_file_path, as_attachment=True)
    
    return render_template('doctoimg.html', error=None)
