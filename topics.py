from flask import session
from db import db
from app import app
import messages
import users
from sqlalchemy.sql import text

def list_topics(): 
    try: 
        sql =text("SELECT DISTINCT topic FROM topics")
        result=db.session.execute(sql)  
        return result.fetchall()
    except: 
        return False 

def number_messages(): 
    try: 
        sql = text("SELECT COUNT(DISTINCT topic) FROM topics")
        result=db.session.execute(sql)  
        return result.fetchall() 
    except: 
        return False 
    
def new_topic(topic): 
    try: 
        sql = text("INSERT INTO topics (topic) VALUES (:topic)")
        db.session.execute(sql, {"topic":topic})
        db.session.commit()  
        return True  
    except: 
        return False 
    

    