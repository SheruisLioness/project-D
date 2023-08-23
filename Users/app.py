from flask import Flask, render_template, request, redirect, session
import hashlib
import pymysql

app = Flask(__name__)
app.template_folder = 'templates'
app.secret_key = 'your_secret_key'

# Configure your MySQL connection
db = pymysql.connect(host='localhost', user='root', password='1234', db='project')
cursor = db.cursor()

@app.route('/')
def home():
    return redirect('/signin')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        # Check if the username is already taken
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            return "Username already taken. Please choose a different username."

        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        db.commit()
        session['username'] = username  # Automatically sign in the user
        return "SignedUp in successfully!"
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            session['username'] = username
            return "Signed in successfully!"
        else:
            return "Invalid username or password. Please sign up."
    return render_template('signin.html')

@app.route('/welcome')
def welcome():
    if 'username' in session:
        return f"Welcome, {session['username']}!"
    return redirect('/signin')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/signin')

if __name__ == '__main__':
    app.run(debug=True)
