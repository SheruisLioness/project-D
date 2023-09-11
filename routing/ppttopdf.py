import os
from flask import Blueprint, render_template, request, send_file, flash
from pptx import Presentation
from io import BytesIO, StringIO
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

ppttopdf_bp = Blueprint('ppttopdf', __name__)

@ppttopdf_bp.route('/ppttopdf', methods=['GET', 'POST'])
def ppttopdfindex():
    if request.method == 'POST':
        if 'pptx_file' not in request.files:
            flash('No file part', 'error')
        else:
            pptx_file = request.files['pptx_file']
            if pptx_file.filename == '':
                flash('No selected file', 'error')
            else:
                pptx_bytes = pptx_file.read()
                pdf_bytes, error_message = convert_pptx_to_pdf(pptx_bytes)
                if pdf_bytes:
                    return send_file(
                        BytesIO(pdf_bytes),
                        as_attachment=True,
                        download_name='converted.pdf',
                        mimetype='application/pdf'
                    )
                else:
                    flash(error_message, 'error')

    return render_template('ppttopdf.html')

def convert_pptx_to_pdf(pptx_bytes):
    try:
        prs = Presentation(BytesIO(pptx_bytes))
        pdf_buffer = BytesIO()

        # Create a PDF canvas
        pdf_canvas = canvas.Canvas(pdf_buffer, pagesize=letter)

        for slide_number, slide in enumerate(prs.slides):
            image = slide_to_image(slide)

            # Save the image as a temporary file
            temp_image_path = 'temp_image.png'
            image.save(temp_image_path, 'PNG')

            # Draw the temporary image file on the PDF canvas
            pdf_canvas.drawImage(temp_image_path, 0, 0, width=letter[0], height=letter[1], preserveAspectRatio=True)

            if slide_number < len(prs.slides) - 1:
                pdf_canvas.showPage()

            # Clean up the temporary image file
            os.remove(temp_image_path)

        pdf_canvas.save()
        pdf_bytes = pdf_buffer.getvalue()
        return pdf_bytes, None
    except Exception as e:
        error_message = f"Conversion error: {str(e)}"
        print(error_message)
        return None, error_message

def slide_to_image(slide):
    slide_width = int(letter[0])
    slide_height = int(letter[1])
    image_stream = BytesIO()

    slide_image = Image.new("RGB", (slide_width, slide_height), (255, 255, 255))

    for shape in slide.shapes:
        if hasattr(shape, "image"):
            image = shape.image
            image_bytes = image.blob
            image_stream.write(image_bytes)
            image_stream.seek(0)

            img = Image.open(image_stream)
            img.thumbnail((slide_width, slide_height))
            slide_image.paste(img, (0, 0))

    return slide_image
