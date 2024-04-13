from flask import render_template,jsonify,redirect,url_for,request,session

from App.Admin.route_studenthub_admin import AdminBp
from App.Controllers.fonction import *
import random
#GESTION RETRAIT
@AdminBp.route('/demanderetrait')
def demanderetrait():
    if session.get('admin')=='connect':
        dem=Retrait.query.filter_by(statut="attente")
        
        return render_template("demanderetrait.html",demande=dem)
    else:
        return redirect(url_for('Main.connexion'))

@AdminBp.route('/detailsretrait/<id>')
def detailsretrait(id):
    if session.get('admin')=='connect':
        dem=Retrait.query.filter_by(id=id).first()
        prof=Prof.query.filter_by(id=id)
        user=User.query.filter_by(id=prof.id_user_p)
        
        return render_template("detailsretrait.html",demand=dem,user=user)
    else:
        return redirect(url_for('Main.connexion'))


@AdminBp.route('/validerretrait/<id>', methods=['GET'])
def tvaliderretrait(id):
    if session.get('admin')=='connect':
        dem = Retrait.query.get_or_404(id)
        dem.statut = 'valide'
        db.session.commit()
        prof=Prof.query.filter_by(id=dem.id_demandeur).first()
        prof.solde=prof.solde-dem.montant_retrait
        db.session.commit()
        return redirect(url_for('Main.demanderetrait'))
    else:
        return redirect(url_for('Main.connexion'))
#END GESTION RETRAIT