from App import db

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
