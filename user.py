from flask import Flask, render_template, request
import sqlite3 as sql

from werkzeug.utils import redirect

connection=sql.connect("BookAdmin.db",check_same_thread=False)
listofBookuser = connection.execute("select name from sqlite_master where type='table' AND name='user'").fetchall()

if listofBookuser!=[]:
    print("Table exist already")
else:
    connection.execute('''create table user(
                             ID integer primary key autoincrement,
                             name text,
                             address text,
                             email text,
                             phone integer,
                             password text
                             )''')
    print("Table Created Successfully")

user=Flask(__name__)

@user.route("/",methods=["POST","GET"])
def user_login_details():
    if request.method == "POST":
        getname=request.form["name"]
        getaddress=request.form["address"]
        getemail=request.form["email"]
        getphone=request.form["phone"]
        getpassword=request.form["password"]
        print(getname)
        print(getaddress)
        print(getemail)
        print(getphone)
        print(getpassword)
        try:
            connection.execute("insert into user(name,address,email,phone,password)\
                                   values('" + getname + "','" + getaddress + "','" + getemail + "'," + getphone + ",'" + getpassword + "')")
            connection.commit()
            print("Student Data Added Successfully.")
        except Exception as e:
            print("Error occured ", e)

    return render_template("user_login.html")

@user.route("/uselogin",methods=["POST","GET"])
def use_login():
    if request.method=="POST":
        getemail=request.form["email"]
        getpassword=request.form["password"]
        print(getemail)
        print(getpassword)
        if getemail!="1" and getpassword!="0":
            return redirect("/viewbook")
    return render_template("uselogin.html")


@user.route("/viewbook")
def user_viewbook():
    cursor = connection.cursor()
    count = cursor.execute("select * from Book")
    result = cursor.fetchall()
    return render_template("viewbook.html", Book=result)

@user.route("/searchbook",methods=["POST","GET"])
def user_search_book():
    if request.method == "POST":
        getbookname=request.form["name"]
        print(getbookname)
        cursor = connection.cursor()
        count = cursor.execute("select * from book where bookname='"+getbookname+"'")
        result = cursor.fetchall()
        return render_template("searchbook.html", searchBook=result)

    return render_template("searchbook.html")

if __name__=="__main__":
    user.run()