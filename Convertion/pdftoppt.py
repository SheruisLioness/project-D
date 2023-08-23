import os
from flask import Flask, render_template, request, send_file
from pdf2image import convert_from_bytes
from pptx import Presentation
from pptx.util import Inches
import tempfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def pdf_to_images(pdf_bytes):
    images = convert_from_bytes(pdf_bytes)
    return images

def create_pptx(images):
    prs = Presentation()
    
    temp_dir = tempfile.mkdtemp()  # Create a temporary directory

    for i, image in enumerate(images):
        image_path = os.path.join(temp_dir, f'image_{i}.png')
        image.save(image_path, 'PNG')  # Save the image as a temporary file
        
        slide = prs.slides.add_slide(prs.slide_layouts[5])
        left = Inches(1)
        top = Inches(1)
        pic = slide.shapes.add_picture(image_path, left, top, width=Inches(8.5), height=Inches(6))

    pptx_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.pptx')
    prs.save(pptx_path)

    # Clean up temporary directory
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        os.remove(file_path)
    os.rmdir(temp_dir)

    return pptx_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return render_template('pdftoppt.html', error='No file part')

        pdf_file = request.files['pdf_file']
        
        if pdf_file.filename == '':
            return render_template('pdftoppt.html', error='No selected file')

        if pdf_file:
            pdf_bytes = pdf_file.read()
            images = pdf_to_images(pdf_bytes)
            pptx_path = create_pptx(images)
            return send_file(pptx_path, as_attachment=True)
    
    return render_template('pdftoppt.html', error=None)

if __name__ == '__main__':
    app.run(debug=True)
