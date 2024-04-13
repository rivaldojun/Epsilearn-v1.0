from App import db

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

