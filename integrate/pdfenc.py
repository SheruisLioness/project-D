from flask import Flask, Blueprint, render_template, request, send_file
from flask_wtf import FlaskForm
from wtforms import FileField, PasswordField
import PyPDF2
import os
import datetime

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
        
        with open(encrypted_path, "wb") as output_pdf:
            pdf_writer.write(output_pdf)

        return send_file(encrypted_path, as_attachment=True, download_name=encrypted_filename)

    return render_template("pdfenc.html", form=form, encrypted_filename=encrypted_filename)

if __name__ == "__main__":
    app.register_blueprint(encrypt_bp)
    app.run(host="localhost", port=4444)
