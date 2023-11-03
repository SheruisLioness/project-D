import os
import subprocess
import uuid
from flask import Blueprint, render_template, redirect, url_for, request, send_file
from email_utils import send_email

odttopdf_bp = Blueprint('odttopdf_bp', __name__)

@odttopdf_bp.route('/odttopdf', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_file = request.files['file']
        action = request.form.get('action')

        if input_file:
            unique_filename = str(uuid.uuid4()) + os.path.splitext(input_file.filename)[-1]
            input_filename = os.path.join('uploads', unique_filename)
            input_file.save(input_filename)

            try:
                pdf_filename = os.path.splitext(unique_filename)[0] + '.pdf'
                pdf_filepath = os.path.join('uploads', pdf_filename)
                subprocess.run(['C:\\Program Files\\LibreOffice\\program\\soffice.exe', '--headless', '--convert-to', 'pdf', input_filename, '--outdir', 'uploads'])

                if action == 'send':
                    recipient_email = request.form.get('email')
                    smtp_username = 'dconvertz@gmail.com'  # Replace with your Gmail email address
                    smtp_password = 'aicwueerhuresupz'  # The 16-digit app password you generated
                    send_email(pdf_filepath, recipient_email, smtp_username, smtp_password)
                    return redirect(url_for('odttopdf_bp.index'))
                elif action == 'download':
                    return send_file(pdf_filepath, as_attachment=True, download_name=pdf_filename)
            except Exception as e:
                return f"Error converting file: {str(e)}"

    return render_template('odttopdf.html')

if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)
    app.register_blueprint(odttopdf_bp)

    # Ensure the existence of the 'uploads' directory
    os.makedirs('uploads', exist_ok=True)

    app.run(debug=True)
