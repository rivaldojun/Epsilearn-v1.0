from flask import render_template,jsonify,redirect,url_for,request,session
from App.Models.models import *
from App.Controllers.fonction import *
from App.Main.routes_about import MainBp
from sqlalchemy import and_,or_

#HOME PAGE PART
@MainBp.app_context_processor
def inject_param():
    return dict(current_user=current_user,np=np,nd=nd,n_stud=n_stud,user_type=session.get("role"))

@MainBp.route('/')
def visiteur():
    return redirect(url_for("Main.accueil"))


@MainBp.route('/accueil')
def accueil(): 
    print(session.get('role'))
    evenements=[]
    derniere_demande=[]
    if 'online_users' not in session:
        session['online_users']=0
    if session.get('userid') and user.ter=="oui":
        try:
            user_id = session.get('userid')
            evenements_participes = Participation.query.filter_by(id_participant=user_id).all()
            evenements_ids = [participation.id_evenement for participation in evenements_participes]
            evenements = Evenement.query.filter(Evenement.id_evenement.in_(evenements_ids)).all()
            if session.get('role')=="professeur":
                programmeprof =  Demande.query.filter(and_(or_(Demande.statut_demande == 'accepte',Demande.statut_demande == "report_accepte"), Demande.id_prof == user_id),Demande.acceptation=="oui").all()
                programmeprof = sorted(programmeprof, key=lambda demande: demande.id_demande, reverse=True)
                derniere_demande=programmeprof
            elif session.get('role')=="etudiant":
                programmeetudiant = Demande.query.filter(and_(or_(Demande.statut_demande == 'accepte',Demande.statut_demande == "report_accepte"), Demande.id_etudiant == user_id,Demande.acceptation=="oui")).all()
                programmeetudiant = sorted(programmeetudiant, key=lambda demande: demande.id_demande, reverse=True)
                derniere_demande = programmeetudiant
            else:
                derniere_demande =""
        except:
            return render_template('error.html')
    return render_template('accueil.html',evenements=evenements,pge=derniere_demande,nb=nb,online_users=session['online_users'])
#END HOME PAGE PART
