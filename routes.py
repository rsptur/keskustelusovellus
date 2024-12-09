from flask import Flask
from flask import redirect, render_template, request, session, abort
import users
import topics
import secrets 
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
        session["csrf_token"] = secrets.token_hex(16)
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
            return render_template("error.html", message="Käyttäjätunnus on jo käytössä tai sitä ei voitu luoda")

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
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        topic = request.form["topic"]
        message = request.form["message"]
        while len(topic)>5000: 
            render_template("error.html", message="Aiheesi on liian pitkä")
        while len(message)>5000: 
            render_template("error.html", message="Viesti on liian pitkä")
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
            
@app.route("/add_admin",methods=["GET","POST"])
def register_admin(): 
    if request.method=="GET": 
        return render_template("admin_request.html")   
    if request.method=="POST": 
        user=session["username"]
        if users.add_admin(user): 
            return redirect("/")
        else: 
            return render_template("error.html", message="Ylläpitäjää ei voitu lisätä")

@app.route("/admin",methods=["GET","POST"])    
def admin_page():
    if request.method=="GET":
        result=topics.admin_messages(session["username"])             
        return render_template("admin.html",topics=result)   
    if request.method=="POST":
        if request.method=="POST":
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
            message_id= request.form["number"]
            if topics.modify_messages(message_id, session["username"]):
                result=topics.admin_messages()
                return render_template("admin.html",topics=result)  
            else: 
                return render_template("error.html", message="Viestiä ei voitu poistaa")      

@app.route("/modify",methods=["GET","POST"])    
def user_page():
    if request.method=="GET":
        result=topics.admin_messages()            
        return render_template("user_messages.html",topics=result)   
    if request.method=="POST":
        if request.method=="POST":
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
            message_id= request.form["number"]
            if topics.modify_messages(message_id,session["username"]):
                result=topics.admin_messages()
                return render_template("user_messages.html",topics=result)  
            else: 
                return render_template("error.html", message="Viestiä ei voitu poistaa")   
            
