from flask import Flask,render_template
from imgcompress import image_compressor_bp
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('img.html')

if __name__ == '__main__':
    app.run(debug=True)