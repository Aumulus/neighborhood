from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

users = {
    'admin@example.com': {
        'username': 'admin',
        'password': 'admin'
    }
}

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
            return redirect(url_for('welcome_user'))
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
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/welcome_user')
def welcome_user():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    return render_template('welcome_user.html', username=username)

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
