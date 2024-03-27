from flask import render_template,jsonify,redirect,url_for,request,session,Blueprint
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from User.Controllers.fonction import *
from User.Models.models import *
from flask import render_template,jsonify,redirect,url_for,request,session,send_file,Blueprint,after_this_request
from datetime import datetime,timedelta
from werkzeug.utils import secure_filename
import os
import zipfile
from User.Models.models import *
import io
from User import socketio
from User.Controllers.fonction import *
import stripe
EventBp = Blueprint("Event",__name__,template_folder="templates")

#EVENT PART
@EventBp.route('/get_event', methods=['GET'])
def get_event():
    try:
        userid=session.get('userid')
        # Perform a join between the User and Prof tables to retrieve the data
        joined_data = db.session.query(Evenement.id_evenement,Evenement.id_organisateur,Evenement.Nom, Evenement.date, Evenement.type_ev, Evenement.nbplace, Evenement.nbplace_occupe, Evenement.lien, Evenement.live, Evenement.vue, Evenement.description, Evenement.photo, Evenement.statut,User.nom,User.prenom,User.id).\
            join(User, User.id == Evenement.id_organisateur).all()
        # Convert the data to a list of dictionaries
        evenements_participes = [p.id_evenement for p in Participation.query.filter_by(id_participant=userid).all()]
        professeurs_list = []
        for data in joined_data:
            prof_dict = {
                'id':data.id_evenement,
                'userid':data.id,
                'organisateurid':data.id_organisateur,
                'nomevent': data.Nom,
                'nom': data.nom,
                'prenom': data.prenom,
                'date': data.date,
                'type': data.type_ev,
                'nbplace': data.nbplace,
                'nbplace_occupe': data.nbplace_occupe,
                'live': data.live,
                'lien': data.lien,
                'description' :data.description,
                'photo' :data.photo,
                'statut' :data.statut,
                'vue' :data.vue,
                'ig' :session.get('userid')
            }
            if prof_dict["id"] not in evenements_participes and prof_dict["nbplace_occupe"]!=prof_dict["nbplace"]:
               professeurs_list.append(prof_dict)
        # Return the data as a JSON response
        return jsonify(professeurs_list)
    except Exception as e:
        # Handle the exception and return an error response
        return jsonify({'error': str(e)}), 500



@EventBp.route('/evenement')
def evenement():
    supprimer_evenements_expirees()
    user_id = session.get('userid')  # Récupère l'ID de l'utilisateur à partir de la session
     # Récupère l'utilisateur de la table User
    nombre_de_participations = db.session.query(func.count(Participation.id)).filter_by(id_participant=user_id).scalar()
    
    
    
    return render_template('evenement.html',ne=nombre_de_participations)

@EventBp.route('/plusevenement/<typer>')
def plusevenement(typer):
    supprimer_evenements_expirees()
    user_id = session.get('userid')  # Récupère l'ID de l'utilisateur à partir de la session
     # Récupère l'utilisateur de la table User
    nombre_de_participations = db.session.query(func.count(Participation.id)).filter_by(id_participant=user_id).scalar()
    
    
    

    return render_template('plusevenement.html',ne=nombre_de_participations,typer=typer)

@EventBp.route('/confirmationevent')
def confirmationevent():
    user_id = session.get('userid')
    
    
    
    
    return render_template('confirmationevent.html')


@EventBp.route('/ajouterevenement',methods=["POST","GET"])
@login_required
def ajouterevenement():
    user_id = session.get('userid')
    
    
    user_id = session.get('userid')
    mails = [user.mail for user in User.query.all()]
    if request.method=="POST":
        nom=request.form['nom']
        participant_emails = request.form.getlist('participantEmails[]')
        # Concaténez les valeurs avec des points-virgules
        emails_concatenated = ';'.join(participant_emails)
        typ=request.form['type']
        description=request.form['description']
        date=request.form['date']
        live=request.form['live']
        nbplace=request.form['nbplace']
        pays_ville=request.form['paysville']
        photo=request.files['photo']
        lien=request.form['lien']
        if photo:
            current_date = datetime.now()
            # Formatez la date actuelle en tant que chaîne pour l'utiliser dans le nom de fichier
            date_string = current_date.strftime("%Y%m%d%H%M%S")
            # Obtenez l'extension du fichier téléchargé
            file_extension = photo.filename.split('.')[-1]
            # Créez un nom de fichier unique en ajoutant la date actuelle au nom d'origine
            filename = f"{secure_filename(photo.filename.replace('.', '_'))}_{date_string}.{file_extension}"
            path1="User/static"
            path2="evenement"
            photo.save(os.path.join(path1,path2, filename))
            photo = os.path.join("static",path2, filename)
        else:
            photo=""
        date = datetime.fromisoformat(date)
        if live=="Oui":
            ev=Evenement(id_organisateur=int(user_id),Nom=nom,type_ev=typ,description=description,date=date,live=live,nbplace=nbplace,photo=photo,pays_ville=pays_ville,lien=lien,cd=uuidv4())
        else:
            ev=Evenement(id_organisateur=int(user_id),Nom=nom,type_ev=typ,description=description,date=date,live=live,nbplace=nbplace,photo=photo,pays_ville=pays_ville,lien=lien)

        db.session.add(ev)
        db.session.commit()
        ajouter_participants_par_email(emails_concatenated, event_id=ev.id_evenement)
        return redirect(url_for('Event.evenement'))
    
    
    
    return render_template('ajouterevenement.html',mails=mails)


@EventBp.route('/get_user_emails', methods=['GET'])
def get_user_emails():
    user_emails = [user.mail for user in User.query.all()]  # Supposons que votre modèle User a un champ "email"

    user_emails=["vfvsfjsf@hbj.com","sbsfsbhf@vgh.com","sbsfsbhf@vgh.com"]
    return jsonify(user_emails)


@EventBp.route('/effacer_evenement/<int:id_ev>')
@login_required
def effacer_evenement(id_ev):
    
    user = User.query.get(int(session.get("userid")))    
    evenement = Evenement.query.get(id_ev)
    # Vérifier si l'utilisateur est réellement inscrit à l'événement
    part = Participation.query.filter_by(id_evenement=id_ev, id_participant=user.id).first()
    if part:
        # Mettre à jour le nombre de places occupées et supprimer l'enregistrement de participation
        evenement.nbplace_occupe -= 1
        db.session.delete(part)
        db.session.commit()
    return redirect(url_for('Event.mesevenements'))


@EventBp.route('/details_evenements/<int:idev>',methods=["POST","GET"])
@login_required
def details_evenements(idev) :
    
    user_id = session.get('userid')  # Récupère l'ID de l'utilisateur à partir de la session
     # Récupère l'utilisateur de la table User
    evenement= Evenement.query.filter_by(id_evenement=idev).first()
    com = CommentEV.query.filter_by(id_ev=idev).all()
    prof = Prof.query.filter_by(id_user_p=user.id).first()
    evenement.vue=int(evenement.vue)+1
    db.session.add(evenement)
    db.session.commit()
    if request.method=="POST":
        commentaire = request.form.get('commentaire')
        if commentaire is not None or commentaire!='N? KBKGG':
            comment = CommentEV(user_id=user_id, id_ev=idev, commentaire=commentaire)
            db.session.add(comment)
            db.session.commit()
        # Renvoyer une réponse JSON indiquant le succès de la mise à jour
        response = jsonify(success=True)
        # Récupérer l'URL de la page actuelle et la renvoyer comme réponse JSON
        referrer_url = request.referrer
        response.headers['Location'] = referrer_url
        # Renvoyer une réponse avec un code de redirection (302) pour recharger la page
        return response, 302
    
    
    
    return render_template('detailsevenements.html',evenement=evenement,user=user.id,commentaires=com,prof=prof,photo=evenement.photo)

@EventBp.route('/reserver/<int:id_ev>')
@login_required
def reserver(id_ev):
    
    user = User.query.get(int(session.get("userid")))    
    evenement = Evenement.query.get(id_ev)
    # Vérifier s'il y a des places disponibles pour l'événement
    if evenement.nbplace_occupe < evenement.nbplace:
        # Mettre à jour le nombre de places occupées
        evenement.nbplace_occupe += 1
        db.session.add(evenement)
        # Créer un nouveau enregistrement de participation pour l'utilisateur et l'événement
        part = Participation(id_evenement=id_ev, id_participant=user.id)
        db.session.add(part)
        db.session.commit()
    else:
        # Gérer le cas où il n'y a plus de places disponibles
        return "Désolé, cet événement est complet."
    return redirect(url_for('Event.confirmationevent'))

@EventBp.route('/supprimerevent/<int:id_ev>')
@login_required
def supprimer(id_ev):
        
    
    evenement = Evenement.query.get(id_ev)
    db.session.delete(evenement)
    db.session.commit()
    return redirect(url_for('Event.evenement'))


@EventBp.route('/mesevenements')
@login_required
def mesevenements() :
    
    
    user_id = session.get('userid')  # Récupère l'ID de l'utilisateur à partir de la session
     # Récupère l'utilisateur de la table User
    evenements_participes = [p.id_evenement for p in Participation.query.filter_by(id_participant=user_id).all()]
    evenements_participes = Evenement.query.filter(Evenement.id_evenement.in_(evenements_participes)).all()
    # Récupérer tous les événements auxquels l'utilisateur ne participe pas
    
    
    
    return render_template('mesevenements.html',evenements=evenements_participes)
#END EVENT PART