from App import db
from datetime import datetime

class Pomodoro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time = db.Column(db.Integer, default=0)
    utilisateur = db.relationship('User', backref='user_concerne', foreign_keys=[id_utilisateur])


class Groupstud(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_createur = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    titre = db.Column(db.String)
    time_debut = db.Column(db.String)
    time_fin = db.Column(db.String)
    utilisateur = db.relationship('User', backref='groupecreat', foreign_keys=[id_createur])

class Grouptasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_groupe = db.Column(db.Integer, db.ForeignKey('groupstud.id'), nullable=False)
    tache = db.Column(db.String)
    utilisateur = db.relationship('Groupstud', backref='grouptask', foreign_keys=[id_groupe])

class Groupmessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_groupe = db.Column(db.Integer, db.ForeignKey('groupstud.id'), nullable=False)
    message = db.Column(db.String)
    audio_data = db.Column(db.LargeBinary)
    audio_data_path=db.Column(db.String)
    date_env=db.Column(db.DateTime,default=datetime.utcnow)
    id_user=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    utilisateur = db.relationship('User', backref='usermessage', foreign_keys=[id_user])


class Groupmember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_groupe = db.Column(db.Integer, db.ForeignKey('groupstud.id'), nullable=False)
    id_member =db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    statut = db.Column(db.String,default="attente")
    utilisateur = db.relationship('User', backref='groupmember', foreign_keys=[id_member])
    groupe = db.relationship('Groupstud', backref='group_groupe', foreign_keys=[id_groupe])

class Best_time_25(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_us =db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    temps = db.Column(db.Integer)
    utilisateur = db.relationship('User', backref='best_time_25', foreign_keys=[id_us])

class Memorix(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_us =db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nombre = db.Column(db.Integer)
    utilisateur = db.relationship('User', backref='best_memorix', foreign_keys=[id_us])