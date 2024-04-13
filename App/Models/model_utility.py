from App import db

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




