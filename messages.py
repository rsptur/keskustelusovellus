from flask import session
from db import db
from app import app
import topics
import users
from sqlalchemy.sql import text


def list_messages():
    try: 
        sql=text("SELECT topic FROM topics")
        result=db.session.execute(sql)
        return result.fetchall()  
    except: 
        return False 
        
def new_message(message,topic): 
    try: 
        sql = "INSERT INTO messages (message,topic) VALUES (:message,:topic)"
        db.session.execute(sql, {"message":message,"topic":topic})
        db.session.commit() 
        return True  
    except: 
        return False
