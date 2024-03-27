from flask import render_template,jsonify,redirect,url_for,request,session
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import pycountry
import os
from User.Models.models import *
from User.Controllers.fonction import *
from User.Main.routes_about import MainBp

#INSCRIPTION PART
@MainBp.route('/inscription', methods=['GET', 'POST'])
def inscription():  
    
    text = text = ""
    # Récupérer la liste de nationalités avec leurs noms en anglais et codes alpha-2
    nationalites_disponibles = [(country.name, country.alpha_2) for country in pycountry.countries]
    nationalites_disponibles.sort(key=lambda x: x[0])
    if request.method == "POST":
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        password = request.form['password']
        passwordconf = request.form['Confirm_password']
        nationalite = request.form['nationalite']  # Récupérer la nationalité sélectionnée par l'utilisateur
        # Check if the email already exists in the database
        if User.query.filter_by(mail=email).first():
            text = "Ce mail existe déjà."
        elif not is_strong_password(password):
            text = "Le mot de passe ne respecte pas les exigences de sécurité."
        elif password != passwordconf:
            text = "Les mots de passe ne correspondent pas."
        elif User.query.filter_by(nom=nom,prenom=prenom).first():
            text="Ce nom d'utilisateur existe deja"
        else:
            password_hash = generate_password_hash(password)
            code = generate_confirmation_code()
            user = User(nom=nom, prenom=prenom, mail=email, mdp=password_hash, code=code, nationalite=nationalite,pseudo=generate_pseudo())  # Ajouter la nationalité à l'objet User
            session['email'] = email
            db.session.add(user)
            db.session.commit()
            session['userid'] = user.id
            # Send password reset email
            subject = 'Demande de confirmation'
            body = render_template("mail_inscription.html",nom=nom,prenom=prenom,code=code)
            sender_email =os.getenv("OUR_MAIL")
            send_email(sender_email, email, subject, body)
            return redirect(url_for('Main.confirmation', email=email))
    return render_template('inscription.html',error_message=text, nationalites_disponibles=nationalites_disponibles)

@MainBp.route('/confirmation/<email>',methods=["POST","GET"])
def confirmation(email):
    t=""
    if request.method == "POST":
        cd=request.form["confirmation_code"]
        user = User.query.filter_by(mail=email).first()
        code=user.code
        if cd==code:
            session['userid'] = user.id
            user.confirmer="oui"
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('Main.role'))
        else:
            t="Code errone"
    return render_template('confirmation.html',t=t)

@MainBp.route('/role')
def role():
    return render_template('role.html')

@MainBp.route('/enregistrerprof', methods=['POST','GET'])
def enregistrerprof():
    if session.get('role')=="etudiant"  :
        return redirect(url_for('Main.acces_interdit'))
    if request.method == 'POST':
        formation=request.form['formation']
        niveau=request.form["Nvdetud"]
        filiere=request.form['filiere']
        ecole=request.form['ecole']
        diplome=request.form['diplome']
        date_naiss=request.form['age']
        age=calcul_age(date_naiss)
        vend=request.form['vendervous']
        cv=request.files['cv']
        if cv:
            current_date = datetime.now()
            # Formatez la date actuelle en tant que chaîne pour l'utiliser dans le nom de fichier
            date_string = current_date.strftime("%Y%m%d%H%M%S")
            # Obtenez l'extension du fichier téléchargé
            file_extension = cv.filename.split('.')[-1]
            # Créez un nom de fichier unique en ajoutant la date actuelle au nom d'origine
            filename = f"{secure_filename(cv.filename.replace('.', '_'))}_{date_string}.{file_extension}"
            path1="User/static"
            path2="CV"
            cv.save(os.path.join(path1,path2, filename))
            # Mettre à jour le chemin de la nouvelle image dans la base de données
            cvpath = os.path.join("static",path2, filename)
        # Sauvegarder les modifications dans la base de données
        db.session.commit()
        selected_disciplines = []
        for discipline in request.form.getlist('discipline[]'):
                selected_disciplines.append(discipline)
        selected_disciplines_str = ', '.join(selected_disciplines)
        autre=Autre.query.filter_by(id_user_a=user.id).first()
        if autre:
            db.session.delete(autre)
            db.session.commit()
        userid=session.get('userid')
        prof=Prof(id_user_p=int(userid), discipline=selected_disciplines_str,Nvdetud=niveau,filiere=filiere,Diplome=diplome,formation=formation,ecole=ecole,etoile=1,vendervous=vend,age=age,cv=cvpath)
        date_naiss = datetime.strptime(date_naiss, '%Y-%m-%d')
        user = User.query.filter_by(id=userid).first()
        user.ter="oui"
        user.age=age
        user.date_naiss=date_naiss
        user.role="Prof"
        db.session.add(user)
        db.session.add(prof)
        db.session.commit()
        return redirect(url_for('Main.confirmationcompte'))
    return render_template('inscriptiontermine.html')

@MainBp.route('/enregistreretudiant', methods=['POST','GET'])
def enregistreretudiant():
    if session.get('role')=="professeur"  :
        return redirect(url_for('acces_interdit'))
    if request.method == 'POST':
        niveau=request.form["niveauEtudiant"]
        filiere=request.form['filiereEtudiant']
        ecole=request.form['ecoleEtudiant']
        date_naiss=request.form['ageEtudiant']
        age=calcul_age(date_naiss)
        formation=request.form['formationetud']
        userid=session.get('userid')
        user = User.query.filter_by(id=userid).first()
        autre=Autre.query.filter_by(id_user_a=user.id).first()
        if autre:
            db.session.delete(autre)
            db.session.commit()
        etud = Etudiant(id_user_e=int(userid),Nvdetud=niveau,age=age,ecole=ecole,filiere=filiere,formation=formation)
        date_naiss = datetime.strptime(date_naiss, '%Y-%m-%d')
        user.ter="oui"
        user.age=age
        user.date_naiss=date_naiss
        user.role="Etudiant"
        db.session.add(user)
        db.session.commit()
        db.session.add(etud)
        db.session.commit()
        return redirect(url_for('Main.confirmationcompte'))
    return render_template('inscriptiontermine.html')

@MainBp.route('/enregistrerautre', methods=['POST','GET'])
def enregistrerautre():
    if session.get('role')=="professeur" :
        return redirect(url_for('Main.acces_interdit'))
    if request.method == 'POST':
        date_naiss=request.form['age']
        age=calcul_age(date_naiss)
        userid=session.get('userid')
        vend=request.form['vendervous']
        user = User.query.filter_by(id=userid).first()
        autre = Autre(id_user_a=int(userid),age=age,vendervous=vend)
        date_naiss = datetime.strptime(date_naiss, '%Y-%m-%d')
        user.ter="oui"
        user.age=age
        user.date_naiss=date_naiss
        user.role="Autre"
        db.session.add(user)
        db.session.commit()
        db.session.add(autre)
        db.session.commit()
        return redirect(url_for('Main.confirmationcompte'))
    return render_template('inscriptiontermine.html')


@MainBp.route('/confirmationcompte')
def confirmationcompte():
    return render_template('confirmationcompte.html')
# END INSCRIPTION PART