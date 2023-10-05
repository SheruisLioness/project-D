import os
from flask import Blueprint, render_template, request, send_file, flash
from PIL import Image
from reportlab.lib.pagesizes import portrait
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

imgtopdf_bp = Blueprint('imgtopdf', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def images_to_pdf(image_files, pdf_filename):
    try:
        c = canvas.Canvas(pdf_filename, pagesize=portrait((8.5 * 72, 11 * 72)))  # Letter size in points (72 points per inch)

        for image_file in image_files:
            img = Image.open(image_file)
            img_width, img_height = img.size
            c.setPageSize((img_width, img_height))
            c.drawImage(
                ImageReader(img),
                x=0, y=0,
                width=img_width, height=img_height
            )
            c.showPage()

        c.save()
    except Exception as e:
        print(f"PDF creation error: {str(e)}")
        return None

# @imgtopdf_bp.route('/')
# def index():
#     return render_template('imgtopdf.html')

@imgtopdf_bp.route('/convert', methods=['GET','POST'])
def convert():
    if 'file' not in request.files:
        flash('No file part', 'error')
        return render_template('imgtopdf.html')

    uploaded_files = request.files.getlist('file')

    if not uploaded_files:
        flash('No selected files', 'error')
        return render_template('imgtopdf.html')

    images = []
    for uploaded_file in uploaded_files:
        if uploaded_file.filename == '':
            continue
        if allowed_file(uploaded_file.filename):
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(file_path)
            images.append(file_path)
        else:
            flash('Unsupported file format', 'error')
            return render_template('imgtopdf.html')

    if images:
        pdf_filename = 'output.pdf'
        images_to_pdf(images, pdf_filename)
        return send_file(
            pdf_filename,
            as_attachment=True,
            download_name='output.pdf',
            mimetype='application/pdf'
        )
    else:
        flash('No valid images uploaded', 'error')
        return render_template('imgtopdf.html')
