from App import app,socketio,db
import os
with app.app_context():
        db.create_all()

if __name__=="__main__":  
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app,port=port,debug=True,allow_unsafe_werkzeug=True)
    #app.run(port=5000,debug=True)
    #app_admin.run(debug=True)
