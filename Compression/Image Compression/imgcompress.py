from flask import Blueprint, request, send_file, render_template
from PIL import Image

image_compressor_bp = Blueprint('image_compressor_bp', __name__)

# Define a function to compress the uploaded image
def compress_image(image, quality=60):
    img = Image.open(image)
    img = img.convert("RGB")
    compressed_path = "compressed_image.jpg"
    img.save(compressed_path, format="JPEG", quality=quality)
    return compressed_path

@image_compressor_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if an image file was uploaded
        if "image" in request.files:
            image = request.files["image"]
            if image.filename != "":
                # Compress the image
                compressed_path = compress_image(image, quality=60)  # Adjust quality as needed
                return send_file(compressed_path, as_attachment=True)

    return render_template("img.html")
