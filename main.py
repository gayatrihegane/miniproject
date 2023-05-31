from flask import Flask,render_template,redirect,request,session
import mysql.connector
from werkzeug.utils import secure_filename


app=Flask(__name__)
app.secret_key="Gayatri"


@app.route("/Admin",methods=["GET","POST"])
def Admin():
    if(request.method == "GET"):
        return render_template("Admin.html")
    else:
        unm = request.form["unm"]
        pwd = request.form["pwd"]
        
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Gayatri@123",   
                database ='cafe'                        
                )
        cursor = mydb.cursor()
        
        sql = '''select count(*) from userinfo where unm=%s
                      and pwd=%s and login='admin'  '''
        val = (unm,pwd)
        cursor.execute(sql,val)
        record = cursor.fetchone()
        if(int(record[0]) == 1):
            session["unm"] = unm
            return redirect("/Adminhome")
        else:
           return redirect("/Admin")

        
@app.route("/Adminhome")
def Adminhome():
    if("unm" in session):
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Gayatri@123",   
                database = 'cafe'                        
                )
        cursor = mydb.cursor()
        sql = "select * from cafe"
        cursor.execute(sql)
        records = cursor.fetchall()    
        return render_template("Adminhome.html",cafe=records)
    else:
        return redirect("/Admin")
        

@app.route("/Login",methods=["GET","POST"])
def Login():
    if(request.method == "GET"):
        return render_template("Login.html")
    else:
        unm = request.form["unm"]
        pwd = request.form["pwd"]
        
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Gayatri@123",   
                database ='cafe'                        
                )
        cursor = mydb.cursor()
        
        sql = '''select count(*) from userinfo where unm=%s and pwd=%s'''
        val = (unm,pwd)
        cursor.execute(sql,val)
        record = cursor.fetchone()
        if(int(record[0]) == 1):
            session["unm"] = unm
            return redirect("/")
        else:
            return redirect("/Login")

@app.route("/Signup",methods=["GET","POST"])      
def Signup():
    if(request.method == "GET"):
        return render_template("Signup.html")
    else:
        unm = request.form["unm"]
        pwd = request.form["pwd"]
        mail_id = request.form["mail_id"]

        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Gayatri@123",   
                database = 'cafe'                        
                )
        cursor = mydb.cursor()
        sql = '''insert into userinfo(unm,pwd,mail_id) values (%s,%s,%s)'''       
        val = (unm,pwd,mail_id)
        cursor.execute(sql,val)
        mydb.commit()
        mydb.close()
        return redirect("/Login")
    

def showallitems():
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Gayatri@123",   
                database = 'cafe'                        
                )
    cursor = mydb.cursor()
    sql = "select * from Cafe"
    cursor.execute(sql)
    records = cursor.fetchall()    
    return render_template("showallitems.html",cafe=records)

def Details(id):
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Gayatri@123",   
                database = 'cafe'                        
                )
    cursor = mydb.cursor()
    sql = "select * from Cafe where id=%s"
    val = (id,)
    cursor.execute(sql,val)
    details= cursor.fetchone()        
    return render_template("Details.html",cafe=details)



@app.route("/additem",methods=["GET", "POST"])
def additem():
    if("unm" not in session):
        return redirect("/Admin")
    else:
        if(request.method == "GET"):
            return render_template("additem.html")
        else:
            itemnm=request.form["itemnm"]
            price=request.form["price"]
            p=request.files["photo"]
            qty=request.form["qty"]
            p.save("static\\image\\"+secure_filename(p.filename))
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Gayatri@123",   
                database = 'cafe'                        
                )
            cursor = mydb.cursor()
            sql= "insert into cafe (itemnm,price,photo,qty) value (%s,%s,%s,%s)"
            val=(itemnm,price,p.filename,qty)
            cursor.execute(sql,val)
            mydb.commit()
            mydb.close()
            return redirect("/Adminhome")
    

@app.route("/edit/<id>",methods=["GET","POST"])
def edit(id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Gayatri@123",   
        database = 'cafe'                        
        )
    cursor = mydb.cursor()
    if(request.method=="GET"):
        sql = "select * from Cafe where id=%s"
        val = (id,)
        cursor.execute(sql,val)
        record = cursor.fetchone()    
        return render_template("edit.html",cafe=record)
    else:
        itemnm = request.form["itemnm"]
        price = request.form["price"]
        photo = request.form["photo"]
        qty = request.form["qty"]
        
        sql = '''update Cafe set itemnm=%s,
                 price=%s,photo=%s,qty=%s 
                 where id=%s'''
        val = (itemnm,price,photo,qty,id)
        cursor.execute(sql,val)
        mydb.commit()
        mydb.close()
        return redirect("/Adminhome")
    
@app.route("/Removeitem/<id>")
def Removeitem(id):
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Gayatri@123",   
                database = 'cafe'                        
                )
    cursor = mydb.cursor()
    sql = "delete from cafe where id=%s"
    val =(id,)
    cursor.execute(sql,val)
    mydb.commit()
    mydb.close()
    return redirect("/Adminhome")  


@app.route("/Addtocart",methods=["GET","POST"])
def Addtocart():
    if("unm" not in session):
        return redirect("/Login")
    else:
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Gayatri@123",   
                database = 'cafe'                        
                )
    cursor = mydb.cursor()
    unm = session["unm"]
    id=request.form["id"]
    qty = request.form["qty"]
    sql = "select count(*) from mycart where username=%s and id=%s"
    val = (unm,id)
    cursor.execute(sql,val)
    result = cursor.fetchone()
    if(result[0] == 0):
        sql = "insert into mycart(id,qty,username) values(%s,%s,%s)"    
        val = (id,qty,unm)
        cursor.execute(sql,val)
        mydb.commit()
        mydb.close()
        return redirect("/showcartitems")
    else:
        return "Item already present in cart.."
    

def showcartitems():
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Gayatri@123",   
                database = 'cafe'                        
                )
    cursor = mydb.cursor()
    sql = '''select c.id,c.itemnm,c.price,
             c.photo,m.qty from cafe c 
             inner join mycart m on c.id = m.id 
             and m.username=%s'''
    val = (session["unm"],)
    cursor.execute(sql,val)
    records = cursor.fetchall()
    sql = "select sum(qty*price) from cartitems_vw where username=%s"
    val = (session["unm"],)
    cursor.execute(sql,val)
    sum = cursor.fetchone()
    session["total"] = sum[0]
    return render_template("showcartitems.html",cafe = records)

@app.route("/RemovefromCart/<id>")
def RemovefromCart(id):
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Gayatri@123",   
                database = 'cafe'                        
                )
    cursor = mydb.cursor()
    sql = "delete from mycart where username=%s and id=%s"
    val = (session["unm"],id)
    cursor.execute(sql,val)
    mydb.commit()
    mydb.close()
    return redirect("/showcartitems")


def updatefromCart():
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Gayatri@123",   
                database = 'cafe'                        
                )
    cursor = mydb.cursor()
    unm=session["unm"]
    id=request.form["id"]
    qty = request.form["qty"]
    sql = "update mycart set qty=%s where id=%s and username=%s"
    val = (qty,id,unm)
    cursor.execute(sql,val)
    mydb.commit()
    mydb.close()
    return redirect("/showcartitems")


def MakePayment():
    if(request.method == "GET"):
        return render_template("MakePayment.html")
    else:
        cdno = request.form["cdno"]
        cvv = request.form["cvv"]
        expdt = request.form["expdt"]
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Gayatri@123",   
                database = 'cafe'                        
                )
        cursor = mydb.cursor()
        sql = '''select count(*) from carddetails 
                where cdno=%s and cvv=%s and expdt = %s'''
        val = (cdno,cvv,expdt)
        cursor.execute(sql,val)
        record = cursor.fetchone()
        if(int(record[0]) == 1):
            total = session["total"]
            sql1 = "update carddetails set total = total - %s where cdno=%s"
            sql2 = "update carddetails set total = total + %s where cdno=100"
            val1 = (total,cdno)
            val2 = (total,)
            cursor.execute(sql1,val1)
            cursor.execute(sql2,val2)
            mydb.commit()
        else:
            cdno = request.form["cdno"]
            cvv = request.form["cvv"]
            expdt = request.form["expdt"]
            cursor = mydb.cursor()
            sql="insert into carddetails(cdno,cvv,expdt) values(%s,%s,%s)"
            val=(cdno,cvv,expdt)
            cursor.execute(sql,val)
            mydb.commit()
    return redirect("/")


def Signout():
    session.clear()
    return redirect("/Login")

        
    
app.add_url_rule("/additem","additem",additem)
app.add_url_rule('/','', showallitems)
app.add_url_rule("/Details/<id>",'item',Details)
app.add_url_rule("/Signup",'signup',Signup,methods=["GET","POST"])
app.add_url_rule("/Login",'login',Login,methods=["GET","POST"])
app.add_url_rule("/Signout",'signout',Signout)
app.add_url_rule("/Addtocart",'Addtocart',Addtocart,methods=["GET","POST"])
app.add_url_rule("/showcartitems",'showcartitems',showcartitems,methods=["GET","POST"])
app.add_url_rule("/Updateitem",'updateitem',updatefromCart,methods=["GET","POST"])
app.add_url_rule("/MakePayment",'makepayment',MakePayment,methods=["GET","POST"])


if(__name__=="__main__"):
    app.run(debug=True)