import os
from flask import Blueprint, redirect, render_template, request, send_file, flash, url_for
from PIL import Image
from reportlab.lib.pagesizes import portrait
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from email_utils import send_email

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


@imgtopdf_bp.route('/convert', methods=['GET','POST'])
def convert():
    if 'file' not in request.files:
        flash('No file part', 'error')
        return render_template('imgtopdf.html')

    uploaded_files = request.files.getlist('file')
    action = request.form.get('action')
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
        if action == 'send':
                recipient_email = request.form.get('email')
                smtp_username = 'dconvertz@gmail.com'  # Replace with your Gmail email address
                smtp_password = 'aicwueerhuresupz'  # The 16-digit app password you generated
                send_email(pdf_filename, recipient_email, smtp_username, smtp_password)
                return redirect(url_for('imgtopdf.convert'))
        elif action == 'download':
                if os.path.exists(pdf_filename):
                    return send_file(pdf_filename, as_attachment=True)
                else:
                    flash(f'File {pdf_filename} not found', 'danger')
    else:
        flash('No valid images uploaded', 'error')
        return render_template('imgtopdf.html')
