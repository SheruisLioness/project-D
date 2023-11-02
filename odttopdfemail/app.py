from flask import Flask
from odttopdf import odttopdf_bp

app = Flask(__name__)

# Register the odttopdf blueprint
app.register_blueprint(odttopdf_bp)

if __name__ == '__main__':
    app.run(debug=True)
