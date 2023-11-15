
from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for
import pdfkit
import os

from email_utils import send_email

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
    action = request.form.get('action')
    # Save the uploaded HTML file to a temporary file
    temp_html_path = 'temp.html'
    html_file.save(temp_html_path)

    # Convert HTML to PDF using pdfkit
    output_pdf_path = 'output.pdf'
    pdfkit.from_file(temp_html_path, output_pdf_path, configuration=config)

    # Delete the temporary HTML file
    os.remove(temp_html_path)

    # Send the generated PDF as a response
    if action == 'send':
                recipient_email = request.form.get('email')
                smtp_username = 'dconvertz@gmail.com'  # Replace with your Gmail email address
                smtp_password = 'aicwueerhuresupz'  # The 16-digit app password you generated
                send_email(output_pdf_path, recipient_email, smtp_username, smtp_password)
                return redirect(url_for('htmltopdf.index'))
    elif action == 'download':
                if os.path.exists(output_pdf_path):
                    return send_file(output_pdf_path, as_attachment=True)
                else:
                    flash(f'File {output_pdf_path} not found', 'danger')
