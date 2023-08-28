from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultiparts
from email.mime.application import MIMEApplication

app = Flask(__name__)

def send_email(sender_email, receiver_email, subject, message, file_path, smtp_server, smtp_port, username, password):
    try:
        # Create the MIMEText object
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        # Attach the file
        with open(file_path, "rb") as attachment:
            part = MIMEApplication(attachment.read(), Name="attached_file")
            part["Content-Disposition"] = f'attachment; filename="{file_path}"'
            msg.attach(part)

        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Start TLS encryption
        server.login(username, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        print("An error occurred:", str(e))
        return False
    finally:
        server.quit()  # Disconnect from the server

@app.route("/", methods=["GET", "POST"])
def send_email_page():
    if request.method == "POST":
        sender_email = "Dconvertz@gmail.com"
        receiver_email = request.form["receiver_email"]
        subject = request.form["subject"]
        message = request.form["message"]
        file = request.files["file"]  # Get the uploaded file
        
        if file:
            file_path = file.filename
            file.save(file_path)
        else:
            file_path = None
        
        smtp_server = "smtp.gmail.com"
        smtp_port = 587  # Gmail's SMTP port
        
        username = "Dconvertz@gmail.com"
        password = "hsqbsglmyyxwwgzb"  # Use the generated app password or your Gmail password
        
        if send_email(sender_email, receiver_email, subject, message, file_path, smtp_server, smtp_port, username, password):
            return "Email sent successfully!"
        else:
            return "Email could not be sent. Please try again later."
    return render_template("email_form.html")

if __name__ == "__main__":
    app.run(debug=True)
