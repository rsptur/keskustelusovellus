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

#Hakee aiheen viimeisimmän viestin ajan
def most_recent(topic): 
    try: 
        sql = text("SELECT TO_CHAR(MAX(sent_at), 'YYYY-MM-DD') FROM messages WHERE topic=:topic")
        result=db.session.execute(sql,{"topic":topic})  
        return result.fetchall() 
    except: 
        return False 

## Tallentaa viestin messages tauluun
def new_topic(message,topic): 
    try: 
        sql = text("INSERT INTO messages (message,topic,sent_at) VALUES (:message,:topic,current_timestamp)")
        db.session.execute(sql, {"message":message,"topic":topic})
        db.session.commit()  
        return True  
    except: 
        return False  
    
def show_messages(username):
    try: 
        sql = text("SELECT id FROM users WHERE username=:username")
        result=db.session.execute(sql,{"username":username})
        user=result.fetchone()
        sql = text("SELECT id,message,topic FROM messages WHERE id=:user_id")
        result=db.session.execute(sql, {"user_id":user[0]})
        return result.fetchall()
    except: 
        return False  

def modify_messages(message_id):
    try: 
        sql = text("DELETE FROM messages WHERE id=:message_id")
        result=db.session.execute(sql,{"message_id":message_id})
        db.session.commit()
        return True
    except: 
        return False    
    



    
