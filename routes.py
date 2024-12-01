from flask import Flask
from flask import redirect, render_template, request, session
import users
import messages
import topics
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
            return render_template("error.html", message="Käyttäjätunnusta ei voitu luoda")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/aiheet")
def topiclist():
    result=topics.list_topics() 
    number=topics.number_messages()
    return render_template("form.html", count=len(result),ttopics=result,nro=number)

@app.route("/viestit",methods=["GET","POST"])
def messages():
    if request.method=="GET": 
        return render_template("write.html")
    if request.method=="POST": 
        topic = request.form["topic"]
        message = request.form["message"]
        if topics.new_topic(topic): 
            return redirect("/aiheet")
        if messages.new_message(message,topic): 
            return redirect("/aiheet")
        else: 
            return render_template("error.html", message="Viestiä ei voitu lähettää")
