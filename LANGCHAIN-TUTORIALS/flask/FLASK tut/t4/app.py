from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == 'admin' and password == 'secret':
        return render_template('index.html', username=username)
    else:
        return render_template('login.html', error='Invalid credentials. Please try again.')



if __name__ == '__main__':
    app.run(debug=True)