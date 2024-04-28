from flask import render_template,jsonify,redirect,url_for,request,session,flash
from datetime import datetime,timedelta
from sqlalchemy import and_,or_
from App.Models.models import *
from App.Controllers.fonction import *
import os
from werkzeug.utils import secure_filename
from App.Cours.routes_booking import *

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#COURS MANAGEMENT PART
@CoursBp.route('/demande')
@login_required
def demande():
    user_id = session.get('userid')
    if session.get("role")=="etudiant":
        update_aj_column_e()
    if session.get("role")=="professeur":
        update_aj_column_p()
    delete_expired_demandes()
    try:
        demandeprof =Demande.query.filter(and_(Demande.statut_demande == 'enattente', Demande.id_prof == user_id)).all()
        demandeprof = sorted(demandeprof, key=lambda demande: demande.id_demande, reverse=True)
        demandeetudiant = Demande.query.filter(and_(or_(Demande.statut_demande == 'enattente',Demande.statut_demande == 'refuse'), Demande.id_etudiant == user_id,Demande.acceptation=="non")).all()
        demandeetudiant = sorted(demandeetudiant, key=lambda demande: demande.id_demande, reverse=True)
        date_act = datetime.now()
    except Exception as e:
        return render_template('error.html')
    return render_template('demande.html',demandeprof=demandeprof,demandeetudiant=demandeetudiant,date_act=date_act)

@CoursBp.route('/details_dmd/<int:demande_id>', methods=['POST',"GET"])
@login_required
def detaildmd(demande_id):
    try:
        demand = Demande.query.filter_by(id_demande=demande_id).first()
        etudiant=Etudiant.query.filter_by(id_user_e=demand.id_etudiant).first()
        etudiant=User.query.filter_by(id=etudiant.id_user_e).first()
    except Exception as e:
        return render_template('error.html')
    return render_template('detailsdemande.html',demand=demand,etudiant=etudiant)

@CoursBp.route('/programme')
@login_required
def programme():
    user_id = session.get('userid')
    if session.get("role")=="etudiant":
        update_aj_column_e_a()
    if session.get("role")=="professeur":
        update_aj_column_p_a()
    date_act = datetime.now()
    date_act1=date_act + timedelta(hours=2)
    date_act1= date_act1
    date_act2=date_act - timedelta(hours=2)
    date_act2= date_act2
    update_status()
    delete_unpaid_demandes()
    try:
        programmeprof =  Demande.query.filter(and_(or_(Demande.statut_demande == 'accepte',Demande.statut_demande == 'report_demande',Demande.statut_demande == "report_accepte",Demande.statut_demande == "refuse"), Demande.id_prof == user_id),Demande.acceptation=="oui").all()
        programmeetudiant = Demande.query.filter(and_(or_(Demande.statut_demande == 'accepte',Demande.statut_demande == 'report_demande',Demande.statut_demande == "report_accepte",Demande.statut_demande == "refuse"), Demande.id_etudiant == user_id,Demande.acceptation=="oui")).all()
        programmeprof = sorted(programmeprof, key=lambda demande: demande.id_demande, reverse=True)
        programmeetudiant = sorted(programmeetudiant, key=lambda demande: demande.id_demande, reverse=True) 
    except Exception as e:
        return render_template('error.html')
    return render_template('programme.html',programmeprof=programmeprof,programmeetudiant=programmeetudiant,date_act1=date_act1,date_act2=date_act2,user=user,date_act=date_act)

@CoursBp.route('/offre', methods=["POST", "GET"])
@prof_login_required
def offre():
    try:
        demandes = Demande.query.filter(and_(Demande.statut_demande == 'enattente', Demande.id_prof =="0")).all()
    except Exception as e:
        return render_template('error.html')
    return render_template('offre.html', demands=demandes)


@CoursBp.route('/accepte_demande/date1/<int:demande_id>/<cd>', methods=['DELETE'])
@prof_login_required
def accepte_demande1(demande_id,cd):
    if request.method == 'DELETE':
        demande = Demande.query.filter_by(id_demande=demande_id).first()
        id_etud=demande.id_etudiant
        print(id_etud)
        etudiant=User.query.filter_by(id=id_etud).first()
        if demande:
            try:
                demande.statut_demande="accepte"
                live=Live(date=demande.date1,id_moderateur=session.get("userid"),id_demande=demande_id)
                db.session.add(live)
                db.session.commit()
                demande.acceptation="oui"
                demande.aj_e="modif"
                demande.aj_p="modif"
                demande.date_acc=demande.date1
                duree_demande = datetime.strptime(demande.temps, '%H:%M')
                delta = timedelta(hours=duree_demande.hour, minutes=duree_demande.minute)
                # Calculer la date de fin en ajoutant la durée à la date d'acceptation
                demande.date_fin = demande.date_acc + delta
                demande.id_prof=session.get("userid")
                demande.id_live=live.id
                demande.code=cd
                db.session.commit()
                start1=StartLive(date=demande.date1,id_live=live.id,id_participant=demande.id_prof,code=cd)
                start2=StartLive(date=demande.date1,id_live=live.id,id_participant=demande.id_etudiant,code=cd)
                db.session.add(start1)
                db.session.add(start2)
                db.session.commit()
                body = render_template("Mail_acceptation_demande.html",demande=demande)
                sender_email = os.getenv("OUR_MAIL")
                send_email(sender_email, etudiant.mail,"Acceptation de demande", body)
                return redirect(url_for('offre'))
            except Exception as e:
                print(e)
                db.session.rollback()
                return jsonify(success=False, message=str(e))
        else:
            return jsonify(success=False, message='Demande not found')
    
@CoursBp.route('/accepte_demande/date2/<int:demande_id>/<cd>', methods=['DELETE'])
@prof_login_required
def accepte_demande2(demande_id,cd):
    if request.method == 'DELETE':
        demande = Demande.query.filter_by(id_demande=demande_id).first()
        id_etud=demande.id_etudiant
        etud=Etudiant.query.filter_by(id=id_etud).first()
        etudiant=User.query.filter_by(id=etud.id_user_e).first()
        if demande:
            try:
                demande.statut_demande="accepte"
                demande.acceptation="oui"
                live=Live(date=demande.date2,id_moderateur=session.get("userid"),id_demande=demande_id)
                db.session.add(live)
                db.session.commit()
                demande.aj_e="modif"
                demande.aj_p="modif"
                demande.date_acc=demande.date2
                duree_demande = datetime.strptime(demande.temps, '%H:%M')
                delta = timedelta(hours=duree_demande.hour, minutes=duree_demande.minute)
                # Calculer la date de fin en ajoutant la durée à la date d'acceptation
                demande.date_fin = demande.date_acc + delta
                demande.id_prof=session.get("userid")
                demande.id_live=live.id
                demande.code=cd
                start1=StartLive(date=demande.date2,id_live=live.id,id_participant=demande.id_prof,code=cd)
                start2=StartLive(date=demande.date2,id_live=live.id,id_participant=demande.id_etudiant,code=cd)
                db.session.add(start1)
                db.session.add(start2)
                db.session.commit()
                body=render_template("Mail_acceptation_demande.html",demande=demande)
                sender_email = os.getenv("OUR_MAIL")
                send_email(sender_email, etudiant.mail,"Acceptation de demande", body)
                return jsonify(success=True)
            except Exception as e:
                db.session.rollback()
                return jsonify(success=False, message=str(e))
        else:
            return jsonify(success=False, message='Demande not found')


@CoursBp.route('/confprof/<int:demande_id>')
@prof_login_required
def confprof(demande_id):
    demande=Demande.query.filter_by(id_demande=demande_id)
    if demande:
        demande.confprof='oui'
        db.session.commit()
        return redirect(url_for('Main.accueil'))
    else:
        return jsonify(success=False, message='Demande not found')
    
@CoursBp.route('/confetud/<int:demande_id>')
@student_login_required
def confetud(demande_id):
    demande=Demande.query.filter_by(id_demande=demande_id)
    if demande:
        demande.confetud='oui'
        db.session.commit()
        return redirect(url_for('Main.accueil'))
    else:
        return jsonify(success=False, message='Demande not found')


@CoursBp.route('/accepte_report/<int:demande_id>', methods=['DELETE'])
@student_login_required
def accepte_report(demande_id):
    if request.method == 'DELETE':
        demande = Demande.query.get(demande_id)
        if demande:
            try:
                live=Live.query.filter_by(id_demande=demande_id).first()
                demande.statut_demande="report_accepte"
                demande.acceptation="oui"
                demande.aj_e="modif"
                demande.aj_p="modif"
                demande.date_acc=demande.date_propose
                duree_demande = datetime.strptime(demande.temps, '%H:%M')
                delta = timedelta(hours=duree_demande.hour, minutes=duree_demande.minute)
                # Calculer la date de fin en ajoutant la durée à la date d'acceptation
                demande.date_fin = demande.date_acc + delta
                demande.id_live=live.id
                live.date=demande.date_propose
                db.session.commit()
                return jsonify(success=True)
            except Exception as e:
                db.session.rollback()
                return jsonify(success=False, message=str(e))
        else:
            return jsonify(success=False, message='Demande not found')
        
@CoursBp.route('/delete_demande/<int:demande_id>', methods=['DELETE'])
@student_prof_login_required
def delete_demande(demande_id):
    if request.method == 'DELETE':
        demande = Demande.query.get(demande_id)
        if demande:
            db.session.delete(demande)
            db.session.commit()
            return jsonify(success=True)
        else:
            return jsonify(success=False, message='Demande not found')

@CoursBp.route('/refuse_demande/<int:demande_id>', methods=['DELETE'])
@login_required
def refuse_demande(demande_id):
    if request.method == 'DELETE':
        demande = Demande.query.get(demande_id)
        if demande:
            try:
                demande.statut_demande="refuse"
                demande.aj_e="modif"
                demande.aj_p="modif"
                db.session.commit()
                return jsonify(success=True)
            except Exception as e:
                db.session.rollback()
                return jsonify(success=False, message=str(e))
        else:
            return jsonify(success=False, message='Demande not found')


@CoursBp.route('/report/<int:demande_id>', methods=['POST',"GET"])
@login_required
def report(demande_id):
    if request.method == 'POST':
        try:
            data = request.get_json()
            dt1= data['dt1']
            date1 = datetime.fromisoformat(dt1)
            demande = Demande.query.filter_by(id_demande=demande_id).first()
            demande.date_propose=date1
            demande.aj_e="modif"
            demande.statut_demande="report_demande"
            db.session.commit()
            return redirect(url_for("Cours.programme"))
        except Exception as e:
            db.session.rollback()
            return jsonify(success=False, message=str(e))
    return render_template("report.html",demande_id=demande_id)

 

@CoursBp.route('/offreprof',methods=['POST','GET'])
def offreprof() :
        offres = Offre.query.all()
        form_submitted = False
        offres_simulees=offres 
        if request.method == 'POST':
            form_submitted = True
            criteria = request.form['criteria']
            search_query = request.form['search']
            if criteria == 'matiere':
                offres_simulees=Offre.query.filter(Offre.matiere.ilike(f'%{search_query}%')).all()
            elif criteria == 'nom_offre':
                offres_simulees = Offre.query.filter(Offre.nom_offre.ilike(f'%{search_query}%')).all() 
            else:
                offres_simulees = []   
        return render_template('offreprof.html',offres=offres_simulees,form_submitted=form_submitted)

@CoursBp.route('/ajoutoffre')
@prof_login_required_AI
def ajoutoffre() :
        return render_template('ajoutoffre.html' )


@CoursBp.route('/traiter_offre', methods=['POST'])
def traiter_offre():
    if request.method == 'POST':
        nom_offre = request.form['nom_offre']
        description = request.form['description']
        matiere = request.form['matiere']
        emplacement = request.form['emplacement']
        prix = request.form['prix']
        organisation=request.form['organisation']
        type = request.form['type']
        duree = request.form['duree']
        tel = request.form['tel']
        seances = []
        seances_presentiel = []
        jours_abreges = {
    'lundi': 'Lun',
    'mardi': 'Mar',
    'mercredi': 'Mer',
    'jeudi': 'Jeu',
    'vendredi': 'Ven',
    'samedi': 'Sam',
    'dimanche': 'Dim'
}
        for i in range(7):  # Vous pouvez ajuster cela en fonction du nombre de jours de la semaine
            jour = request.form.get(f'jour_seance_{i}')
            heure = request.form.get(f'heure_seance_{i}')
            if jour and heure:
                jour_abrege = jours_abreges.get(jour.lower(), jour)
                seance = f"{jour_abrege}-{heure}"
                seances.append(seance)
        horaire = ' | '.join(seances)
        for i in range(7):  # Vous pouvez ajuster cela en fonction du nombre de jours de la semaine
            jour = request.form.get(f'jour_seance_presentiel_{i}')
            heure = request.form.get(f'heure_seance_presentiel_{i}')
            if jour and heure:
                jour_abrege = jours_abreges.get(jour.lower(), jour)
                seance = f"{jour_abrege}-{heure}"
                seances_presentiel.append(seance)
        horaire_presentiel = ' | '.join(seances_presentiel)
        date_debut = datetime.strptime(request.form['date_debut'], '%Y-%m-%d')
        date_fin = datetime.strptime(request.form['date_fin'], '%Y-%m-%d')
        nombre_place_total = int(request.form['nombre_place_total'])
        # Vérifiez si les fichiers d'image ont été téléchargés
        if 'image_1' in request.files and 'image_2' in request.files:
            image_1 = request.files['image_1']
            image_2 = request.files['image_2']
            if allowed_file(image_1.filename) and allowed_file(image_2.filename):
                current_date = datetime.now()
                # Formatez la date actuelle en tant que chaîne pour l'utiliser dans le nom de fichier
                date_string = current_date.strftime("%Y%m%d%H%M%S")
                # Obtenez l'extension du fichier téléchargé
                file_extension1 = image_1.filename.split('.')[-1]
                file_extension2 = image_2.filename.split('.')[-1]
                # Créez un nom de fichier unique en ajoutant la date actuelle au nom d'origine
                filename_1 = f"{secure_filename(image_1.filename.replace('.', '_'))}_{date_string}.{file_extension1}"
                filename_2 = f"{secure_filename(image_2.filename.replace('.', '_'))}_{date_string}.{file_extension2}"
                filename_1 = filename_1.replace('\\', '/')
                filename_2 = filename_2.replace('\\', '/')
                # Enregistrez les fichiers dans le dossier "offres" du répertoire "static"
                path1 = "App/static"  # Chemin vers le répertoire "static" de votre application
                path2 = "offres"  # Nom du sous-dossier où vous souhaitez enregistrer les images
                image_1.save(os.path.join(path1, path2, filename_1))
                image_2.save(os.path.join(path1, path2, filename_2))
                try:
                    # Créez une instance de l'offre avec les données du formulaire
                    nouvelle_offre = Offre(
                        nom_offre=nom_offre,
                        description=description,
                        id_prof=1,
                        prix=prix,
                        type=type,
                        duree=duree,
                        Tel=tel,
                        matiere=matiere,
                        horaire=horaire,
                        horaire_presentiel=horaire_presentiel,
                        emplacement=emplacement,
                        date_debut=date_debut,
                        organisation=organisation,
                        meet=uuidv4(),
                        date_fin=date_fin,
                        nombre_place_total=nombre_place_total,
                        image_1 = os.path.join("static", path2, filename_1).replace("\\", "/"),
                        image_2 = os.path.join("static", path2, filename_2).replace("\\", "/")
                    )

                    db.session.add(nouvelle_offre)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    return jsonify(success=False, message=str(e))
                return render_template('confirmationoffre.html', message='L\'offre a été ajoutée avec succès.')
            else:
                try:  
                    nouvelle_offre = Offre(
                            nom_offre=nom_offre,
                            description=description,
                            id_prof=1,
                            prix=prix,
                            type=type,
                            Tel=tel,
                            duree=duree,
                            matiere=matiere,
                            horaire=horaire,
                            horaire_presentiel=horaire_presentiel,
                            emplacement=emplacement,
                            date_debut=date_debut,
                            organisation=organisation,
                            date_fin=date_fin,
                            meet=uuidv4(),
                            nombre_place_total=nombre_place_total,
                            image_1 ='static/image/removebg.png',
                            image_2 = 'static/image/3.png'
                        )
                    db.session.add(nouvelle_offre)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    return jsonify(success=False, message=str(e))
                return render_template('confirmationoffre.html', message='L\'offre a été ajoutée avec succès.')
    return redirect(url_for('Cours.ajoutoffre'))


@CoursBp.route('/confirmationoffre')
@prof_login_required_AI
def confirmationoffre() :
        return render_template('confirmationoffre.html' )


@CoursBp.route('/detailsoffre/<idoffre>')
@student_prof_login_required_AI
def detailsoffre(idoffre) :
        offre = Offre.query.filter_by(id=idoffre).first()
        prof=Prof.query.filter_by(id=offre.id_prof).first()
        info_prof=User.query.filter_by(id=prof.id_user_p).first()
        return render_template('detailsoffreprof.html',offre=offre,prof=prof,info_prof=info_prof)

@CoursBp.route('/abonner')
@student_login_required_AI
def abonner() : 
        user_id = session.get('userid')  # Récupère l'ID de l'utilisateur à partir de la session
        souscriptions = SubscriptionOffre.query.filter_by(id_participant=user_id).all()      
        return render_template('abonner.html',offre=offre,souscriptions=souscriptions)

@CoursBp.route('/cours-crees')
@prof_login_required_AI
def cour_crees() :   
        user_id = session.get('userid')  # Récupère l'ID de l'utilisateur à partir de la session
        prof=Prof.query.filter_by(id_user_p=user_id).first()
        offre = Offre.query.filter_by(id_prof=prof.id).all()
        return render_template('cours_crees.html',offre=offre,offres=offre)
