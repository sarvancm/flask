from flask import Flask, render_template, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database configuration
db_url = "postgresql://username:password@localhost:5432/database_name"

# Registration route
@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert user record into the database
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
        conn.commit()
        cur.close()
        conn.close()

        return redirect('/login')

    return render_template('register.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Retrieve user record from the database
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[3], password):
            # Store user session information
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect('/')
        else:
            return 'Invalid email or password'

    return render_template('login.html')


# Logout route
@app.route('/logout')
def logout():
    # Clear session data
    session.clear()
    return redirect('/login')


app.run()