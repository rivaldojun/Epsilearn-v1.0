from flask import render_template,redirect,url_for,request,session
from datetime import datetime
from App.Models.models import *
from App.Controllers.fonction import *
from App.Cours.routes_booking import *

#PROFESSOR PAYEMENT PART
@CoursBp.route('/solde')
@prof_login_required
def solde():
    user_id = session.get("userid")
    s=0
    prof=Prof.query.filter_by(id_user_p=user_id).first()
    demandeconf=Demande.query.filter_by(id_prof=prof.id,ajout="non",confetud='oui',confprof='oui').all()
    if demandeconf:
        try:
            for dem in demandeconf:
                s=s+dem.prix
            prof.solde=prof.solde+s
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify(success=False, message=str(e))
    user_balance = prof.solde
    return render_template('solde.html', user_balance=user_balance)


@CoursBp.route('/retrait/<montant>', methods=['POST'])
@prof_login_required
def retrait(montant):
    user_id = session.get("userid")
    user = Prof.query.filter_by(id_user_p=user_id).first()
    user_balance = user.solde
    if request.method == 'POST':
        try:
            nom = request.form['nom']
            numero_carte = request.form['numero_carte']
            montant_retrait = float(montant)
            if montant_retrait<user_balance:
                nouveau_retrait = Retrait(nom=nom,id_demandeur=user.id, numero_carte=numero_carte, montant_retrait=montant_retrait)
                db.session.add(nouveau_retrait)
                db.session.commit()
                return "Retrait enregistré en attente de traitement."
            else:
                return "Retrait impossible.Respectez-vous monsieur"
        except Exception as e:
            db.session.rollback()
            return jsonify(success=False, message=str(e))


@CoursBp.route('/historiqueretrait')
@prof_login_required
def historiqueretrait():
    user_id = session.get("userid")
    user = Prof.query.filter_by(id_user_p=user_id).first()
    data=Retrait.query.filter_by(id_demandeur=user.id,statut="valide").all()
    return render_template('historiqueretrait.html', retraits=data)


@CoursBp.route('/retrait_info',methods=["POST","GET"])
@prof_login_required
def retrait_info():
    if request.method == 'POST':
        montant = request.form['montant']
    user_id = session.get("userid") 
    user = Prof.query.filter_by(id_user_p=user_id).first()
    data=Retrait.query.filter_by(id_demandeur=user.id,statut="valide").all()
    return render_template('retrait_info.html', retraits=data,montant=montant)
#END PROFESSOR PAYEMENT PART