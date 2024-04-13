from flask import render_template,jsonify,redirect,url_for,request,session,flash
from App.Models.models import *
from App.Controllers.fonction import *
from App.Admin.route_studenthub_admin import *

#TABLEAU DE BORD
@AdminBp.route('/dashboard')
def dashboard():
    if session.get('admin')=='connect':
        nbuser=User.query.count()
        prix_total = db.session.query(db.func.sum(Demande.prix)).filter(Demande.statut_payement.in_(["payer"])).scalar()
        # nombre_demandes = db.session.query(Demande).filter(Demande.statut_demande.in_(["accepte", "report_accepte"])).count()
        demande=Demande.query.count()
        event=Evenement.query.count()
        langue=AbonnementLangue.query.count()
        nationalities_with_users = db.session.query(User.nationalite).distinct().all()
        nationalities_list = [nationality[0] for nationality in nationalities_with_users]
        users_count_by_nationality = db.session.query(User.nationalite, db.func.count(User.id)).filter(User.nationalite.in_(nationalities_list)).group_by(User.nationalite).all()
        nationalities = [item[0] for item in users_count_by_nationality]
        user_counts = [item[1] for item in users_count_by_nationality]
        prix_par_duree = {
            1: 8,
            3: 24,
            6: 40
        }
        # Query the AbonnementLangue records
        abonnements = AbonnementLangue.query.all()
        montant=0
        for abonnement in abonnements:
            montant += prix_par_duree[abonnement.duree]
        n=vue()
        return render_template("index.html",nbuser=nbuser,prix_total=prix_total,nationalities=nationalities,user_counts=user_counts,demande=demande,event=event,langue=langue,prixlangue=montant,n=n)
    else:
        return redirect(url_for('Main.connexion'))

@AdminBp.route('/nbuser')
def nbuser():
    if session.get('admin')=='connect':
        nbprof=Prof.query.count()
        nbetud=Etudiant.query.count()
        # Comptez le nombre total d'utilisateurs
        total_users = User.query.count()
        # Calculez le nombre d'utilisateurs qui ne sont ni professeurs ni étudiants
        nb_other_users = total_users - (nbprof + nbetud)
        n=vue()
        return render_template("nbuser.html",nbetud=nbetud,nbprof=nbprof,other=nb_other_users,n=n)
    else:
        return redirect(url_for('Main.connexion'))

@AdminBp.route('/demandedetails')
def demandedetails():
    if session.get('admin')=='connect':
        demande_payer = Demande.query.filter_by(statut_payement='payer').count()
        demande_refuse = Demande.query.filter_by(statut_demande='refuse').count()
        demande_en_attente = Demande.query.filter_by(statut_demande='enattente').count()
        demande_terminee = Demande.query.filter_by(statut_demande='termine').count()
        n=vue()
        return render_template("demandedetails.html",demande_payer=demande_payer,
                            demande_refuse=demande_refuse,
                            demande_en_attente=demande_en_attente,
                            demande_terminee=demande_terminee,n=n)
    else:
        return redirect(url_for('Main.connexion'))
#END TABLEAU DE BORD