import json
from flask import render_template,jsonify,redirect,url_for,request,session,Blueprint
from datetime import datetime
import os
from flask_socketio import SocketIO, emit,join_room
from App.Models.models import *
from App.Controllers.fonction import *
from App import socketio
from flask_socketio import SocketIO, emit


# Utilisez la méthode on pour définir des gestionnaires d'événements
@socketio.on('like')
def handle_like_event(data):
    pass


PomodoroBp = Blueprint("Pomodoro",__name__,template_folder="templates")

#POMODORO PART
@PomodoroBp.route('/pomodoro')
@student_prof_login_required
def pomodoro():
    try:
        user_id = session.get('userid')
        pomodoro = Pomodoro.query.filter_by(id_utilisateur=user_id).first()
        nbrinvit=Groupmember.query.filter_by(id_member=user_id,statut='attente').count()
        nbrsalle=Groupstud.query.filter_by(id_createur=user_id).count()
        if not pomodoro :
            pomodoro=Pomodoro(id_utilisateur=user_id)
            db.session.add(pomodoro)
            db.session.commit()
        classement_users = db.session.query(
            Pomodoro.id_utilisateur,
            User.photo,
            User.nom,
            User.prenom,
            User.mail,
            Pomodoro.time
        ).group_by(Pomodoro.id_utilisateur).order_by(db.desc('time')).all()
        user_id_, photo,nom,prenom,mail,total_time = classement_users[0]
        user_ = User.query.get(user_id_)
        username=user_.nom+" "+user_.prenom
        tps=Best_time_25.query.filter_by().first()
        nb=Memorix.query.filter_by().first()
        if not tps:
            temps_25=0
        else:
            temps_25=tps.temps
        if not nb:
            nombre=0
        else:
            nombre=nb.nombre
    except Exception as e:
        print(e)
        return render_template('error.html')
    return render_template('pomodoro.html',pomodoro=pomodoro,nbrinvit=nbrinvit,nbrsalle=nbrsalle,username=username,temps_25=temps_25,nombre=nombre)


@PomodoroBp.route('/chambrepomodoro')
def chambrepomodoro():
    return render_template('chambrepomodoro.html')

@PomodoroBp.route('/groupestudform')
def groupestudform():
    return render_template('groupstudsheet.html')


@PomodoroBp.route('/groupestudformsave',methods=['GET','POST'])
def groupestudformsave():
    user_id = session.get('userid')
    if request.method=="POST":
        titre=request.form['titre']
        debut=request.form['debut']
        fin=request.form['fin']
        try:
            group=Groupstud(id_createur=user_id,titre=titre,time_debut=debut,time_fin=fin)
            db.session.add(group)
            db.session.commit()
            membre=Groupmember(id_groupe=group.id,id_member=user_id,statut='accepte')
            db.session.add(membre)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            render_template('error.html')
    return redirect(url_for('Pomodoro.addtasks',id_group=group.id))

@socketio.on('join')
def join_room(data):
    room = data['room']
    join_room(room)

@socketio.on('offer')
def handle_offer(data):
    emit('offer', data, room=data['room'])

@socketio.on('answer')
def handle_answer(data):
    emit('answer', data, room=data['room'])

@socketio.on('ice-candidate')
def handle_ice_candidate(data):
    emit('ice-candidate', data, room=data['room'])

@PomodoroBp.route('/suppgroupstud/<int:id_group>', methods=['GET', 'POST'])
def supprimer_groupstud(id_group):
    groupstud = Groupstud.query.get(id_group)
    if groupstud:
        try:
            Grouptasks.query.filter_by(id_groupe=id_group).delete()
            Groupmessage.query.filter_by(id_groupe=id_group).delete()
            Groupmember.query.filter_by(id_groupe=id_group).delete()
            db.session.delete(groupstud)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            render_template('error.html')
        return redirect(url_for('Pomodoro.sallelist'))


@PomodoroBp.route('/ajoutermembre/<int:id_group>/<int:userid>')
def ajoutermembre(id_group,userid):
    try:
        membre=Groupmember(id_groupe=id_group,id_member=userid)
        db.session.add(membre)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        render_template('error.html')
    return redirect(url_for('Pomodoro.groupestud',id_group=id_group))


@PomodoroBp.route('/statut_change/<int:id>')
def statut_change(id):
    membre=Groupmember.query.filter_by(id=id).first()
    try:
        membre.statut='accepte'
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        render_template('error.html')
    return redirect(url_for('Pomodoro.groupestud',id_group=membre.groupe.id))

@PomodoroBp.route('/refuser_etud/<int:id>')
def refuser_etud(id):
    membre=Groupmember.query.filter_by(id=id).first()
    try:
        db.session.delete(membre)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        render_template('error.html')
    return redirect(url_for('Pomodoro.groupelist'))

@PomodoroBp.route('/groupelist')
def groupelist():
    user_id = session.get('userid')
    try:
        grp=Groupmember.query.filter_by(id_member=user_id).all()
    except Exception as e:
        db.session.rollback()
        render_template('error.html')
    return render_template('grouplist.html',grp=grp)

@PomodoroBp.route('/sallelist')
def sallelist():
    user_id = session.get('userid')
    try:
        grp=Groupstud.query.filter_by(id_createur=user_id).all()
    except Exception as e:
        db.session.rollback()
        render_template('error.html')
    return render_template('groupcree.html',grp=grp)

@PomodoroBp.route('/addtasks/<int:id_group>')
def addtasks(id_group):
    grp=Groupstud.query.filter_by(id=id_group).first()
    heuredeb=grp.time_debut
    heurefin=grp.time_fin
    return render_template('addtasks.html',id_group=id_group,heuredeb=heuredeb,heurefin=heurefin)

@PomodoroBp.route('/addtasksave/<int:id_group>', methods=['POST'])
def addtasksave(id_group):
    try:
        taches_json = request.form['taches']  # Récupérez les tâches au format JSON depuis le formulaire
        taches = json.loads(taches_json) if taches_json else []
        for t in taches:
            task = Grouptasks(id_groupe=id_group, tache=t)
            db.session.add(task)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        render_template('error.html')
    return redirect(url_for('Pomodoro.groupestud', id_group=id_group))



@PomodoroBp.route('/groupstud/<id_group>')
def groupestud(id_group):
    try:
        user_id = session.get('userid')
        grant=Groupmember.query.filter_by(id_member=user_id).first()
        createur=Groupstud.query.filter_by(id_createur=user_id).first()  
        grp=Groupstud.query.filter_by(id=id_group).first()
        tasks=Grouptasks.query.filter_by(id_groupe=id_group).all()
        message=Groupmessage.query.filter_by(id_groupe=id_group).order_by(Groupmessage.date_env).all()
        # Transformez les tâches en une liste Python
        task_list = [task.tache for task in tasks]
        us =User.query.all()
        membre=Groupmember.query.filter_by(id_groupe=id_group).all()
        if grant or createur:
            return render_template('groupstud.html',task=task_list,id_group=id_group,message=message,us=us,membre=membre,grp=grp)
        else:
            return render_template('acces-interdit.html',task=task_list,id_group=id_group,message=message,us=us,membre=membre,grp=grp)
    except Exception as e:
        render_template('error.html')

@PomodoroBp.route('/effacer_etudiant/<int:id>')
def effacer_etudiant(id):
    try:
        membre=Groupmember.query.filter_by(id=id).first()
        id_group=membre.groupe.id 
        db.session.delete(membre)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        render_template('error.html')
    return redirect(url_for('Pomodoro.groupestud',id_group=id_group))

@socketio.on('message')
def handle_message(data):
    try:
        id_msg=None
        user_id = session.get('userid')
        content = data['content']
        user_name=user.nom +" "+user.prenom
        id_group=data['group']
        if data['call']=='yes':
            call=data['call']
            audio_data = data['mp3']  # Les données audio reçues depuis le client
            if audio_data:
                    if not os.path.exists('App/static/audio'):
                        os.makedirs('App/static/audio')
                    current_datetime = datetime.now()
                    date_string = current_datetime.strftime("%Y%m%d_%H%M%S")
                    # Enregistrez le fichier audio au format MP3
                    with open(f'App/static/audio/audio_{user_id}_{id_group}_{date_string}.mp3', 'wb') as audio_file:
                        audio_file.write(audio_data)

                    path=f'/static/audio/audio_{user_id}_{id_group}_{date_string}.mp3'
                    new_audio_message = Groupmessage(id_groupe=id_group, message="Message audio vocal", audio_data=audio_data, id_user=user_id,audio_data_path=path)
                    db.session.add(new_audio_message)
                    db.session.commit()
                    id_msg=new_audio_message.id
                    path=new_audio_message.audio_data_path
        else:
            call='no'
            message = Groupmessage(message=content,id_groupe=id_group,id_user=user_id)
            db.session.add(message)
            db.session.commit()
            id_msg=message.id
            path=" "
        emit('message',{'content': content, 'user': request.sid, 'group':id_group, 'username':user_name,'call':call,'msgid':id_msg,'audio_data_path':path}, broadcast=True)
    except Exception as e:
        db.session.rollback()
        render_template('error.html')
# La route pour servir des fichiers audio
@PomodoroBp.route('/get-audio/<audio_id>')
def get_audio(audio_id):
    try:
        audio_record = Groupmessage.query.filter_by(id=audio_id).first()  # Assurez-vous d'adapter cette partie à votre modèle
        if not audio_record:
            return jsonify({"error": "Audio not found"}), 404
        # 2. Convertissez les données audio en un objet BytesIO
        audio_data = audio_record.audio_data_path
        # 3. Utilisez Flask pour envoyer l'objet BytesIO au client
        return  jsonify({"mp3_path": audio_data})
    except Exception as e:
        db.session.rollback()
        render_template('error.html')

@PomodoroBp.route('/update_pomodoro', methods=['POST'])
def update_pomodoro():
    user_id = session.get('userid')
    pomodoro = Pomodoro.query.filter_by(id_utilisateur=user_id).first()  # Supposons que vous avez une seule entrée dans la table Pomodoro
    if pomodoro:
        pomodoro.time += 25  # Ajoutez 25 secondes à la colonne "time"
        db.session.commit()  # Enregistrez la mise à jour dans la base de données
        return jsonify({'message': 'Mise à jour réussie'})
    else:
        return jsonify({'message': 'Aucun enregistrement Pomodoro trouvé'})

@PomodoroBp.route('/classementpomodoro')
def classement():
    try:
        userid = session.get('userid')
        # Obtenez la liste des utilisateurs triés par nombre de points
        classement_users = db.session.query(
            Pomodoro.id_utilisateur,
            User.photo,
            User.mail,
            Pomodoro.time
        ).group_by(Pomodoro.id_utilisateur).order_by(db.desc('time')).all()

        # Créez une liste d'objets contenant le nom, prénom et le temps effectué
        classement_data = []
        for index, (user_id, photo,mail,total_time) in enumerate(classement_users, start=1):
            user = User.query.get(user_id)
            classement_data.append({
                'index':index,
                'id':user_id,
                'nom': user.nom,
                'prenom': user.prenom,
                'mail':mail,
                'temps_effectue': total_time,
                'phot':photo
            })
        # Rendez le modèle HTML avec les données
    except Exception as e:
        render_template('error.html')
    return render_template('classementpomodoro.html', classement_data=classement_data,userid=userid)


@PomodoroBp.route('/score_25alasuite', methods=['POST'])
def save_score():
    try:
        tps=Best_time_25.query.filter_by().first()
        userid = session.get('userid')
        if request.is_json:
            data = request.get_json()
            if 'time' in data:
                time = data['time']
                if tps:
                    if tps.temps>time:
                        tps.temps=time
                        tps.id_us=userid
                        db.session.commit()
                else:
                    t=Best_time_25(temps=time,id_us=userid)
                    db.session.add(t)
                    db.session.commit()
    except Exception as e:
        db.session.rollback()
        render_template('error.html')
    return jsonify({'message': 'Score enregistré avec succès'})

@PomodoroBp.route('/score_memorix', methods=['POST'])
def save_memorix():
    try:
        tps=Memorix.query.filter_by().first()
        userid = session.get('userid')
        if request.is_json:
            data = request.get_json()
            if 'nombre' in data:
                nombre = data['nombre']
                if tps:
                    if tps.nombre<nombre:
                        tps.nombre=nombre
                        tps.id_us=userid
                        db.session.commit()
                else:
                    t=Memorix(nombre=nombre,id_us=userid)
                    db.session.add(t)
                    db.session.commit()
    except Exception as e:
        db.session.rollback()
        render_template('error.html')
    return jsonify({'message': 'Score enregistré avec succès'})
#END POMODORO PART