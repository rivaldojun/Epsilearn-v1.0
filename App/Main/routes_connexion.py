from flask import render_template,jsonify,redirect,url_for,request,session,flash
from werkzeug.security import  check_password_hash
from App.Models.models import *
from App.Controllers.fonction import *
from datetime import datetime, timedelta
from App.Main.routes_about import MainBp
from dotenv import load_dotenv
import os
load_dotenv()

#CONNEXION PART
@MainBp.route('/connexion', methods=['GET','POST'])
def connexion():
    existing_admin = Admin.query.filter_by(mail=os.getenv('ADMIN_MAIL')).first()
    if not existing_admin:
        a = Admin(mail=os.getenv("ADMIN_MAIL"), mdp=os.getenv("ADMIN_PASS"), superadmin="Oui")
        db.session.add(a)
        db.session.commit()
    text=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_c = User.query.filter_by(mail=email).first()
        admin=Admin.query.filter_by(mail=email).first()
        try:
                if user_c :
                    # session.permanent = True
                    if check_password_hash(user_c.mdp, password):
                        if user_c.confirmer=="non":
                            session['userid'] = user_c.id
                            return redirect(url_for('Main.confirmation',email=email))
                        if user_c.confirmer=="oui" and user_c.ter=="non":
                            session['userid'] = user_c.id
                            return redirect(url_for('Main.role',email=email))
                        if user_c.confirmer=="oui" and user_c.ter=="oui":
                            session['userid'] = user_c.id
                            if user_c.role=="Etudiant":                     
                                session['role'] = 'etudiant'
                                print('etudiant mdr inh')
                                next_url = session.pop('next_url', None)
                                if next_url:
                                    return redirect(next_url) 
                                else:
                                    return redirect(url_for('Main.accueil'))
                            elif user_c.role=="Prof" and user_c.prof[0].valider=="oui":
                                session['role'] = 'professeur'
                                print('prof wesh')
                                next_url = session.pop('next_url', None)
                                if next_url:
                                    return redirect(next_url)
                                else:
                                    return redirect(url_for('Main.accueil'))
                            elif user_c.role=="Prof" and user_c.prof[0].valider=="non":
                                text=os.getenv('NOT_VALID_ACCOUNT')
                            elif user_c.role=="Autre":
                                session['role'] = 'autre'
                                print(session.get('next_url'),"hgufhj")
                                next_url = session.pop('next_url', None)
                                if next_url:
                                    return redirect(next_url)
                                else:
                                    return redirect(url_for('Main.accueil'))                                                                     
                            else:
                                session['role'] = 'visiteur'
                                return redirect(url_for('Main.role'))
                    else:
                        text=os.getenv('INCORRECT_PASSWORD')
                elif admin:
                    session['admin'] = "connect"
                    session['superadmin']=admin.superadmin
                    return redirect(url_for('Admin.dashboard'))
                else:
                    text=os.getenv('MAIL_INEXISTANT')
        except Exception as e:
            return redirect(url_for('Main.accueil'))
    return render_template('connexion.html',error_message=text)


@MainBp.route('/deconnexion', methods=['GET','POST'])
def deconnexion():
    session.clear()
    return redirect(url_for('Main.connexion'))
    
    
    

#END CONNEXION PART
