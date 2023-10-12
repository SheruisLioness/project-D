import os
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from io import BytesIO
from PIL import Image
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'

@app.route('/')
def index():
    return render_template('capture.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        image_data = request.form.getlist('imageData')
        
        if not image_data:
            flash('No image data received', 'error')
            return redirect(url_for('index'))

        pdf_filename = 'output.pdf'

        # Create a list to store image objects
        images = []
        
        for img_str in image_data:
            # Decode base64 image data
            image_bytes = base64.b64decode(img_str)
            image = Image.open(BytesIO(image_bytes))
            images.append(image)
        
        # Create a PDF file
        pdf_filename = 'output.pdf'
        images[0].save(
            pdf_filename,
            save_all=True,
            append_images=images[1:],
            resolution=100.0,
            quality=95,
            optimize=True
        )

        return send_file(
            pdf_filename,
            as_attachment=True,
            download_name='output.pdf',
            mimetype='application/pdf'
        )

    except Exception as e:
        print(f"PDF creation error: {str(e)}")
        flash('Error creating PDF', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
