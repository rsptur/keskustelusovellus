from flask import Flask
from flask import redirect, render_template, request, session
import users
from db import db
from app import app
from sqlalchemy.sql import text

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login_user(username,password): 
        session["username"] = username
        return redirect("/")
    else: 
        return "Väärä salasana tai et ole vielä rekisteröitynyt"
    
@app.route("/new",methods=["GET","POST"])
def new(): 
    if request.method=="GET": 
        return render_template("add.html")
    if request.method=="POST": 
        username = request.form["username"]
        password = request.form["password"]
        if users.new_user(username,password): 
            return redirect("/")
        else: 
            return "Tapahtui virhe"

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
