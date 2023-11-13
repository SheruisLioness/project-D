import os
from flask import Blueprint, flash, redirect, request, send_file, render_template, url_for
from PIL import Image

from email_utils import send_email

image_compressor_bp = Blueprint('image_compressor_bp', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','webp'}

# Define a function to check for allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define a function to compress the uploaded image
def compress_image(image, quality=60):
    img = Image.open(image)
    img = img.convert("RGB")
    compressed_path = "compressed_image.jpg"
    img.save(compressed_path, format="JPEG", quality=quality)
    return compressed_path

@image_compressor_bp.route("/imgcompress", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if an image file was uploaded
        if "image" in request.files:
            image = request.files["image"]
            if image.filename != "":
                if allowed_file(image.filename):
                    # Compress the image
                    action = request.form.get('action')
                    compressed_path = compress_image(image, quality=60)  # Adjust quality as needed
                    if action == 'send':
                        recipient_email = request.form.get('email')
                        smtp_username = 'dconvertz@gmail.com'  # Replace with your Gmail email address
                        smtp_password = 'aicwueerhuresupz'  # The 16-digit app password you generated
                        send_email(compressed_path, recipient_email, smtp_username, smtp_password)
                        return redirect(url_for('image_compressor_bp.index'))
                    elif action == 'download':
                        if os.path.exists(compressed_path):
                            return send_file(compressed_path, as_attachment=True)
                        else:
                            flash(f'File {compressed_path} not found', 'danger')
                else:
                    flash('File format not supported. Please upload a valid image file.', 'danger')
            else:
                flash('No file selected. Please upload an image file.', 'danger')

    return render_template("img.html")
