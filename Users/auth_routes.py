from flask import Blueprint, render_template, request, redirect, session, url_for
import hashlib
import pymysql

# Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__, template_folder='templates/auth')

# Define the database connection
db = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    database='pro',
    
    cursorclass=pymysql.cursors.DictCursor
)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        # Check if the username is already taken
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            if cursor.fetchone():
                return "Username already taken. Please choose a different username."

            # Insert the new user into the database
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
            db.commit()
            session['username'] = username
            return "SignedUp successfully!"

    return render_template('signup.html')

@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        # Check if the provided username and password match a user in the database
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()

            if user:
                session['username'] = username
                return "Signed in successfully!"
            else:
                return "Invalid username or password. Please sign up."

    return render_template('signin.html')

@auth_bp.route('/logout')
def logout():
    # Remove the username from the session, effectively logging the user out
    session.pop('username', None)
    return redirect(url_for('auth.signin'))
