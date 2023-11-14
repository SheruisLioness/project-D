from flask import Blueprint, render_template, request, send_file, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import FileField, PasswordField
import PyPDF2
import os
import datetime
import smtplib
from email.message import EmailMessage


encrypt_bp = Blueprint('encrypt_bp', __name__)
encrypt_bp.config = {'UPLOAD_FOLDER': 'uploads'}

class EncryptForm(FlaskForm):
    file = FileField("File")
    password = PasswordField("Password")

    @encrypt_bp.route("/pdfencryption", methods=["GET", "POST"])
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

                msg = EmailMessage()
                msg.set_content('Please find the encrypted PDF attached.')
                msg['Subject'] = 'Encrypted PDF'
                msg['From'] = 'dconvertz@gmail.com'
                msg['To'] = recipient_email

                with open(encrypted_path, 'rb') as pdf_file:
                    pdf_data = pdf_file.read()

                msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=encrypted_filename)

                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(smtp_username, smtp_password)
                    server.send_message(msg)

                flash('Email sent successfully!', 'success')
                return redirect(url_for('encrypt_bp.encrypt'))
            elif action == 'download':
                return send_file(encrypted_path, as_attachment=True)

        return render_template("pdfenc.html", form=form, encrypted_filename=encrypted_filename)


