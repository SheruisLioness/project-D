# pdfsplit.py
from flask import Blueprint, render_template, request, send_file, flash,url_for,send_file,redirect,app
from flask_mail import Mail, Message
import os
from tempfile import NamedTemporaryFile
import PyPDF2

from email_utils import send_email

pdfsplit_bp = Blueprint('pdfsplit_bp', __name__)

@pdfsplit_bp.route('/pdfsplit', methods=['GET', 'POST'])
def pdfsplit():
    if request.method == 'POST':
        input_pdf = request.files['input_pdf']
        start_page = int(request.form['start_page'])
        end_page = int(request.form['end_page'])
        send_mail = 'send_mail' in request.form
        action = request.form.get('action')
        output_filename = split_pdf(input_pdf, start_page, end_page)

        if action == 'send':
                recipient_email = request.form.get('email')
                smtp_username = 'dconvertz@gmail.com'  # Replace with your Gmail email address
                smtp_password = 'aicwueerhuresupz'  # The 16-digit app password you generated
                send_email(output_filename, recipient_email, smtp_username, smtp_password)
                return redirect(url_for('pdfsplit_bp.pdfsplit'))
        elif action == 'download':
                return send_file(output_filename, as_attachment=True)


    return render_template('pdfsplit.html')


def split_pdf(input_pdf, start_page, end_page):
    with NamedTemporaryFile(delete=False) as temp_input:
        # Save the uploaded file to a temporary file
        input_pdf.save(temp_input)
        temp_input_path = temp_input.name

    pdf_file = open(temp_input_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    output_pdf = PyPDF2.PdfWriter()

    for page_num in range(start_page - 1, min(end_page, len(pdf_reader.pages))):
        output_pdf.add_page(pdf_reader.pages[page_num])

    output_filename = f"output_{start_page}_{end_page}.pdf"
    with open(output_filename, 'wb') as output_file:
        output_pdf.write(output_file)

    pdf_file.close()

    # Delete the temporary file
    os.remove(temp_input_path)

    return output_filename


