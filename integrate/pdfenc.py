from flask import Flask, Blueprint, redirect, render_template, request, send_file, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, PasswordField
import PyPDF2
import os
import datetime

from email_utils import send_email

app = Flask(__name__)
app.secret_key = '2222' 

encrypt_bp = Blueprint('encrypt_bp', __name__)
encrypt_bp.config = {'UPLOAD_FOLDER': 'uploads'}

class EncryptForm(FlaskForm):
    file = FileField("File")
    password = PasswordField("Password")

@encrypt_bp.route("/pdfencrypt", methods=["GET", "POST"])
def encrypt():
    form = EncryptForm()
    encrypted_filename = None

    if request.method == 'POST' and form.validate_on_submit():
        file = form.file.data
        password = form.password.data

        pdf_file = file.stream

        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])

        pdf_writer.encrypt(password)

        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        encrypted_filename = f"{current_datetime}.pdf"
        encrypted_path = os.path.join(encrypt_bp.config['UPLOAD_FOLDER'], encrypted_filename)
        action = request.form.get('action')
        with open(encrypted_path, "wb") as output_pdf:
            pdf_writer.write(output_pdf)

        if action == 'send':
                recipient_email = request.form.get('email')
                smtp_username = 'dconvertz@gmail.com'  # Replace with your Gmail email address
                smtp_password = 'aicwueerhuresupz'  # The 16-digit app password you generated
                send_email(output_pdf, recipient_email, smtp_username, smtp_password)
                return redirect(url_for('encrypt_bp.encrypt'))
        elif action == 'download':
                return send_file(output_pdf, as_attachment=True)

    return render_template("pdfenc.html", form=form, encrypted_filename=encrypted_filename)

if __name__ == "__main__":
    app.run(debug=True)
