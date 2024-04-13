from flask import render_template,jsonify,redirect,url_for,request,session,flash
from App.Controllers.fonction import *
from App.Main.routes_about import MainBp

#FORBIDDEN ACCES PART
@MainBp.route('/acces-interdit')
def acces_interdit():
    return render_template('acces-interdit.html')
#END FORBIDDEN ACCES PART