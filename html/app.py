from flask import Flask
from htmltopdf.htmltopdf_blueprint import htmltopdf_bp  # Import the blueprint

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(htmltopdf_bp)

if __name__ == '__main__':
    app.run(debug=True)
