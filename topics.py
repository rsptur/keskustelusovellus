from flask import session
from db import db
from app import app
import users
from sqlalchemy.sql import text

#Hakee aiheet 
def list_topics(): 
    try: 
        sql =text("SELECT DISTINCT topic FROM messages")
        result=db.session.execute(sql)  
        return result.fetchall()
    except: 
        return False 

#Hakee viestit aiheen mukaan
def list_messages(topic): 
    try: 
        sql = text("SELECT message FROM messages WHERE topic=:topic")
        result=db.session.execute(sql,{"topic":topic})  
        return result.fetchall() 
    except: 
        return False 

#Hakee aiheen viimeisimmät viestit
def most_recent(topic): 
    try: 
        sql = text("SELECT MAX(sent_at) FROM messages WHERE topic=:topic")
        result=db.session.execute(sql,{"sent_at":sent_at})  
        return result.fetchone() 
    except: 
        return False 

## Tallentaa viestin messages tauluun
def new_topic(message,topic): 
    try: 
        sql = text("INSERT INTO messages (message,topic) VALUES (:message,:topic)")
        db.session.execute(sql, {"message":message,"topic":topic})
        db.session.commit()  
        return True  
    except: 
        return False  
    
def modify_messages(username):
    try: 
        sql = text("SELECT user_id FROM users WHERE username=:username")
        result=db.session.execute(sql,{"username":username})
        #sql = text("SELECT messages,topic FROM messages WHERE user_id=:user_id")
        #result=db.session.execute(sql, {"user_id":user_id})
        return result.fetchone()
    except: 
        return False     
    



    
