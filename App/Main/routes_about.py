from flask import render_template,jsonify,redirect,url_for,request,session,flash,Blueprint
from App.Controllers.fonction import *
from App.Models.models import *
MainBp = Blueprint("Main",__name__,template_folder="templates")
#ABOUT PART

@MainBp.route('/about')
def about():
    return render_template('about.html')

@MainBp.route('/road')
def road():
    return render_template('road.html')


@MainBp.route('/faq')
def faq():
    return render_template('faq.html')


@MainBp.route('/pricing')
def pricing():
    return render_template('pricing.html')


@MainBp.route('/envoyermail', methods=['POST'])
def envoyermail():
    if request.method == 'POST':
        nom = request.form.get('nom')
        email = request.form.get('email')
        message = request.form.get('message')
        subject = "Message d'un utilisateur"
        body = f'De {nom} mail : {email}.:\n\n{message}'
        sender_email = os.getenv('OUR_MAIL')
        send_email(sender_email, email, subject, body)
        return redirect(url_for('confirmation', email=email))

#END ABOUT PART