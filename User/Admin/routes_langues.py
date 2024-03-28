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
from User.Models.models import *
from User.Controllers.fonction import *
from User.Admin.route_studenthub_admin import *

#GESTION LANGUES
@AdminBp.route('/chiffrelangue')
def chiffrelangue():
    if session.get('admin')=='connect':
        result = db.session.query(AbonnementLangue.nom, func.count(AbonnementLangue.id_abonne)).group_by(AbonnementLangue.nom).all()
    # Créer un dictionnaire pour stocker les résultats
        nombre_abonnes_par_langue = {nom_langue: count for nom_langue, count in result}
            # Define the dictionary of prices per duration
        prix_par_duree = {
            1: 8,
            3: 24,
            6: 40
        }
        
        # Query the AbonnementLangue records
        abonnements = AbonnementLangue.query.all()
        
        # Initialize a dictionary to store the total amounts per name
        montants_par_nom = {
            'francais': 0,
            'anglais': 0,
            'darija': 0
        }
        
        # Calculate the total amounts per name
        for abonnement in abonnements:
            montants_par_nom[abonnement.nom] += prix_par_duree[abonnement.duree]
        n=vue()
        return render_template("chiffrelangue.html",chiffre=montants_par_nom,nombre=nombre_abonnes_par_langue,n=n)
    else:
        return redirect(url_for('Main.connexion'))
@AdminBp.route('/getlangue/<langue>')
def get_langue(langue):
    if session.get('admin')=='connect':
        groupes = groupelangue.query.filter_by(nom=langue).all()
        groupe_ids = [groupe.id for groupe in groupes]

        return jsonify({"groupe_ids": groupe_ids})
    else:
        return redirect(url_for('Main.connexion'))

# Charger les sujets depuis le fichier JSON
def load_sujet():
    with open('langue/sujet.json', 'r') as f:
        suj = json.load(f)["conversations"]
    return suj

def get_available_saturdays():
    # Obtenir la date actuelle
    current_date = datetime.now()

    # Trouver le prochain samedi à 16h00
    next_saturday = current_date + timedelta(days=(5 - current_date.weekday()) % 7)
    next_saturday = next_saturday.replace(hour=16, minute=0, second=0, microsecond=0)

    # Charger les sujets à partir du fichier JSON
    sujets = load_sujet()
    # Générer les prochains samedis non définis dans le JSON
    available_saturdays = []
    while True:
        saturday_string = next_saturday.strftime("%Y-%m-%dT%H:%M:%S")
        if not any(item["date"] == saturday_string for item in sujets):
            available_saturdays.append(saturday_string)
        next_saturday += timedelta(weeks=1)
        if next_saturday.year > current_date.year + 1:
            break
    
    return available_saturdays


@AdminBp.route("/sujet", methods=["GET", "POST"])
def sujet():
    if session.get('admin')=='connect':
        suj=load_sujet()
        # Initialiser la liste sujets
        sujets = []
        if request.method == "POST":
            date = request.form["date"]
            sujet = request.form["sujet"]

            # Charger les sujets à partir du fichier JSON existant
            with open('langue/sujet.json', 'r') as f:
                data = json.load(f)
                sujets = data["conversations"]

            # Ajouter le nouveau sujet à la liste
            sujets.append({"date": date, "sujet": sujet})

            # Écrire la liste mise à jour dans le fichier JSON
            with open('langue/sujet.json', 'w') as f:
                json.dump({"conversations": sujets}, f, indent=4)

        available_saturdays = get_available_saturdays()
        return render_template('suj.html', available_saturdays=available_saturdays, sujets=suj)
    else:
        return redirect(url_for('Main.connexion'))

@AdminBp.route("/groupes")
def groupes():
    if session.get('admin')=='connect':
        groupes = groupelangue.query.all()
        return render_template("groupes.html", groupes=groupes)
    else:
        return redirect(url_for('Main.connexion'))

@AdminBp.route("/groupe/<int:groupe_id>")
def groupe_detail(groupe_id):
    if session.get('admin')=='connect':
        groupe = groupelangue.query.get(groupe_id)
        participants = AbonnementLangue.query.filter_by(id_groupe=groupe_id).all()
        return render_template("detail_groupe.html", groupe=groupe, participants=participants)
    else:
        return redirect(url_for('Main.connexion'))
# END GESTION LANGUE
