from flask import render_template,jsonify,redirect,url_for,request,session
from App.Models.models import *
from App.Controllers.fonction import *
from App.Admin.route_studenthub_admin import *
#GESTION RECLAMATION
@AdminBp.route('/reclamations_non_traitees', methods=['GET'])
def reclamations_non_traitees():
    if session.get('admin')=='connect':
        reclamations = Reclamation.query.filter_by(traite='non').all()
        for reclamation in reclamations:
            reclamation.vue = 'oui'
        db.session.commit()
        n=vue()
        return render_template('reclamations_non_traitees.html', reclamations=reclamations,n=n)
    else:
        return redirect(url_for('Main.connexion'))


@AdminBp.route('/traiter_reclamation/<int:reclamation_id>', methods=['GET'])
def traiter_reclamation(reclamation_id):
    if session.get('admin')=='connect':
        reclamation = Reclamation.query.get_or_404(reclamation_id)
        reclamation.traite = 'oui'
        db.session.commit()
        return redirect(url_for('Main.reclamations_non_traitees'))
    else:
        return redirect(url_for('Main.connexion'))


@AdminBp.route('/other')
def other():
    if session.get('admin')=='connect':
        n=vue()
        return render_template("other.html",n=n)
    else:
        return redirect(url_for('Main.connexion'))
#END GESTION RECLAMATION
