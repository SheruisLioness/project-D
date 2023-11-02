# app.py

import os
from flask import Flask, render_template
from pdfsplit_bp import pdfsplit_bp  # Import the pdfsplit_bp blueprint

app = Flask(__name__)

# Register the pdfsplit_bp blueprint
app.register_blueprint(pdfsplit_bp)

# Set Flask application configurations
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

@app.route('/')
def index():
    return render_template('pdfsplit.html')

if __name__ == '__main__':
    app.run(debug=True)
