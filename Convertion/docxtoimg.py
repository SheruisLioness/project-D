from flask import Flask, render_template, request, send_file
import os
import zipfile
import tempfile
from docx2txt import process
from PIL import Image

from Convertion.pdftoimg import create_image_files

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def docx_to_images(docx_file):
    text = process(docx_file)  # Use the file-like object directly
    # Create an image from the text content (you might need to adjust this part)
    image = Image.new('RGB', (800, 600), color='white')
    # You can add text to the image here if needed
    images = [image]  # Just an example, replace with your actual images
    return images

# ... rest of the code ...

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'docx_file' not in request.files:
            return render_template('doctoimg.html', error='No file part')

        docx_file = request.files['docx_file']
        
        if docx_file.filename == '':
            return render_template('doctoimg.html', error='No selected file')

        if docx_file:
            images = docx_to_images(docx_file)
            
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
    
    return render_template('doctoimg.html', error=None)

if __name__ == '__main__':
    app.run(debug=True)
    