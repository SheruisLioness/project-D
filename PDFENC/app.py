from flask import Flask,render_template
from pdfsplit import pdfsplit_bp
from pdfmerge import pdfmerge_bp
from encryption_app import encryption_bp

# Set the secret key here
SECRET_KEY = '2208'

# Create the Flask app instance
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Import and register blueprints and routes here
app.register_blueprint(pdfsplit_bp, url_prefix="/pdfsplit")
app.register_blueprint(pdfmerge_bp, url_prefix="/pdfmerge")
app.register_blueprint(encryption_bp, url_prefix="/encryption")

# Import and register other routes here
@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="localhost", port=4444, debug=True)
