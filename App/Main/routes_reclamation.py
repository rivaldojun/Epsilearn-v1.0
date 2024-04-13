from flask import render_template,jsonify,redirect,url_for,request,session,flash
from datetime import datetime
from App.Models.models import *
from App.Main.routes_about import MainBp
from App.Controllers.fonction import *
#RECLAMATION PART
@MainBp.route('/reclamation', methods=['GET', 'POST'])
@student_prof_login_required
def reclamation():  
    user_id = session.get("userid")
    if request.method == "POST":
        contenu = request.form['contenu'] 
        # Créer une nouvelle réclamation dans la base de données
        reclamation = Reclamation(user_id=user_id, contenu=contenu)
        db.session.add(reclamation)
        db.session.commit()
        # Rediriger l'utilisateur vers une page de confirmation ou une autre page appropriée
        return redirect(url_for('Main.confirmation_reclamation'))
    return render_template('reclamation.html')

@MainBp.route('/confirmation_reclamation')
@student_prof_login_required
def confirmation_reclamation():
    return render_template('confirmation_reclamation.html')
#END RECLAMATION PART
