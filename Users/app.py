from flask import Flask, render_template
from auth_routes import auth_bp

app = Flask(__name__)
app.secret_key = '2208'

# Import auth_bp from the auth_routes module
app.register_blueprint(auth_bp)

# Main route
@app.route('/')
def index():
    return render_template('auth.html')

if __name__ == '__main__':
    app.run(debug=True)
