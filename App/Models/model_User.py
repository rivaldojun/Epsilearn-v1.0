from App import db,login_manager

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
    etudiant= db.relationship('Etudiant', backref='acces_etudiant', foreign_keys=[id])
    prof= db.relationship('Prof', backref='acces_prof', foreign_keys=[id])
    autre= db.relationship('Autre', backref='acces_autre', foreign_keys=[id])
    def is_student(self):
        return self.role=="Etudiant"
    def is_prof(self):
        return self.role=="Prof"
    def is_other(self):
        return self.role=="Autre"
    def is_not_active(self):
        self.active=False 

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

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)