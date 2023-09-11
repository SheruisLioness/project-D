from flask import Flask, render_template
from pdftodoc import pdftodocx_blueprint
from doctopdf import doctopdf_blueprint

app = Flask(__name__)
app.register_blueprint(pdftodocx_blueprint)
app.register_blueprint(doctopdf_blueprint)

# Configure the UPLOAD_FOLDER for both blueprints in the main app
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # Define the routes for the dynamic menu
    routes = [
        {'name': 'PDF to DOCX Conversion', 'url': 'pdftodocx.pdftodocx_index'},
        {'name': 'DOCX to PDF Conversion', 'url': 'doctopdf.doctopdf_index'}
        # Add more routes if needed
    ]
    return render_template('menu.html', routes=routes)

if __name__ == '__main__':
    app.run(debug=True)
