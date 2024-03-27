from User import db
from datetime import datetime
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    prenom = db.Column(db.String(50))
    nationalite = db.Column(db.String(50))
    mail = db.Column(db.String(50))
    code = db.Column(db.String(50))
    pseudo=db.Column(db.String(200))
    date_naiss=db.Column(db.DateTime)
    ter = db.Column(db.String(50),default="non")
    age=db.Column(db.Integer)
    confirmer = db.Column(db.String(50),default="non")
    mdp=db.Column(db.String(50))
    photo=db.Column(db.String(50),default="static/Profil/unknown.jpg")
    password_reset_token = db.Column(db.String(100))
    password_reset_expiration = db.Column(db.DateTime)
    role=db.Column(db.String(200))
    def is_student(self):
        return self.role=="Etudiant"
    def is_prof(self):
        return self.role=="Prof"
    def is_other(self):
        return self.role=="Autre"
    def is_not_active(self):
        self.active=False
         
         
         
class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user_e = db.Column(db.Integer, db.ForeignKey('user.id'))
    Nvdetud=db.Column(db.String(50))
    formation=db.Column(db.String(50))
    age=db.Column(db.Integer)
    filiere=db.Column(db.String(50))
    ecole=db.Column(db.String(50))
    photo=db.Column(db.String(50),default="static/Profil/unknown.jpg")

class Autre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user_a = db.Column(db.Integer, db.ForeignKey('user.id'))
    age=db.Column(db.Integer)
    photo=db.Column(db.String(50),default="static/Profil/unknown.jpg")
    vendervous=db.Column(db.String(500))


# Table Prof
class Prof(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user_p = db.Column(db.Integer, db.ForeignKey('user.id'))
    formation=db.Column(db.String(50))
    Nvdetud=db.Column(db.String(50))
    filiere=db.Column(db.String(50))
    age=db.Column(db.Integer)
    Diplome=db.Column(db.String(50))
    discipline=db.Column(db.String(500))
    valider=db.Column(db.String(50),default="non")
    positif = db.Column(db.Integer,default=1)
    nefatif = db.Column(db.Integer,default=1)
    solde = db.Column(db.Float, default=0.0)
    ecole=db.Column(db.String(50))
    photo=db.Column(db.String(50),default="static/Profil/unknown.jpg")
    etoile=db.Column(db.Integer,default=1)
    vendervous=db.Column(db.String(500))
    cv=db.Column(db.String(500))


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


class CommentEV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_ev=db.Column(db.Integer, db.ForeignKey('evenement.id_evenement'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    commentaire = db.Column(db.String(500))
    commentateur = db.relationship('User', backref='event', foreign_keys=[user_id])

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
