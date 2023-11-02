from PdfCompress import pdf_compressor_bp
from flask import Flask, render_template
app = Flask(__name__)
app.register_blueprint(pdf_compressor_bp)
@app.route("/")
def index():
    return render_template("pdf.html")

if __name__=='__main__':
    app.run(debug=True)