from flask import Flask,render_template

app= Flask(__name__,template_folder='templates')

@app.route('/') 
def index():
    myvalue = "Hello, World!"
    myresult = 42
    mylist = [1, 2, 3, 4, 5]
    return render_template('index.html',value=myvalue,result=myresult,list=mylist)

if __name__ == '__main__':
    app.run(debug=True)