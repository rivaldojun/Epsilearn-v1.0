from User import db
from datetime import datetime

class Retrait(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_demandeur=db.Column(db.Integer, db.ForeignKey('prof.id'))
    nom = db.Column(db.String(50))
    numero_carte = db.Column(db.String(50))
    montant_retrait = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    statut = db.Column(db.String(50), default='attente')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    etudiant_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    prof_id = db.Column(db.Integer, db.ForeignKey('prof.id'))
    commentaire = db.Column(db.String(500))
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    commentateurs = db.relationship('User', backref='evnt', foreign_keys=[etudiant_id])

class Reclamation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vue=db.Column(db.String(50),default="non")
    traite=db.Column(db.String(50),default="non")
    contenu = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    util = db.relationship('User', backref='rec', foreign_keys=[user_id])


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text)
    date_envoi = db.Column(db.DateTime, default=datetime.utcnow)
    expediteur_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    expediteur = db.relationship('User', backref='messages_envoyes', foreign_keys=[expediteur_id])
    destinataire_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    destinataire = db.relationship('User', backref='messages_recus', foreign_keys=[destinataire_id])

