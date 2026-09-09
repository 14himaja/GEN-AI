from flask import Flask, request, render_template, redirect, url_for
from database import init_db, register_user, verify_user

app = Flask(__name__)

# Initialize database on startup
init_db()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if verify_user(username, password):
        return render_template('index.html', username=username)
    else:
        return render_template('login.html', error='Invalid username or password.')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if register_user(username, password):
            return redirect(url_for('login_page'))
        else:
            return render_template('register.html', error='Username already exists.')
    
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
