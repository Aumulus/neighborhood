from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

# Email configuration — replace with your Gmail & app password
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'         # your Gmail address
app.config['MAIL_PASSWORD'] = 'your_app_password'            # your Gmail App Password

mail = Mail(app)

# Users dictionary: email keys, store username & password
users = {
    'admin@example.com': {
        'username': 'admin',
        'password': 'admin'
    }
}

# New clean welcome landing page
@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = users.get(email)
        if user and user['password'] == password:
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            return "Invalid email or password. Please go back and try again."
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if email in users:
            return "Email already registered. Please log in instead."
        else:
            users[email] = {
                'username': username,
                'password': password
            }

            # Send welcome email
            try:
                msg = Message(
                    subject='Welcome to Finora!',
                    recipients=[email],
                    body=f"Hi {username},\n\nThanks for signing up for Finora!\n\nYour login email: {email}"
                )
                mail.send(msg)
                print(f"Sent welcome email to {email}")
            except Exception as e:
                print(f"Failed to send email: {e}")

            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=username)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
