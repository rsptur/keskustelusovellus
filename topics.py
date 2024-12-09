from flask import session
from db import db
from app import app
import users
from sqlalchemy.sql import text

def list_topics(): 
    try: 
        sql =text("SELECT DISTINCT topic FROM messages")
        result=db.session.execute(sql)  
        return result.fetchall()
    except: 
        return False 

def list_messages(topic): 
    try: 
        sql = text("SELECT message FROM messages WHERE topic=:topic")
        result=db.session.execute(sql,{"topic":topic})  
        return result.fetchall() 
    except: 
        return False 

def most_recent(topic): 
    try: 
        sql = text("SELECT TO_CHAR(MAX(sent_at), 'YYYY-MM-DD') FROM messages WHERE topic=:topic")
        result=db.session.execute(sql,{"topic":topic})  
        return result.fetchall() 
    except: 
        return False 

def new_topic(message,topic): 
    try: 
        sql = text("INSERT INTO messages (message,topic,sent_at) VALUES (:message,:topic,current_timestamp)")
        db.session.execute(sql, {"message":message,"topic":topic})
        db.session.commit()  
        return True  
    except: 
        return False  

def modify_messages(message_id,username):
    if users.is_admin(username): 
        try: 
            sql = text("DELETE FROM messages WHERE id=:message_id")
            db.session.execute(sql,{"message_id":message_id})
            db.session.commit()
            return True
        except: 
            return False        
    if users.is_users(message_id,username):
        try: 
            sql = text("DELETE FROM messages WHERE id=:message_id")
            db.session.execute(sql,{"message_id":message_id})
            db.session.commit()
            return True
        except: 
            return False   
    else: 
        return False            

def admin_messages():
    sql = text("SELECT id,message,topic,TO_CHAR(sent_at, 'YYYY-MM-DD') FROM messages")
    result=db.session.execute(sql)
    return result.fetchall()




    
