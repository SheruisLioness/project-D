from flask import Blueprint, render_template, request, send_file
from flask_wtf import FlaskForm
from wtforms import FileField, PasswordField
import PyPDF2
import os
import datetime

encryption_bp = Blueprint("encryption", __name__, template_folder="templates")

class EncryptForm(FlaskForm):
    file = FileField("File")
    password = PasswordField("Password")

@encryption_bp.route("/encrypt", methods=["GET", "POST"])
def encrypt():
    form = EncryptForm()
    encrypted_filename = None

    if form.validate_on_submit():
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
        encrypted_path = os.path.join("uploads", encrypted_filename)

        with open(encrypted_path, "wb") as output_pdf:
            pdf_writer.write(output_pdf)

        # Check if the file exists before sending it
        if os.path.exists(encrypted_path):
            return send_file(encrypted_path, as_attachment=True, download_name=encrypted_filename)
        else:
            return "File not found."

    return render_template("encryption_app.html", form=form, encrypted_filename=encrypted_filename)
