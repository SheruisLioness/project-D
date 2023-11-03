from flask import Flask
from pdfenc import encrypt_bp

app = Flask(__name__)
app.register_blueprint(encrypt_bp)
app.secret_key="2222"
if __name__ == "__main__":
    app.run(debug=True)
