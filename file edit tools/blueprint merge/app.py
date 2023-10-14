from flask import Flask, render_template
from pdfmerge_bp import pdf_merge_bp  # Import the PDF merge Blueprint

# Create the Flask app
app = Flask(__name__)

# Register the PDF merge Blueprint with a URL prefix
app.register_blueprint(pdf_merge_bp, url_prefix='/pdfmerge')

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
