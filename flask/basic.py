from flask import Flask,request
app = Flask(__name__) 

@app.route('/')
def hello_world():
    return 'Hello, World!\n',404



@app.route('/about')
def about():
    return "<h1>About Page</h1><p>This is a simple Flask application.</p>"

@app.route('/greet/<name>')
def greet(name):
    return f"<h1>Hello, {name}!</h1>"

@app.route('/add/<int:num1>/<int:num2>')
def add(num1, num2):
    result = num1 + num2
    return f"<h1>The sum of {num1} and {num2} is {result}.</h1>"


@app.route('/handle_url_params')
def handle_url_params():
    return request.args

@app.route('/handle_url_parameters')
def handle_url_parameters():
    if 'greeting'in request.args.keys() and 'name' in request.args.keys():
        greeting = request.args['greeting']
        name = request.args['name']
        return f"<h1>{greeting}, {name}!</h1>"  
    else:
        return "<h1>Missing 'greeting' or 'name' parameter.</h1>"

@app.route('/home',methods=['GET','POST'])
def home():
    return "<h1>POST request received!</h1>"



if __name__ == '__main__':
    app.run(debug=True)