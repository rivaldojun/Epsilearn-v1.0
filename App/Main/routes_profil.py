from flask import render_template,jsonify,redirect,url_for,request,session,flash
from datetime import datetime
from werkzeug.utils import secure_filename
from sqlalchemy import and_
from App.Models.models import *
from App.Main.routes_about import MainBp
from App.Controllers.fonction import *
import os


#PROFIL MANAGEMENT PART
@MainBp.route('/modifierprofil',methods=['POST','GET'])
@login_required
def modifierprofil() :
    try:
        etudiant=Etudiant()
        prof=Prof()
        if session.get("role")=="etudiant":
            etudiant = Etudiant.query.filter_by(id_user_e=user.id).first()
            profile_picture_path=etudiant.photo
            if request.method=="POST":
                Nvdetud = request.form['education-level']
                ecole = request.form['ecole']
                filiere = request.form['filiere']
                etudiant.Nvdetud = Nvdetud
                etudiant.ecole = ecole
                etudiant.filiere = filiere
                profile_picture = request.files['profile-picture']
                if profile_picture:
                    save_modifier_profil_picture(file=profile_picture,ob=etudiant,us=user)
                db.session.commit()
                return redirect(url_for('Main.profil'))
        elif session.get("role")=="autre":
            autre=Autre.query.filter_by(id_user_a=user.id).first()
            profile_picture_path=user.photo
            if request.method=="POST":
                date_naiss=request.form['age']
                age=calcul_age(date_naiss)
                bio=request.form['vendervous']
                autre.age=age
                autre.vendervous=bio
                profile_picture = request.files['profile-picture']
                if profile_picture:
                    save_profile_picture(profile_picture,autre,user)
                db.session.commit()
        else:
            prof = Prof.query.filter_by(id_user_p=user.id).first()
            profile_picture_path=prof.photo
            if request.method=="POST":
                Nvdetud = request.form['education-level']
                ecole = request.form['ecole']
                filiere = request.form['filiere']
                formation=request.form['formation']
                diplome=request.form['diplome']
                bio=request.form['bio']
                prof.Nvdetud = Nvdetud
                prof.ecole = ecole
                prof.filiere = filiere
                prof.formation=formation
                prof.Diplome=diplome
                prof.vendervous=bio
                profile_picture = request.files['profile-picture']
                if profile_picture:
                    save_profile_picture(profile_picture,prof,user)
                db.session.commit()
                return redirect(url_for('Main.profil'))
    except Exception as e:
        print(e)
        db.session.rollback()
        return render_template('error.html')
    return render_template('modifierprofil.html',etudiant=etudiant,prof=prof,profile_picture_path=profile_picture_path)


@MainBp.route('/profil')
@login_required
def profil() :
    try:
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
    except:
        db.session.rollback()
        return render_template('error.html')
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