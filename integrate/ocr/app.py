from flask import Flask, render_template
import os
from ocr import ocr_blueprint

app = Flask(__name__)
app.secret_key = '0911'

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# Register the blueprint with a URL prefix (e.g., '/ocr')
app.register_blueprint(ocr_blueprint)

@app.route('/')
def index():
    return render_template('index.html', download_link=None)

if __name__ == '__main__':
    app.run(debug=True)
