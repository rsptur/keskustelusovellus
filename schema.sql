CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username UNIQUE TEXT, 
    password TEXT);  

CREATE TABLE messages (
    id SERIAL PRIMARY KEY, 
    message TEXT, 
    topic TEXT, 
    sent_at TIMESTAMP,
    user_id INTEGER REFERENCES users,
    topic_id INTEGER REFERENCES topics); 