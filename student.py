from flask import *
import sqlite3
app=Flask(__name__)
app.secret_key='abc'



@app.route('/')
def home():
    return render_template("home.html")


@app.route('/register')
def register():
    return render_template("register.html")

# Studentregister
@app.route('/studentreg')
def studentreg():
    return render_template("studentreg.html")

@app.route('/savestd',methods=['POST'])
def savestd():
    if request.method=="POST":
        f=request.form['firstname']
        l=request.form['lastname']
        e=request.form['email']
        s='student'
        u=request.form['username']
        p=request.form['password']
        ph=request.form['phone_number']
        a=request.form['address']
        g=request.form['guardian']
        con=sqlite3.connect("studentmanagement.db")
        cursor1=con.cursor()
        cursor1.execute("insert into Login(username,password,usertype,status)values(?,?,?,?)",(u,p,s,0))
        cursor1.execute("select max(loginid) from Login")
        data=cursor1.fetchone()
        cursor1.execute("insert into Student(firstname,lastname,email,phone_number,address,guardian,logid)values(?,?,?,?,?,?,?) ",(f,l,e,ph,a,g,data[0]))

        con.commit()
    return render_template("login.html", message="Registration successful!")    


# Teacher register

@app.route('/teacherreg')
def teacherreg():
    return render_template("teacherreg.html")

@app.route('/savetchr',methods=['POST'])
def savetchr():
    if request.method=="POST":
        f=request.form['firstname']
        l=request.form['lastname']
        e=request.form['email']
        st='teacher'
        u=request.form['username']
        p=request.form['password']
        ph=request.form['phone_number']
        a=request.form['address']
        s=request.form['salary']
        ex=request.form['experience']
        con=sqlite3.connect("studentmanagement.db")
        cursor1=con.cursor()
        cursor1.execute("insert into Login (username,password,usertype,status)values(?,?,?,?) ",(u,p,st,0))
        cursor1.execute("select max(loginid) from Login")
        data=cursor1.fetchone()
        cursor1.execute("insert into Teacher(firstname,lastname,email,phone_number,address,salary,experience,logid)values(?,?,?,?,?,?,?,?) ",(f,l,e,ph,a,s,ex,data[0]))
        con.commit()
    return render_template("login.html", message="Teacher registered successfully!")


# Login

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logins',methods=['POST'])
def logincheck():
    if request.method=="POST":
        u=request.form["username"]
        p=request.form["password"]
        con=sqlite3.connect("studentmanagement.db")
        con.row_factory=sqlite3.Row
        cursor1=con.cursor()
        cursor1.execute("select * from Login where username=? and password=?",(u,p))
        data=cursor1.fetchone()
        con.close()
        print(data)
        if data:
            session["logid"]=data["loginid"]
            session["usertype"] = data["usertype"] 
            if data['usertype']=='teacher' and data['status']==1 :
                return render_template("teacherhome.html")
            elif data['usertype']=='student' and  data['status']==1:
                return render_template("studenthome.html")
            else:
                return("Oops....not approved")
        elif u=="admin" and p=="admin":
            return render_template("adminhome.html")
        else:
            return ("Invalid username and password")
                
    return render_template("login.html")

# Admin
# --------------------------------
@app.route('/viewstd')
def viewstd():
    con=sqlite3.connect("studentmanagement.db")
    con.row_factory=sqlite3.Row
    cursor1=con.cursor()
    cursor1.execute("select * from Student")
    data=cursor1.fetchall()
    return render_template("viewstd.html",view=data)


@app.route('/viewtchr')
def viewtchr():
    con=sqlite3.connect("studentmanagement.db")
    con.row_factory=sqlite3.Row
    cursor1=con.cursor()
    cursor1.execute("select * from Teacher")
    data=cursor1.fetchall()
    return render_template("viewtchr.html",view=data)

@app.route('/approvestudent')
def approvestudent():
    con=sqlite3.connect("studentmanagement.db")
    con.row_factory=sqlite3.Row
    cursor1=con.cursor()
    cursor1.execute("SELECT * FROM Student WHERE logid IN (SELECT loginid FROM Login WHERE status = 0) ")
    data=cursor1.fetchall()
    con.close()
    return render_template("approvestudent.html",view=data)


@app.route('/approvestd/<int:id>')
def approvestd(id):
    con=sqlite3.connect("studentmanagement.db")
    cursor1=con.cursor()
    cursor1.execute("UPDATE Login SET status = 1 WHERE loginid = ?", (id,))
    con.commit()
    return redirect(url_for('approvestudent'))


@app.route('/approveteacher')
def approveteacher():
    con=sqlite3.connect("studentmanagement.db")
    con.row_factory=sqlite3.Row
    cursor1=con.cursor()
    cursor1.execute("SELECT * FROM Teacher WHERE logid IN (SELECT loginid FROM Login WHERE status = 0)")
    data=cursor1.fetchall()
    con.close()
    return render_template("approveteacher.html",view=data)


@app.route('/approvetchr/<int:id>')
def approvetchr (id):
    con=sqlite3.connect("studentmanagement.db")
    cursor1=con.cursor()
    cursor1.execute("UPDATE Login SET status = 1 WHERE loginid = ?", (id,))
    con.commit()
    return redirect(url_for('approveteacher'))

@app.route('/deletestd')
def deletestd():
    con=sqlite3.connect("studentmanagement.db")
    con.row_factory=sqlite3.Row
    cursor1=con.cursor()
    cursor1.execute("select * from Student")
    data=cursor1.fetchall()
    return render_template("deletestd.html",view=data)


@app.route('/delstd/<int:id>')
def delstd(id):
    con=sqlite3.connect("studentmanagement.db")
    con.row_factory=sqlite3.Row
    cursor1=con.cursor()
    cursor1.execute("DELETE FROM Login WHERE loginid = (SELECT logid FROM Student WHERE studid=?)",(id,))
    cursor1.execute("delete from Student where studid=?",(id,))
    con.commit()
    return redirect(url_for('deletestd'))


@app.route('/deletetchr')
def deletetchr():
    con=sqlite3.connect("studentmanagement.db")
    con.row_factory=sqlite3.Row
    cursor1=con.cursor()
    cursor1.execute("select * from Teacher ")
    data=cursor1.fetchall()
    return render_template("deletetchr.html",view=data)


@app.route('/deltchr/<int:id>')
def deltchr(id):
    con=sqlite3.connect("studentmanagement.db")
    con.row_factory=sqlite3.Row
    cursor1=con.cursor()
    cursor1.execute("DELETE FROM Login WHERE loginid = (SELECT logid FROM Teacher WHERE teachid=?)",(id,))
    cursor1.execute("delete from Teacher where teachid=?",(id,))
    con.commit()
    return redirect(url_for('deletetchr'))

# Student
# --------------------------------
@app.route('/tchrlist')
def tchrlist():
    con=sqlite3.connect("studentmanagement.db")
    con.row_factory=sqlite3.Row
    cursor1=con.cursor()
    cursor1.execute("select * from Teacher")
    data=cursor1.fetchall()
    return render_template("tchrlist.html",view=data)


@app.route('/editstd')
def editstd():
     if "logid" in session and session.get("usertype")=="student":
        user=session["logid"]  
        con=sqlite3.connect("studentmanagement.db")
        con.row_factory=sqlite3.Row
        cursor=con.cursor()
        cursor.execute("SELECT * FROM student WHERE logid = ?", (user,))
        data=cursor.fetchone()
        con.close()
        return render_template("editstd.html", student=data)


@app.route("/updstd", methods=['POST'])
def updstd():
    if "logid" in session and session.get("usertype")=="student":
        user = session["logid"] 
        f = request.form['firstname']
        l = request.form['lastname']
        a = request.form['address']
        ph = request.form['phone_number']
        e = request.form['email']
        g = request.form['guardian']
        con = sqlite3.connect("studentmanagement.db")
        cursor1=con.cursor()
        cursor1.execute("UPDATE Student SET firstname =?,lastname =?,address =?,phone_number =?,email =?,guardian =? WHERE logid =?"
        , (f,l,a,ph,e,g,user))
        con.commit()
        con.close()
    return render_template("studenthome.html") 


@app.route("/stdlogout")
def stdlogout():
    session.clear()  
    return redirect(url_for("home"))

# Teacher
# --------------------------------
@app.route('/stdlist')
def stdlist():
    con=sqlite3.connect("studentmanagement.db")
    con.row_factory=sqlite3.Row
    cursor1=con.cursor()
    cursor1.execute("select * from Student")
    data=cursor1.fetchall()
    return render_template("stdlist.html",view=data)


@app.route('/edittchr')
def edittchr():
     if "logid" in session and session.get("usertype")=="teacher":
        user=session["logid"]  
        con=sqlite3.connect("studentmanagement.db")
        con.row_factory=sqlite3.Row
        cursor=con.cursor()
        cursor.execute("SELECT * FROM Teacher WHERE logid = ?", (user,))
        data=cursor.fetchone()
        con.close()
        return render_template("edittchr.html", student=data)


@app.route("/updtchr", methods=['POST'])
def updtchr():
    if "logid" in session and session.get("usertype")=="teacher":
        user = session["logid"] 
        f = request.form['firstname']
        l = request.form['lastname']
        a = request.form['address']
        ph = request.form['phone_number']
        e = request.form['email']
        s=request.form['salary']
        ex=request.form['experience']
        con = sqlite3.connect("studentmanagement.db")
        cursor1=con.cursor()
        cursor1.execute("UPDATE Teacher SET firstname =?,lastname =?,address =?,phone_number =?,email =?,salary=?,experience=? WHERE logid =?"
        , (f,l,a,ph,e,s,ex,user))
        con.commit()
        con.close()
    return render_template("teacherhome.html") 


@app.route("/tchrlogout")
def tchrlogout():
    session.clear()  
    return redirect(url_for("home"))




if __name__ =="__main__":
    app.run(debug=True)