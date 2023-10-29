from flask import Flask, render_template
from routing.pdftodocx import pdftodocx_blueprint
from routing.doctopdf import doctopdf_blueprint
from routing.doctoimg import doctoimg_blueprint
from routing.docxtopptx import docxtopptx_blueprint
from routing.pdftoimg import pdf2img_bp
from routing.pdftoppt import pdftoppt_bp
from routing.ppttopdf import ppttopdf_bp
from routing.ppttoimg import ppttoimages_bp
from routing.imgtopdf import imgtopdf_bp
from routing.xceltopdf import exceltopdf_bp
from routing.xceltodocx import exceltodocx_bp
app = Flask(__name__)

app.register_blueprint(pdftodocx_blueprint)
app.register_blueprint(doctopdf_blueprint)
app.register_blueprint(doctoimg_blueprint)
app.register_blueprint(docxtopptx_blueprint)
app.register_blueprint(pdf2img_bp)
app.register_blueprint(pdftoppt_bp) 
app.register_blueprint(ppttopdf_bp)
app.register_blueprint(ppttoimages_bp)
app.register_blueprint(imgtopdf_bp)
app.register_blueprint(exceltopdf_bp)
app.register_blueprint(exceltodocx_bp)

app.secret_key = '2208'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
