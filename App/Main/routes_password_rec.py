from flask import render_template,jsonify,redirect,url_for,request,session,flash
from datetime import datetime,timedelta
import secrets
from werkzeug.security import generate_password_hash
from App.Models.models import *
from App.Main.routes_about import MainBp
from App.Controllers.fonction import *
#PASSWORD RECOVERY PART
@MainBp.route('/password_reset_request', methods=['GET', 'POST'])
def password_reset_request():
    text = ''
    t=""
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(mail=email).first()
        if user:
            try:
                # Generate a unique token for password reset
                token = secrets.token_urlsafe(32)
                user.password_reset_token = token
                user.password_reset_expiration = datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour
                db.session.commit()
                # Send password reset email
                reset_url = url_for('Main.password_reset', token=token, _external=True)
                subject = 'Demande de réinitialisation de mot de passe'
                body = f'Cliquez sur le lien ci-dessous pour réinitialiser votre mot de passe.:\n\n{reset_url}'
                sender_email =os.getenv("OUR_MAIL")
                send_email(sender_email, email, subject, body)
                # Display a message, whether the email exists or not, to avoid disclosing registered email addresses.
                text = "Un lien de réinitialisation de mot de passe a été envoyé à votre adresse e-mail, s'il existe dans nos enregistrements. Veuillez vérifier votre boîte de réception pour de plus amples instructions"
            except:
                db.session.rollback()
                return render_template('error.html')
        else:
          t="Ce mail ne correspond a aucun compte"
    return render_template('password_reset_request.html',error_message=text,t=t)

@MainBp.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    user_c = User.query.filter_by(password_reset_token=token).first()
    if user_c and user_c.password_reset_expiration > datetime.utcnow():
        if request.method == 'POST':
            try:
                password = request.form['password']
                confirm_password = request.form['confirm_password']
                if password != confirm_password:
                    flash('Les mots de passe ne correspondent pas. Veuillez réessayer.', 'error')
                    return redirect(url_for('Main.password_reset', token=token))
                password_hash = generate_password_hash(password)
                user_c.mdp = password_hash
                user_c.password_reset_token = None
                user_c.password_reset_expiration = None
                db.session.commit()
                session['userid'] = user_c.id
            except:
                db.session.rollback()
                return render_template('error.html')
            return redirect(url_for('Main.connexion'))  # Redirect to the user's home page after password reset
        return render_template('password_reset.html', token=token)
    return redirect(url_for('Main.invalid_token')) 
@MainBp.route('/invalid_token')
def invalid_token() :
    return render_template('invalid_token.html')
#END PASSWORD RECOVERY PART