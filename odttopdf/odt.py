from flask import Blueprint, request, render_template, send_file
import os
import subprocess
import uuid

odt_blueprint = Blueprint('odt_blueprint', __name__)

@odt_blueprint.route('/')
def index():
    return render_template('index.html')

@odt_blueprint.route('/download/<pdf_filename>')
def download(pdf_filename):
    pdf_filepath = os.path.join('uploads', pdf_filename)
    if os.path.exists(pdf_filepath):
        return send_file(pdf_filepath, as_attachment=True)
    else:
        return "PDF file not found."
