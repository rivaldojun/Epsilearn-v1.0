from User import db

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



class CommentEV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_ev=db.Column(db.Integer, db.ForeignKey('evenement.id_evenement'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    commentaire = db.Column(db.String(500))
    commentateur = db.relationship('User', backref='event', foreign_keys=[user_id])
