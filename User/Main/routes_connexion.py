from flask import render_template,jsonify,redirect,url_for,request,session,flash
from werkzeug.security import  check_password_hash
from User.Models.models import *
from User.Controllers.fonction import *
from datetime import datetime, timedelta
from User.Main.routes_about import MainBp
from dotenv import load_dotenv
import os
load_dotenv()

#CONNEXION PART
@MainBp.route('/connexion', methods=['GET','POST'])
def connexion():
    existing_admin = Admin.query.filter_by(mail="mohammedia14@casa.rabat").first()
    # Si aucun enregistrement existant n'est trouvé, créez-en un
    if not existing_admin:
        a = Admin(mail=os.getenv("ADMIN_MAIL"), mdp=os.getenv("ADMIN_PASS"), superadmin="Oui")
        db.session.add(a)
        db.session.commit()
    session.clear()
    text=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_c = User.query.filter_by(mail=email).first()
        admin=Admin.query.filter_by(mail=email).first()
        if user_c :
            session.permanent = True
            if check_password_hash(user_c.mdp, password):
                if user_c.confirmer=="non":
                    session['userid'] = user_c.id
                    return redirect(url_for('Main.confirmation',email=email))
                if user_c.confirmer=="oui" and user_c.ter=="non":
                   session['userid'] = user_c.id
                   return redirect(url_for('Main.role',email=email))
                if user_c.confirmer=="oui" and user_c.ter=="oui":
                   etudiant = Etudiant.query.filter_by(id_user_e=user_c.id).first()
                   prof = Prof.query.filter_by(id_user_p=user_c.id).first()
                   autre=Autre.query.filter_by(id_user_a=user_c.id).first()
            
                   if etudiant:                     
                       session['userid'] = user_c.id
                       session['role'] = 'etudiant'
                       
                       return redirect(url_for('Main.accueil'))  # Redirige vers la page des étudiants
                   elif prof and prof.valider=="oui":
                       session['userid'] = user_c.id
                       session['role'] = 'professeur'
                       return redirect(url_for('Main.accueil'))  # Redirige vers la page des professeurs
                   elif prof and prof.valider=="non":
                       text="Votre Compte prof n'est pas encore valider par les admins"
                   elif autre:
                       session['userid'] = user_c.id
                       session['role'] = 'autre'
                       return redirect(url_for('Main.accueil'))  # Redirige vers la page des professeurs    
                   else:
                    # Gérer le cas où l'utilisateur n'est ni un étudiant ni un professeur
                       session['role'] = 'visiteur'
                       return redirect(url_for('Main.role'))  # Redirige vers une page pour les utilisateurs inconnus     
            else:
                text='Mot de passe incorrecte'
        elif admin:
            session['admin'] = "connect"
            session['superadmin']=admin.superadmin
            return redirect(url_for('Admin.dashboard'))
        else:
            text='Mail inexistant'    
    return render_template('connexion.html',error_message=text)

#END CONNEXION PART
