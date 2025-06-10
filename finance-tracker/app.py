from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy user database (replace with real DB in production)
users = {
    'admin': 'admin'  # example user for testing
}

# Redirect root to login
@app.route('/')
def home():
    return redirect(url_for('login'))

# Login page & form handling
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username] == password:
            return redirect(url_for('dashboard', username=username))
        else:
            return "Invalid credentials. Please go back and try again."
    return render_template('login.html')

# Signup page & form handling
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users:
            return "Username already exists. Please choose another."
        else:
            users[username] = password
            return redirect(url_for('login'))
    return render_template('signup.html')

# Dashboard page
@app.route('/dashboard')
def dashboard():
    username = request.args.get('username', 'user')
    return f"<h1>Welcome to Finora, {username}!</h1>"

if __name__ == '__main__':
    print("\nRegistered routes:")
    for rule in app.url_map.iter_rules():
        print(rule)
    app.run(debug=True)
