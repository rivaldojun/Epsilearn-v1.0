from flask import render_template,jsonify,redirect,url_for,request,session
from App.Models.models import *
from App.Main.routes_about import MainBp
from App.Controllers.fonction import *
import random
#GESTION RETRAIT
@MainBp.route('/demanderetrait')
def demanderetrait():
    if session.get('admin')=='connect':
        dem=Retrait.query.filter_by(statut="attente")
        n=vue()
        return render_template("demanderetrait.html",demande=dem,n=n)
    else:
        return redirect(url_for('Main.connexion'))

@MainBp.route('/detailsretrait/<id>')
def detailsretrait(id):
    if session.get('admin')=='connect':
        dem=Retrait.query.filter_by(id=id).first()
        prof=Prof.query.filter_by(id=id)
        user=User.query.filter_by(id=prof.id_user_p)
        n=vue()
        return render_template("detailsretrait.html",demand=dem,n=n,user=user)
    else:
        return redirect(url_for('Main.connexion'))


@MainBp.route('/validerretrait/<id>', methods=['GET'])
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