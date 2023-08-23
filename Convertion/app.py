from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def test():
    return render_template('index.html')

@app.route('/doctopdf', methods=['GET', 'POST'])
def doctopdf():
    return render_template("doctopdf.html")

if __name__ == "__main__":
    app.run(debug=True)
