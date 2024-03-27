from User import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(50))
    mdp=db.Column(db.String(50))
    superadmin=db.Column(db.String(50))
