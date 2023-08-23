from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure email settings
# Local SMTP server configuration
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 5000
app.config['MAIL_USE_TLS'] = False

app.config['MAIL_USERNAME'] = 'your_username'
app.config['MAIL_PASSWORD'] = 'your_password'

mail = Mail(app)

@app.route('/')
def index():
    return render_template('contact_form.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        subject = 'New Contact Form Submission'
        body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        msg = Message(subject=subject,
                      sender='21001cs069@gmail.com',
                      recipients=['receiver@example.com'])  # Receiver's email

        msg.body = body

        try:
            mail.send(msg)
            return 'Email sent successfully!'
        except Exception as e:
            return f'Error sending email: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
