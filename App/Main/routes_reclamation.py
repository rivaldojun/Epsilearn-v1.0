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
        try:
            contenu = request.form['contenu'] 
            reclamation = Reclamation(user_id=user_id, contenu=contenu)
            db.session.add(reclamation)
            db.session.commit()
            return redirect(url_for('Main.confirmation_reclamation'))
        except Exception as e:
            db.session.rollback()
            return render_template('error.html')
    return render_template('reclamation.html')

@MainBp.route('/confirmation_reclamation')
@student_prof_login_required
def confirmation_reclamation():
    return render_template('confirmation_reclamation.html')
#END RECLAMATION PART
