from flask import Flask, render_template,redirect,url_for
from odt import odt_blueprint
from flask import request
import uuid
import os
import subprocess
app = Flask(__name__)
app.register_blueprint(odt_blueprint)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_file = request.files['file']
        if input_file:
            unique_filename = str(uuid.uuid4()) + os.path.splitext(input_file.filename)[-1]
            input_filename = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            input_file.save(input_filename)

            try:
                pdf_filename = os.path.splitext(unique_filename)[0] + '.pdf'
                pdf_filepath = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
                subprocess.run(['C:\\Program Files\\LibreOffice\\program\\soffice.exe', '--headless', '--convert-to', 'pdf', input_filename, '--outdir', app.config['UPLOAD_FOLDER']])
            except Exception as e:
                return f"Error converting file: {str(e)}"

            return redirect(url_for('odt_blueprint.download', pdf_filename=pdf_filename))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
