from flask import render_template,jsonify,redirect,url_for,request,session,flash
from datetime import datetime
from werkzeug.utils import secure_filename
from sqlalchemy import and_
from User.Models.models import *
from User.Main.routes_about import MainBp
from User.Controllers.fonction import *
import os



#PROFIL MANAGEMENT PART
@MainBp.route('/modifierprofil',methods=['POST','GET'])
@login_required
def modifierprofil() :
      # Récupère l'utilisateur de la table User
    etudiant = Etudiant.query.filter_by(id_user_e=user.id).first()
    prof = Prof.query.filter_by(id_user_p=user.id).first()
    autre=Autre.query.filter_by(id_user_a=user.id).first()
    if session.get("role")=="etudiant":
        profile_picture_path=etudiant.photo
        if request.method=="POST":
            Nvdetud = request.form['education-level']
            ecole = request.form['ecole']
            filiere = request.form['filiere']
            # Mettre à jour les propriétés de l'étudiant avec les nouvelles valeurs
            etudiant.Nvdetud = Nvdetud
            etudiant.ecole = ecole
            etudiant.filiere = filiere
            profile_picture = request.files['profile-picture']
            if profile_picture:
                current_date = datetime.now()
                # Formatez la date actuelle en tant que chaîne pour l'utiliser dans le nom de fichier
                date_string = current_date.strftime("%Y%m%d%H%M%S")
                # Obtenez l'extension du fichier téléchargé
                file_extension = profile_picture.filename.split('.')[-1]
                # Créez un nom de fichier unique en ajoutant la date actuelle au nom d'origine
                filename = f"{secure_filename(profile_picture.filename.replace('.', '_'))}_{date_string}.{file_extension}"
                path1="User/static"
                path2="Profil"
                profile_picture.save(os.path.join(path1,path2, filename))
                # Mettre à jour le chemin de la nouvelle image dans la base de données
                etudiant.photo =os.path.join("static",path2, filename)
                user.photo =os.path.join("static",path2, filename)
            # Sauvegarder les modifications dans la base de données
            db.session.commit()
            return redirect(url_for('Main.profil'))
    elif session.get("role")=="autre":
        profile_picture_path=user.photo
        if request.method=="POST":
            date_naiss=request.form['age']
            age=calcul_age(date_naiss)
            bio=request.form['vendervous']
            autre.age=age
            autre.vendervous=bio
            profile_picture = request.files['profile-picture']
            if profile_picture:
                current_date = datetime.now()
                # Formatez la date actuelle en tant que chaîne pour l'utiliser dans le nom de fichier
                date_string = current_date.strftime("%Y%m%d%H%M%S")
                # Obtenez l'extension du fichier téléchargé
                file_extension = profile_picture.filename.split('.')[-1]
                # Créez un nom de fichier unique en ajoutant la date actuelle au nom d'origine
                filename = f"{secure_filename(profile_picture.filename.replace('.', '_'))}_{date_string}.{file_extension}"
                path1="User/static"
                path2="Profil"
                profile_picture.save(os.path.join(path1,path2, filename))
                # Mettre à jour le chemin de la nouvelle image dans la base de données
                autre.photo = os.path.join("static",path2, filename)
                user.photo =os.path.join("static",path2, filename)
            # Sauvegarder les modifications dans la base de données
            db.session.commit()
    else:
        profile_picture_path=prof.photo
        if request.method=="POST":
            Nvdetud = request.form['education-level']
            ecole = request.form['ecole']
            filiere = request.form['filiere']
            formation=request.form['formation']
            diplome=request.form['diplome']
            bio=request.form['bio']
            # Mettre à jour les propriétés de l'étudiant avec les nouvelles valeurs
            prof.Nvdetud = Nvdetud
            prof.ecole = ecole
            prof.filiere = filiere
            prof.formation=formation
            prof.Diplome=diplome
            prof.vendervous=bio
            profile_picture = request.files['profile-picture']
            if profile_picture:
                current_date = datetime.now()
                # Formatez la date actuelle en tant que chaîne pour l'utiliser dans le nom de fichier
                date_string = current_date.strftime("%Y%m%d%H%M%S")
                # Obtenez l'extension du fichier téléchargé
                file_extension = profile_picture.filename.split('.')[-1]
                # Créez un nom de fichier unique en ajoutant la date actuelle au nom d'origine
                filename = f"{secure_filename(profile_picture.filename.replace('.', '_'))}_{date_string}.{file_extension}"
                path1="User/static"
                path2="Profil"
                profile_picture.save(os.path.join(path1,path2, filename))
                # Mettre à jour le chemin de la nouvelle image dans la base de données
                prof.photo = os.path.join("static",path2, filename)
                user.photo =os.path.join("static",path2, filename)
            # Sauvegarder les modifications dans la base de données
            db.session.commit()
            return redirect(url_for('Main.profil'))
    return render_template('modifierprofil.html',etudiant=etudiant,prof=prof,profile_picture_path=profile_picture_path)


@MainBp.route('/profil')
@login_required
def profil() :
    etudiant = Etudiant.query.filter_by(id_user_e=user.id).first()
    prof = Prof.query.filter_by(id_user_p=user.id).first()
    autre = Autre.query.filter_by(id_user_a=user.id).first()
    if session.get("role")=="professeur":
        profile_picture_path=prof.photo
        idprof=prof.id
    if session.get("role")=="etudiant":
        profile_picture_path=etudiant.photo
        idprof=""
    if session.get('role')=="autre":
        profile_picture_path=user.photo
        idprof=""
    return render_template('profil.html',user=user,prof=prof,etudiant=etudiant,profile_picture_path=profile_picture_path,idprof=idprof)

@MainBp.route('/profilprof/<int:prof_id>',methods=["POST","GET"])
@login_required
def profilprof(prof_id) :
    
    user_id = session.get('userid')  # Récupère l'ID de l'utilisateur à partir de la session
      # Récupère l'utilisateur de la table User
    prof = Prof.query.filter_by(id=prof_id,valider="oui").first()
    userp=User.query.filter_by(id=prof.id_user_p).first()
    nom=userp.nom
    prenom=userp.prenom
    niveau=prof.Nvdetud
    formation=prof.formation
    diplome=prof.Diplome
    bio=prof.vendervous
    discipline=prof.discipline
    photo=prof.photo
    note=prof.etoile
    com = Comment.query.filter(and_(Comment.etudiant_id==User.id,Comment.prof_id==prof_id)).all()
    if request.method=="POST":
        etudiant_id = user_id
        prof_id = prof_id
        commentaire = request.form.get('commentaire')
        if commentaire is not None:
            comment = Comment(etudiant_id=etudiant_id, prof_id=prof_id, commentaire=commentaire)
            db.session.add(comment)
            db.session.commit()
        # Renvoyer une réponse JSON indiquant le succès de la mise à jour
        response = jsonify(success=True)
        # Récupérer l'URL de la page actuelle et la renvoyer comme réponse JSON
        referrer_url = request.referrer
        response.headers['Location'] = referrer_url
        # Renvoyer une réponse avec un code de redirection (302) pour recharger la page
        return response, 302
    return render_template("profilprof.html",nom=nom,Prenom=prenom,Discipline=discipline,Formation=formation,Niveau=niveau,Diplome=diplome,photo=photo,bio=bio,note=note,commentaires=com,nat=userp.nationalite)


@MainBp.route('/listeprof')
def listeprof():
    # Effectuez une jointure entre les tables User et Prof
    user_id = session.get('userid')
    # Passez les données à un modèle HTML pour l'affichage
    return render_template('liste_professeurs.html', professeurs=professeurs,user_id=user_id)


#END PROFIL MANAGEMENT PART