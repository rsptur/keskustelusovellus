from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from app import app
from sqlalchemy.sql import text

def login_user(username,password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            return True 
        else:
            return False  

def new_user(username,password): 
    hash_value = generate_password_hash(password)
    try: 
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()    
    except: 
        return False
    return login_user(username,password)    