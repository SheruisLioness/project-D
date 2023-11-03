from flask import Flask
from zip import file_upload_bp
import os

app = Flask(__name__)
app.secret_key = '2222'  # Set a secret key for the session

# Register the blueprint
app.register_blueprint(file_upload_bp)

if __name__ == '__main__':
    app.run(debug=True)
