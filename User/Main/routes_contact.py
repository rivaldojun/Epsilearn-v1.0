from flask import render_template,jsonify,redirect,url_for,request,session,flash
from datetime import datetime,timedelta
from User.Models.models import *
from User import socketio
from User.Controllers.fonction import *
from User.Main.routes_about import MainBp
#CONTACT BETWEEN USERS PART
@MainBp.route('/users')
@student_prof_login_required
def users():
    
    user_id = session.get('userid')
    if session.get('role')=="etudiant":
        users= User.query.join(Prof).filter(User.id != user_id).all()
    if session.get('role')=="professeur":
        users= User.query.join(Etudiant).filter(User.id != user_id).all() 
    # Obtenir la liste des utilisateurs avec lesquels user_id a eu des interactions
    interactions = (
        db.session.query(User)
        .join(Message, (Message.expediteur_id == User.id) | (Message.destinataire_id == User.id))
        .filter((Message.expediteur_id == user_id) | (Message.destinataire_id == user_id))
        .distinct()
    )
    # Obtenir les derniers messages pour chaque utilisateur
    dernier_messages = {}
    for autre_utilisateur in interactions:
        dernier_message = (
            Message.query.filter(
                ((Message.expediteur_id == user_id) & (Message.destinataire_id == autre_utilisateur.id)) |
                ((Message.expediteur_id == autre_utilisateur.id) & (Message.destinataire_id == user_id))
            )
            .order_by(Message.date_envoi.desc())
            .first()
        )
        dernier_messages[autre_utilisateur] = dernier_message
    return render_template('users.html', users=users,user=user,dernier_messages=dernier_messages)

@MainBp.route('/conversation/<int:user_id>', methods=['GET', 'POST'])
@student_prof_login_required
def conversation(user_id):
    
    user_dest=User.query.filter_by(id=user_id).first()
    user=User.query.get(session.get("userid"))
    if current_user is None:
        return "Utilisateur introuvable", 404
    if request.method == 'POST':
        content = request.form.get('new_message')
        if content:
            new_message = Message(contenu=content, date_envoi=datetime.utcnow(), expediteur=user, destinataire=user_dest)
            db.session.add(new_message)
            db.session.commit()
            # Émettre le nouveau message via WebSocket à tous les clients connectés
            socketio.emit('new_message', {'content': content, 'sender_name': user.nom, 'recipient_name': user_dest.nom})
        return redirect(url_for("Main.conversation", user_id=user_id))
    try:
        messages = Message.query.filter(((Message.expediteur == user) & (Message.destinataire == user_dest)) | ((Message.expediteur == user_dest) & (
                        Message.destinataire == user))).order_by(Message.date_envoi).all()
    except:
        messages=[]
    return render_template('conversation.html', user=user_dest, messages=messages, user_e=user)
#END CONTACT BETWEEN USERS PART