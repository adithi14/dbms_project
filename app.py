from flask import Flask,request,render_template

app=Flask(__name__)



@app.route("/user/<Adithi>")
def profile(Adithi):
    return f"{Adithi}\'s profile"

'''@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        return do_the_login()
    else:
        return show_login_form()'''

@app.route("/")
def hello_world():
    
    return render_template("index.html")

@app.route("/greet")


def greet():
    name=request.args.get("name","everyone")
    return render_template("greet.html",name=name)