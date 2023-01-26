from flask import Flask,request,render_template,redirect,session
from flaskext.mysql import MySQL
import hashlib
app=Flask(__name__)


@app.route("/")
def hello_world():
    
    return f"hello"


app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='Ida@14062002'
app.config['MYSQL_DATABASE_DB']='dbms_mini'
#app.config['MYSQL_DATABASE_PORT']="3306"


#mysql=MySQL(app)
mysql = MySQL()
mysql.init_app(app)

app.secret_key = 'adithiaiman'

@app.route('/login',methods = ['POST','GET'])
def login():
    if request.method=="POST":
        #  Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html",message="must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html",message="must provide password")

        # Query database for username
        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT * FROM users WHERE name = %s",[request.form.get("username")])
        
        row = cursor.fetchone()#fetches the first entry of query output
        #password=hashlib.md5(request.form.get("password").encode())
        #print(password)
        # Ensure username exists and password is correct
        #print(row[0])
        if row is None:
            print("hi")
            print(request.form.get("username"))
            return render_template("error.html",message="invalid username")
        
        # Remember which user has logged in
        session["user_id"] = row[0]
        print(session["user_id"])
        print("hrllo")
        # Redirect user to home page
        return redirect("/index.html")
    
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/index.html") #home page
def home():
    return render_template("index.html",person=session["user_id"])

@app.route('/empdet',methods=["POST","GET"])
def emplogin():
    if request.method=="GET":
        return render_template("emp.html",person=session["user_id"])
    
    if request.method=="POST": 
        print("employee details")
        empid=request.form['empid']
        empname=request.form['name']
        dept=request.form['dept']
        date=request.form['dob']
        gend=request.form['gender']
        cur1=mysql.get_db().cursor()
        cur1.execute('''INSERT INTO employee values(%s,%s,%s,%s,%s)''',(empid,empname,dept,date,gend))
        mysql.get_db().commit()
        cur1.close()
        return redirect("/displayemp")


@app.route('/travelrequest',methods=["POST","GET"])
def travelreq():
    if request.method=="GET":
        return render_template("travel.html",person=session["user_id"])
    
    if request.method=='POST':
        trid=request.form['trid']
        empname=request.form['name']
        empid=request.form['empid']
        purp=request.form['purpose']
        #tripno=request.form['tripno']
        cur=mysql.get_db().cursor()
        print("cursor created")
        cur.execute('''INSERT INTO travelreq values(%s,%s,%s,%s)''',(trid,empname,empid,purp))
        print("insertion done")
        mysql.get_db().commit()
        cur.close()
        return redirect("/displaytravreq")

@app.route("/localtrip",methods=["POST","GET"])
def loc_trip():
    if request.method=="GET":
        return render_template("localtr.html",person=session["user_id"])
    
    if request.method=="POST":
        tripno=request.form['tripno']
        place=request.form["place"]
        start=request.form["start"]
        end=request.form["end"]
        trid=request.form["trid"]
        cur1=mysql.get_db().cursor()
        cur1.execute('''INSERT INTO local_trip values(%s,%s,%s,%s,%s)''',(tripno,place,start,end,trid))
        mysql.get_db().commit()
        cur1.close()
        return redirect("/displayloctr")


@app.route("/outstrip",methods=["POST","GET"])
def out_trip():
    if request.method=="GET":
        return render_template("outst.html",person=session["user_id"])
    
    if request.method=="POST":
        tripno=request.form['tripno']
        place=request.form["place"]
        start=request.form["start"]
        end=request.form["end"]
        addr=request.form['addr']
        mode=request.form["mode"]
        trid=request.form["trid"]
        cur1=mysql.get_db().cursor()
        cur1.execute('''INSERT INTO outstation_trip values(%s,%s,%s,%s,%s,%s,%s)''',(tripno,place,start,end,addr,mode,trid))
        mysql.get_db().commit()
        cur1.close()
        return redirect("/displayoutr")

@app.route("/locexp",methods=["POST","GET"])
def locexp():
    if request.method=="GET":
        return render_template("loc_exp.html",person=session["user_id"])
    
    if request.method=="POST":
        expid=request.form['expid']
        city=request.form["city"]
        cat=request.form["cat"]
        vend=request.form["vend"]
        amt=request.form["amt"]
        edate=request.form['edate']
        tripno=request.form['tripno']

        cur1=mysql.get_db().cursor()
        cur1.execute('''INSERT INTO local_exp values(%s,%s,%s,%s,%s,%s,%s)''',(expid,city,cat,vend,amt,edate,tripno))
        mysql.get_db().commit()
        cur1.close()
        return redirect("/diplaylocexp")

@app.route("/outexp",methods=["POST","GET"])
def outexp():
    if request.method=="GET":
        return render_template("out_exp.html",person=session["user_id"])
    
    if request.method=="POST":
        expid=request.form['expid']
        city=request.form["city"]
        cat=request.form["cat"]
        vend=request.form["vend"]
        amt=request.form["amt"]
        edate=request.form['edate']
        tripno=request.form['tripno']

        cur1=mysql.get_db().cursor()
        cur1.execute('''INSERT INTO outst_exp values(%s,%s,%s,%s,%s,%s,%s)''',(expid,city,cat,vend,amt,edate,tripno))
        mysql.get_db().commit()
        cur1.close()
        return redirect("/dispoutexp")


@app.route("/displayemp")
def distable(): #only displaying values
    cur=mysql.get_db().cursor()
    value=cur.execute("SELECT * FROM employee")

    if value > 0:
        empdetails=cur.fetchall()
        return render_template("empdisp.html",empdetails=empdetails)
 

@app.route("/displaytravreq")
def distrav():
    cur=mysql.get_db().cursor()
    value=cur.execute("SELECT * FROM travelreq")

    if value > 0:
        travreq=cur.fetchall()
        return render_template("trareqdisp.html",travreq=travreq)


@app.route("/displayloctr")
def disloc():
    cur=mysql.get_db().cursor()
    value=cur.execute("SELECT * FROM local_trip")

    if value>0:
        loctr=cur.fetchall()
        return render_template("disploctr.html",loctr=loctr)


@app.route("/displayoutr")
def disout():
    cur=mysql.get_db().cursor()
    value=cur.execute("SELECT * FROM outstation_trip")

    if value>0:
        outr=cur.fetchall()
        return render_template("dispout.html",outr=outr)

@app.route("/displaylocexp")
def dislexp():
    cur=mysql.get_db().cursor()
    value=cur.execute("SELECT * FROM local_exp")

    if value>0:
        lexp=cur.fetchall()
        return render_template("displexp.html",lexp=lexp)

@app.route("/displayoutexp")
def disoexp():
    cur=mysql.get_db().cursor()
    value=cur.execute("SELECT * FROM outst_exp")

    if value>0:
        oexp=cur.fetchall()
        return render_template("dispoexp.html",oexp=oexp)


@app.route("/views")
def views():
    return render_template("views.html")

    
if __name__ == "__main__":
    app.run(host='localhost',port=5000)

