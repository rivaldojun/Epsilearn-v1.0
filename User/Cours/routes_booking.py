from flask import render_template,jsonify,redirect,url_for,request,session,flash,Blueprint
from datetime import datetime,timedelta
from werkzeug.utils import secure_filename
import os
from User.Models.models import *
from User.Controllers.fonction import *

CoursBp = Blueprint("Cours",__name__,template_folder="templates")
#COURS BOOKING PART
@CoursBp.route('/discipline')
@student_login_required_AI
def discipline():
    return render_template('discipline.html')

@CoursBp.route('/matiere/<discipline>',methods=["POST","GET"])
@student_login_required_AI
def matiere(discipline):
    if request.method=="POST":
        matiere=request.form["selected_discipline"]
        session['discipline']=discipline
        session['matiere']=matiere
        return redirect(url_for('Cours.chapitre'))
    return render_template('matiere.html',discipline=discipline)

@CoursBp.route('/chapitre',methods=["POST","GET"])
@student_login_required_AI
def chapitre():
    if request.method=="POST":
        chapitre=request.form["chapitre"]
        session['chapitre']=chapitre
        return redirect(url_for('Cours.date'))
    return render_template('chapitre.html')

@CoursBp.route('/epreuve',methods=['POST','GET'])
@student_login_required_AI
def epreuve():
    if request.method=="POST":
        file = request.files['file']
        if file:
            current_date = datetime.now()
            date_string = current_date.strftime("%Y%m%d%H%M%S")
            file_extension = file.filename.split('.')[-1]
            filename = f"{secure_filename(file.filename.replace('.', '_'))}_{date_string}.{file_extension}"
            path1=os.getenv("Path1")
            path2="epreuve"
            file.save(os.path.join(path1,path2, filename))  # Replace with your desired directory path
            fichier=os.path.join("static",path2, filename)
            session['fichier']=fichier
            return redirect(url_for("Cours.date"))
    return render_template('epreuve.html')

@CoursBp.route('/date',methods=['POST','GET'])
@student_login_required_AI
def date():
    if request.method=="POST":
        data = request.get_json()
        date1= data['dt1']
        date2= data['dt2']
        session['date1']=date1
        session['date2']=date2
        return redirect(url_for("Cours.heure"))
    return render_template('date.html')

@CoursBp.route('/choixprof')
@student_login_required_AI
def choixprof():
    return render_template('choixprof.html')

@CoursBp.route('/get_professeur', methods=['GET'])
def get_professeur():
    try:
        joined_data = db.session.query(User.id,User.nom, User.prenom,User.nationalite, Prof.discipline, Prof.formation, Prof.Nvdetud, Prof.Diplome, Prof.etoile,Prof.photo,Prof.valider,Prof.vendervous).\
            join(Prof, User.id == Prof.id_user_p).all()
        professeurs_list = []
        for data in joined_data:
            prof_dict = {
                'id':data.id,
                'nom': data.nom,
                'prenom': data.prenom,
                'discipline': data.discipline,
                'formation': data.formation,
                'niveau': data.Nvdetud,
                'diplome': data.Diplome,
                'note': data.etoile,
                'photo' :data.photo,
                'nationalite' :data.nationalite,
                'bio' :data.vendervous,
                'valider':data.valider
            }
            if prof_dict['valider']=="oui":
                professeurs_list.append(prof_dict)
        # Return the data as a JSON response
        return jsonify(professeurs_list)
    except Exception as e:
        # Handle the exception and return an error response
        return jsonify({'error': str(e)}), 500

@CoursBp.route('/heure',methods=["POST","GET"])
@student_login_required_AI
def heure():
    if request.method=="POST":
        prix=request.form['prix']
        temps=request.form['t']
        session['prix']=prix
        session['temps']=temps
        return redirect(url_for('Cours.choixprof'))
    return render_template('heure.html')


@CoursBp.route('/creationdemande/<idprof>')
@student_login_required_AI
def creationdemande(idprof):
    if idprof!="0":
        userprof = User.query.get(idprof)
        nps=userprof.nom +" "+ userprof.prenom
        body = render_template("Mail_demande.html",user=user)
        sender_email = os.getenv("OUR_MAIL")
        send_email(sender_email, userprof.mail,"Reception de demande", body)
    else:
        nps=""
    date_demande = datetime.now()
    date1 = datetime.fromisoformat(session.get("date1")) if session.get("date1") else None
    date2 =datetime.fromisoformat(session.get("date2")) if session.get("date2") else None
    demande = Demande(
        id_prof=idprof,
        id_etudiant=session.get('userid'), 
        date_demande=date_demande,
        discipline=session.get('discipline'), 
        date1=date1,
        date2=date2,
        matiere=session.get("matiere"),
        chapiter=session.get("chapitre"),
        description=session.get("chapitre"),
        fichier=session.get('fichier'),
        prix=session.get("prix"),
        temps=session.get("temps")
    )
    db.session.add(demande)
    db.session.commit()
    return render_template('creationdemande.html',demande=demande,nom=nps)
#END COURS BOOKING PART