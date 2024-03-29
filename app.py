from User import create_app,socketio,redis_store
import os
from User.Controllers.fonction import *
from threading import Thread
from flask import request
from flask_redis import FlaskRedis
from dotenv import load_dotenv

load_dotenv()

app=create_app(conf=None)
processed_requests = {}

#SECURITY HEADER
@app.after_request
def set_secure_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.before_request
def update_session_time():
    if user.id not in processed_requests and user.id is not None:
        last_activity_key = f'last_activity:{user.id}'
        redis_store.set(last_activity_key, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ex=3)
        session['online_users'] = len(redis_store.keys('last_activity:*'))
        processed_requests[user.id] = True

if __name__=="__main__":  
    socketio.run(app,host="0.0.0.0",port=int(os.getenv("PORT")),debug=os.getenv("DEBUG"))
