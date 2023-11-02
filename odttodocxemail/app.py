from flask import Flask
from odttodocx import odttodocx_bp

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(odttodocx_bp)

if __name__ == '__main__':
    app.run(debug=True)
