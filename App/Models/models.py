from App import db,login_manager
from flask import session
from datetime import datetime,timedelta
from werkzeug.local import LocalProxy
from App.Decorators import *

# Table User

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
    etudiant= db.relationship('Etudiant', backref='acces_etudiant', foreign_keys='Etudiant.id_user_e')
    prof= db.relationship('Prof', backref='acces_prof', foreign_keys='Prof.id_user_p')
    autre= db.relationship('Autre', backref='acces_autre', foreign_keys='Autre.id_user_a')
    def is_student(self):
        return self.role=="Etudiant"
    def is_prof(self):
        return self.role=="Prof"
    def is_other(self):
        return self.role=="Autre"
    def is_not_active(self):
        self.active=False 
         
         
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(50))
    mdp=db.Column(db.String(50))
    superadmin=db.Column(db.String(50))

    
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_creator=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    subject = db.Column(db.String(200))  # Champ pour le sujet du room
    messages = db.relationship('MessageRoom', backref='room', lazy=True)
    users = db.relationship('ChatRoom', backref='room', lazy=True)
    creator = db.relationship('User', backref='created_rooms', foreign_keys=[id_creator])

class ChatRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=True)

class MessageRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.String(200))
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    pseudo=db.Column(db.String(200))
    utilisateur = db.relationship('User', backref=db.backref('messages', lazy=True))


# Table Etudiant
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


# Table Demande
class Demande(db.Model):
    id_demande = db.Column(db.Integer, primary_key=True)
    id_prof = db.Column(db.Integer, db.ForeignKey('prof.id'))
    id_live=db.Column(db.Integer, db.ForeignKey('live.id'))
    code=db.Column(db.String(500))
    prix=db.Column(db.Float)
    temps=db.Column(db.String(50))
    id_etudiant = db.Column(db.Integer, db.ForeignKey('etudiant.id'))
    date_demande = db.Column(db.DateTime)
    date_propose = db.Column(db.DateTime)
    confprof=db.Column(db.String(50),default="non")
    confetud=db.Column(db.String(50),default="non")
    ajout=db.Column(db.String(50),default="non")
    date_acc = db.Column(db.DateTime)
    date_fin = db.Column(db.DateTime)
    date1 = db.Column(db.DateTime)
    date2 = db.Column(db.DateTime)
    fichier = db.Column(db.String(50))
    discipline=db.Column(db.String(50))
    matiere = db.Column(db.String(50))
    chapiter = db.Column(db.String(50),default="Aucun chapitre mentionné")
    description = db.Column(db.Text)
    statut_demande = db.Column(db.String(50),default="enattente")
    statut_payement = db.Column(db.String(50),default="impayer")
    acceptation=db.Column(db.String(50),default="non")
    aj_e=db.Column(db.String(50),default="nouvelle")
    aj_p=db.Column(db.String(50),default="nouvelle")

class Evenement(db.Model):
    id_evenement = db.Column(db.Integer, primary_key=True)
    id_organisateur = db.Column(db.Integer, db.ForeignKey('user.id'))
    Nom = db.Column(db.String(50))
    date= db.Column(db.DateTime)
    type_ev=db.Column(db.String(50))
    nbplace = db.Column(db.Integer)
    nbplace_occupe = db.Column(db.Integer, default=0) 
    pays_ville=db.Column(db.String(50)) 
    live=db.Column(db.String(50))
    lien=db.Column(db.String(50))
    description=db.Column(db.String(500))
    vue = db.Column(db.Integer,default=0)
    cd=db.Column(db.String(500))
    photo=db.Column(db.String(500))
    statut=db.Column(db.String(50),default="Bientot")
    organizer = db.relationship('User', backref='events', foreign_keys=[id_organisateur])


class Participation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_evenement = db.Column(db.Integer, db.ForeignKey('evenement.id_evenement'))
    id_participant=db.Column(db.Integer, db.ForeignKey('user.id'))


class Retrait(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_demandeur=db.Column(db.Integer, db.ForeignKey('prof.id'))
    nom = db.Column(db.String(50))
    numero_carte = db.Column(db.String(50))
    montant_retrait = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    statut = db.Column(db.String(50), default='attente')


class AbonnementLangue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_abonne = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_groupe = db.Column(db.Integer, db.ForeignKey('groupelangue.id'))
    datedebut = db.Column(db.DateTime)
    nb=db.Column(db.Integer,default=1)
    datefin = db.Column(db.DateTime)
    duree = db.Column(db.Integer)
    point = db.Column(db.Integer)
    nom = db.Column(db.String(50))
    termine = db.Column(db.String(50))
    util= db.relationship('User', backref='langue', foreign_keys=[id_abonne])

class groupelangue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lien = db.Column(db.String(500))
    nom = db.Column(db.String(50))
    abonnements = db.relationship('AbonnementLangue', backref='groupe', lazy=True)

    def calculate_avg_point(self):
        total_points = sum(abonnement.point for abonnement in self.abonnements)
        if len(self.abonnements) > 0:
            return total_points / len(self.abonnements)
        return 0


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


class Live(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    id_moderateur = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_demande = db.Column(db.Integer, db.ForeignKey('demande.id_demande'))

class StartLive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_live = db.Column(db.Integer, db.ForeignKey('live.id'))
    date = db.Column(db.DateTime)
    id_participant = db.Column(db.Integer, db.ForeignKey('user.id'))
    code=db.Column(db.String(500))



class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text)
    date_envoi = db.Column(db.DateTime, default=datetime.utcnow)
    expediteur_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    expediteur = db.relationship('User', backref='messages_envoyes', foreign_keys=[expediteur_id])
    destinataire_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    destinataire = db.relationship('User', backref='messages_recus', foreign_keys=[destinataire_id])


# Table Offre
class Offre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_offre = db.Column(db.String(50))
    description = db.Column(db.String(500))
    id_prof = db.Column(db.Integer, db.ForeignKey('prof.id'), nullable=False)
    matiere = db.Column(db.String(50), nullable=False)
    organisation = db.Column(db.String(100), nullable=True)
    type=db.Column(db.String(50))
    duree=db.Column(db.String(50), nullable=True)
    Tel=db.Column(db.String(50), nullable=True)
    horaire = db.Column(db.String(500))
    horaire_presentiel = db.Column(db.String(500))
    meet = db.Column(db.String(500))
    emplacement = db.Column(db.String(500))
    date_debut = db.Column(db.DateTime)
    date_fin = db.Column(db.DateTime)
    nombre_place_total = db.Column(db.Integer)
    prix = db.Column(db.Float)
    nombre_place_occupe = db.Column(db.Integer, default=0)
    image_1 = db.Column(db.String(500))
    image_2 = db.Column(db.String(500))

# Table SubscriptionOffre (table de souscription aux offres)
class SubscriptionOffre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_offre = db.Column(db.Integer, db.ForeignKey('offre.id'), nullable=False)
    id_participant = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    offre = db.relationship('Offre', foreign_keys=[id_offre], backref=db.backref('subscriptions', lazy=True))


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

class np_nombre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    us =db.Column(db.Integer,nullable=False)
    # def __init__(self,us):
    #     self.id=1
    #     self.us=us

class nd_nombre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    us =db.Column(db.Integer,nullable=False)
    # def __init__(self,us):
    #     self.id=1
    #     self.us=us

class nstud_nombre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    us =db.Column(db.Integer,nullable=False)
    # def __init__(self,us):
    #     self.id=1
    #     self.us=us

class username_fp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    us =db.Column(db.String,nullable=False)
    # def __init__(self,us):
    #     self.id=1
    #     self.us=us

class nb_req(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nr =db.Column(db.Integer,nullable=False)
    # def __init__(self,nr):
    #     self.id=1
    #     self.nr=nr

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


