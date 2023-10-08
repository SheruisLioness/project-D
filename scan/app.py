from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    # Handle the image conversion logic here
    # Retrieve the image data from request.form['imageData']

    # After conversion, redirect to the success page
    return redirect(url_for('success'))

@app.route('/success')
def success():
    # Render the conversion success page (success.html)
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
