from flask import Flask
from flask import redirect, render_template, request, session
import users
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
        if len(username)<1: 
            return render_template("error.html", message="Käyttäjätunnus puuttuu tai on liian lyhyt")
        if len(username)>100: 
            return render_template("error.html", message="Käyttäjätunnus on liian pitkä")
        if len(password)<1: 
            return render_template("error.html", message="Salasana puuttuu tai on liian lyhyt")
        if len(password)>100: 
            return render_template("error.html", message="Salasana on liian pitkä")
        elif users.new_user(username,password): 
            return redirect("/")
        else: 
            return render_template("error.html", message="Käyttäjätunnusta ei voitu luoda")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/topics")
def topiclist(): 
    result=topics.list_topics() 
    return render_template("form.html", count=len(result),topics=result)

@app.route("/viestit",methods=["GET","POST"])
def messages():
    if request.method=="GET": 
        return render_template("write.html")
    if request.method=="POST": 
        topic = request.form["topic"]
        message = request.form["message"]
        if topics.new_topic(message,topic):
            return redirect("/topics")
        else: 
            return render_template("error.html", message="Viestiä ei voitu lähettää")

@app.route("/topic/<string:topic>")
def viestilista(topic): 
    result=topics.list_messages(topic)
    result2=len(result)
    result3=topics.most_recent(topic)
    result3=result3[-1][0]
    return render_template("topic.html",topics=result, count=result2,time=result3)

@app.route("/etsi",methods=["GET","POST"])
def search(): 
    if request.method=="GET": 
        return render_template("search_messages.html")
    if request.method=="POST":
        query= request.form["query"]
        sql=text("SELECT message FROM messages WHERE message like (:query)")
        result = db.session.execute(sql, {"query":"%"+query+"%"})
        found = result.fetchall()
        return render_template("search_results.html",topics=found)

@app.route("/muokkaa",methods=["GET","POST"])
def modify():  
    if "username" in session:
        if request.method=="GET": 
            result=topics.show_messages(session["username"])
            return render_template("user_messages.html",topics=result)
        if request.method=="POST":
            message_id= request.form["viestinro"]
            if topics.modify_messages(message_id):
                result=topics.show_messages(session["username"])
                return render_template("user_messages.html",topics=result)
            else: 
                return "Viestiä ei löytynyt tai ei voitu poistaa"

#admin can delete any
#@app.route("/admin")