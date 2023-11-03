from flask import Blueprint, render_template, request, send_file
import pdfkit
import os

htmltopdf_bp = Blueprint('htmltopdf', __name__)

# Set the path to wkhtmltopdf executable
wkhtmltopdf_path = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

@htmltopdf_bp.route('/htmltopdf')
def index():
    return render_template('htmltopdf.html')

@htmltopdf_bp.route('/htmltopdfconvert', methods=['POST'])
def convert():
    html_file = request.files['htmlFile']

    # Save the uploaded HTML file to a temporary file
    temp_html_path = 'temp.html'
    html_file.save(temp_html_path)

    # Convert HTML to PDF using pdfkit
    output_pdf_path = 'output.pdf'
    pdfkit.from_file(temp_html_path, output_pdf_path, configuration=config)

    # Delete the temporary HTML file
    os.remove(temp_html_path)

    # Send the generated PDF as a response
    return send_file(output_pdf_path, as_attachment=True)
