from flask import render_template,jsonify,redirect,url_for,request,session
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import pycountry
import os
from App.Models.models import *
from App.Controllers.fonction import *
from App.Main.routes_about import MainBp

#INSCRIPTION PART
@MainBp.route('/inscription', methods=['GET', 'POST'])
def inscription():  
    text = text = ""
    nationalites_disponibles = [(country.name, country.alpha_2) for country in pycountry.countries]
    nationalites_disponibles.sort(key=lambda x: x[0])
    if request.method == "POST":
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        password = request.form['password']
        passwordconf = request.form['Confirm_password']
        nationalite = request.form['nationalite'] 
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
            try:
                user = User(nom=nom, prenom=prenom, mail=email, mdp=password_hash, code=code, nationalite=nationalite,pseudo=generate_pseudo())  # Ajouter la nationalité à l'objet User
                session['email'] = email
                db.session.add(user)
                db.session.commit()
                session['userid'] = user.id
                body = render_template("mail_inscription.html",nom=nom,prenom=prenom,code=code)
                send_email(os.getenv("OUR_MAIL"), email, 'Demande de confirmation', body)
            except:
                db.session.rollback()
                return render_template('error.html')
            return redirect(url_for('Main.confirmation', email=email))
    return render_template('inscription.html',error_message=text, nationalites_disponibles=nationalites_disponibles)

@MainBp.route('/confirmation/<email>',methods=["POST","GET"])
def confirmation(email):
    text=""
    if request.method == "POST":
        cd=request.form["confirmation_code"]
        user = User.query.filter_by(mail=email).first()
        code=user.code
        if cd==code:
            try:
                session['userid'] = user.id
                user.confirmer="oui"
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return render_template('error.html')
            return redirect(url_for('Main.role'))
        else:
            text=os.getenv("CODE_ERROR")
    return render_template('confirmation.html',t=text)

@MainBp.route('/role')
def role():
    return render_template('role.html')

@MainBp.route('/enregistrerprof', methods=['POST','GET'])
def enregistrerprof():
    if request.method == 'POST':
        try:
            formation=request.form['formation']
            niveau=request.form["Nvdetud"]
            filiere=request.form['filiere']
            ecole=request.form['ecole']
            diplome=request.form['diplome']
            date_naiss=request.form['age']
            age=calcul_age(date_naiss)
            vend=request.form['vendervous']
            cv=request.files['cv']
            userid=session.get('userid')
            if cv:
                current_date = datetime.now()
                date_string = current_date.strftime("%Y%m%d%H%M%S")
                file_extension = cv.filename.split('.')[-1]
                filename = f"{secure_filename(cv.filename.replace('.', '_'))}_{date_string}.{file_extension}"
                path1="App/static"
                path2="CV"
                cv.save(os.path.join(path1,path2, filename))
                cvpath = os.path.join("static",path2, filename)
            selected_disciplines = []
            for discipline in request.form.getlist('discipline[]'):
                    selected_disciplines.append(discipline)
            selected_disciplines_str = ', '.join(selected_disciplines)
            autre=Autre.query.filter_by(id_user_a=userid).first()
            if autre:
                db.session.delete(autre)
                db.session.commit()
            prof=Prof(id_user_p=int(userid), discipline=selected_disciplines_str,Nvdetud=niveau,filiere=filiere,Diplome=diplome,formation=formation,ecole=ecole,etoile=1,vendervous=vend,age=age,cv=cvpath)
            date_naiss = datetime.strptime(date_naiss, '%Y-%m-%d')
            user = User.query.filter_by(id=userid).first()
            user.ter="oui"
            user.age=age
            user.date_naiss=date_naiss
            user.role=os.getenv('PROF_ROLE_NAME')
            db.session.add(user)
            db.session.add(prof)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            return render_template('error.html')
        return redirect(url_for('Main.confirmationcompte'))
    return render_template('inscriptiontermine.html')

@MainBp.route('/enregistreretudiant', methods=['POST','GET'])
def enregistreretudiant():
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
        try:
            if autre:
                db.session.delete(autre)
                db.session.commit()
            etud = Etudiant(id_user_e=int(userid),Nvdetud=niveau,age=age,ecole=ecole,filiere=filiere,formation=formation)
            date_naiss = datetime.strptime(date_naiss, '%Y-%m-%d')
            user.ter="oui"
            user.age=age
            user.date_naiss=date_naiss
            user.role=os.getenv('STUDENT_ROLE_NAME')
            db.session.add(user)
            db.session.commit()
            db.session.add(etud)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return render_template("error.html")
        return redirect(url_for('Main.confirmationcompte'))
    return render_template('inscriptiontermine.html')

@MainBp.route('/enregistrerautre', methods=['POST','GET'])
@student_login_required_AI
def enregistrerautre():
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
        user.role=os.getenv('OTHER_ROLE_NAME')
        try:
            db.session.add(user)
            db.session.commit()
            db.session.add(autre)
            db.session.commit()
        except:
            db.session.rollback()
            return render_template("error.html")
        return redirect(url_for('Main.confirmationcompte'))
    return render_template('inscriptiontermine.html')


@MainBp.route('/confirmationcompte')
def confirmationcompte():
    return render_template('confirmationcompte.html')
# END INSCRIPTION PART