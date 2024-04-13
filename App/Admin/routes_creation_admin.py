import uuid
import json
from flask import render_template,jsonify,redirect,url_for,request,session,flash
from datetime import datetime,timedelta
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_,or_
from sqlalchemy import func
import os
from flask_socketio import SocketIO, emit, send,join_room,disconnect
import pycountry
import stripe
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from App.Models.models import *
from App.Controllers.fonction import *
from App.Admin.route_studenthub_admin import *

#INSCRIPTION PART
@AdminBp.route('/creationadmin', methods=['GET', 'POST'])
def creation_admin():
    admins = Admin.query.all()
    # Check if there are no superadmins
    superadmins_exist = any(admin.superadmin == "Oui" for admin in admins)
    if session.get('superadmin') == 'Oui' or (not superadmins_exist and session.get('admin') == 'connect'):
        if request.method == "POST":
            mail = request.form['mail']
            mdp = request.form['motdepasse']
            superadmin = request.form['role']
            admin=Admin(mail=mail,mdp=mdp,superadmin=superadmin)
            existing_admin = Admin.query.filter_by(mail=mail).first()
            if existing_admin:
                flash('Admin with this email already exists.', 'error')
            else:
                db.session.add(admin)
                db.session.commit()
                flash('Admin created successfully.', 'success')
    else:
        return "Vous ne pouvez ps effectuer cette operation"
    return render_template('creation_admin.html',n=vue())


@AdminBp.route('/admin_list')
def admin_list():
    # Fetch all admin records from the database
    admins = Admin.query.all()
    return render_template('admin_list.html', admins=admins,n=vue())

@AdminBp.route('/remove_admin/<int:admin_id>')
def remove_admin(admin_id):
    if session.get('superadmin')=='Oui':
        admin = Admin.query.get(admin_id)
        if admin:
            if admin.superadmin == "Oui":
                flash("Superadmin cannot be removed.", "warning")
            else:
                db.session.delete(admin)
                db.session.commit()
                flash("Admin removed successfully.", "success")
    else:
        return "Vous ne pouvez ps effectuer cette operation"
    return redirect(url_for('Admin.admin_list'))

@AdminBp.route('/ajouter_etudiant', methods=['GET', 'POST'])
def ajouter_etudiant():
    if session.get('admin')=='connect':
        nationalites_disponibles = [(country.name, country.alpha_2) for country in pycountry.countries]
        nationalites_disponibles.sort(key=lambda x: x[0])
        if request.method == 'POST':
            nom = request.form['nom']
            prenom = request.form['prenom']
            nationalite = request.form['nationalite']
            mail = request.form['mail']
            age = int(request.form['ageEtudiant'])  # Assurez-vous que l'âge est un entier
            formation = request.form['formationetud']
            filiere = request.form['filiereEtudiant']
            niveau = request.form['niveauEtudiant']
            ecole = request.form['ecoleEtudiant']
            motdepasse= request.form['motdepasse']
            password_hash = generate_password_hash(motdepasse)
            us=User.query.filter_by(mail=mail).first()
            if not us:
                nouvel_utilisateur = User(nom=nom, prenom=prenom, nationalite=nationalite, mail=mail,mdp=password_hash,ter="oui",confirmer="oui",age=age,pseudo=generate_pseudo())
                db.session.add(nouvel_utilisateur)
                db.session.commit()
                nouvel_etudiant = Etudiant(id_user_e=nouvel_utilisateur.id, Nvdetud=niveau, formation=formation, age=age, filiere=filiere, ecole=ecole)
                db.session.add(nouvel_etudiant)
                db.session.commit()
            else:
                return "Mail existant"
            return redirect(url_for('Admin.ajouter_etudiant'))  # Rediriger vers la page d'accueil ou une autre page
        n=vue()
        return render_template('ajouter_etudiant.html',nationalites_disponibles=nationalites_disponibles,n=n)

@AdminBp.route('/ajouter_prof', methods=['GET', 'POST'])
def ajouter_prof():
    if session.get('admin')=='connect':
        nationalites_disponibles = [(country.name, country.alpha_2) for country in pycountry.countries]
        nationalites_disponibles.sort(key=lambda x: x[0])
        if request.method == 'POST':
            nom = request.form['nom']
            prenom = request.form['prenom']
            nationalite = request.form['nationalite']
            mail = request.form['mail']
            formation=request.form['formation']
            niveau=request.form["Nvdetud"]
            filiere=request.form['filiere']
            ecole=request.form['ecole']
            diplome=request.form['diplome']
            age=int(request.form['age'])
            etoile=int(request.form['etoile'])
            vend=request.form['vendervous']
            discipline=request.form['discipline[]']
            motdepasse= request.form['motdepasse']
            password_hash = generate_password_hash(motdepasse)
            us=User.query.filter_by(mail=mail).first()
            if not us:
                nouvel_utilisateur = User(nom=nom, prenom=prenom, nationalite=nationalite, mail=mail,mdp=password_hash,ter="oui",confirmer="oui",age=age,pseudo=generate_pseudo())
                db.session.add(nouvel_utilisateur)
                db.session.commit()
                prof=Prof(id_user_p=nouvel_utilisateur.id, discipline=discipline,Nvdetud=niveau,filiere=filiere,Diplome=diplome,formation=formation,ecole=ecole,etoile=etoile,vendervous=vend,age=age,valider="oui")
                db.session.add(prof)
                db.session.commit()
            else:
                return "Mail existant"
            return redirect(url_for('Admin.ajouter_prof')) 
        n=vue()
        return render_template('ajouter_prof.html',nationalites_disponibles=nationalites_disponibles,n=n)

@AdminBp.route('/affecter_groupe', methods=["POST","GET"])
def affecter_groupe():
    if session.get('admin')=='connect':
        # groupe_id=request.form["groupe"]
        groupes = []
        for groupe in groupelangue.query.all():
            nb_abonnes = AbonnementLangue.query.filter_by(id_groupe=groupe.id).count()
            if nb_abonnes < 6:
                groupes.append(groupe)
        if len(groupes)==0:
            groupe_id=None
        else:
            groupe_id=request.form.get("groupe")
        if request.method == 'POST':
            groupe_id_input=request.form["groupeinput"]
            if  groupe_id_input:
                ex=groupelangue.query.get(groupe_id_input)
            if not groupe_id_input and not groupe_id:
                return "choisissez un groupe"
            utilisateur_id = int(request.form['utilisateur'])
            langue = request.form['langue']
            abonnement = AbonnementLangue.query.filter_by(id_abonne=utilisateur_id,nom=langue).first()
            if groupe_id_input:
                if ex:
                    return "Groupe existant"
                else:
                    lien=uuidv4()
                    groupe_exist = groupelangue.query.filter_by(lien=lien).first()
                    if groupe_exist:
                        lien=uuidv4()
                    else:
                        groupe=groupelangue(id=groupe_id_input,lien=lien,nom=langue)
                        abonnement.id_groupe = groupe_id_input
                        db.session.add(groupe)
            else:
                abonnement.id_groupe = groupe_id
                db.session.commit()
                return redirect(url_for('Admin.affecter_groupe'))
        sans_groupe = AbonnementLangue.query.filter_by(id_groupe=None).all()
        
        n=vue()
        return render_template('affecter_groupe.html',  utilisateurs=sans_groupe,n=n,groupes=groupes)

