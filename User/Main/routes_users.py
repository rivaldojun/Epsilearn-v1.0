from flask import render_template,jsonify,redirect,url_for,request,session
from User.Models.models import *
from User.Controllers.fonction import *
from User.Main.routes_about import MainBp
import random

#GESTION USERS
@MainBp.route('/validerprof/<int:id>')
def validerprof(id):
    if session.get('admin')=='connect':
        if Prof.query.filter_by(id_user_p=id).first():  
            prof= Prof.query.filter_by(id_user_p=id).first()
            prof.valider="oui"
            db.session.commit()
            url="Admin.vuevaliderprof"
        return redirect(url_for(url))

@MainBp.route('/listeprofs')
def listeprofs():
    if session.get('admin')=='connect':
        n=vue()
        return render_template("listeprofs.html",n=n)

@MainBp.route('/vuevaliderprof')
def vuevaliderprof():
    if session.get('admin')=='connect':
        n=vue()
        return render_template("validerprof.html",n=n)

@MainBp.route('/listeetudiant')
def listeetudiant():
    if session.get('admin')=='connect':
        n=vue()
        return render_template("listeetudiant.html",n=n)

@MainBp.route('/get_professeurs', methods=['GET'])
def get_professeurs():
    if session.get('admin')=='connect':
        try:
            # Perform a join between the User and Prof tables to retrieve the data
            joined_data = db.session.query(User.id,User.nom,User.mail, User.prenom,User.nationalite, Prof.discipline, Prof.formation, Prof.Nvdetud, Prof.Diplome, Prof.etoile,Prof.photo,Prof.valider,Prof.cv).\
                join(Prof, User.id == Prof.id_user_p,Prof.valider=="oui").all()
            # Convert the data to a list of dictionaries
            professeurs_list = []
            for data in joined_data:
                prof_dict = {
                    'id':data.id,
                    'nom': data.nom,
                    'mail':data.mail,
                    'prenom': data.prenom,
                    'discipline': data.discipline,
                    'formation': data.formation,
                    'niveau': data.Nvdetud,
                    'diplome': data.Diplome,
                    'note': data.etoile,
                    'photo' :data.photo,
                    'valider' : data.valider,
                    'nationalite' :data.nationalite,
                    'cv':data.cv
                }
                professeurs_list.append(prof_dict)
            # Return the data as a JSON response
            return jsonify(professeurs_list)
        except Exception as e:
            # Handle the exception and return an error response
            return jsonify({'error': str(e)}), 500


@MainBp.route('/get_etudiants', methods=['GET'])
def get_etudiants():
    if session.get('admin')=='connect':
        try:
            # Perform a join between the User and Prof tables to retrieve the data
            joined_data = db.session.query(User.id,User.nom,User.mail, User.prenom,User.nationalite, Etudiant.age, Etudiant.formation, Etudiant.Nvdetud, Etudiant.filiere, Etudiant.ecole).\
                join(Etudiant, User.id == Etudiant.id_user_e).all()
            # Convert the data to a list of dictionaries
            professeurs_list = []
            for data in joined_data:
                prof_dict = {
                    'id':data.id,
                    'nom': data.nom,
                    'prenom': data.prenom,
                    'age': data.age,
                    'mail':data.mail,
                    'formation': data.formation,
                    'niveau': data.Nvdetud,
                    'filiere': data.filiere,
                    'ecole': data.ecole,
                    'nationalite' :data.nationalite,
                }
                professeurs_list.append(prof_dict)
            # Return the data as a JSON response
            return jsonify(professeurs_list)
        except Exception as e:
            # Handle the exception and return an error response
            return jsonify({'error': str(e)}), 500
    

@MainBp.route('/get_user', methods=['GET'])
def get_user():
    if session.get('admin')=='connect':
        try:
            # Perform a join between the User and Prof tables to retrieve the data
            not_in_prof = db.session.query(Prof.id_user_p)
            not_in_etudiant = db.session.query(Etudiant.id_user_e)

            # Obtenir les utilisateurs qui ne sont pas dans Prof ou Etudiant
            joined_data = db.session.query(User.id, User.nom, User.mail, User.prenom, User.nationalite).\
                filter(User.id.notin_(not_in_prof)).\
                filter(User.id.notin_(not_in_etudiant)).\
                all()
            # Convert the data to a list of dictionaries
            professeurs_list = []
            for data in joined_data:
                prof_dict = {
                    'id':data.id,
                    'nom': data.nom,
                    'prenom': data.prenom,
                    'mail':data.mail,
                    'nationalite' :data.nationalite,
                }
                professeurs_list.append(prof_dict)
            # Return the data as a JSON response
            return jsonify(professeurs_list)
        except Exception as e:
            # Handle the exception and return an error response
            return jsonify({'error': str(e)}), 500


@MainBp.route('/effacer/<int:id>')
def effaceruser(id):
    if session.get('admin')=='connect':
        user = User.query.get(id) 
        if Etudiant.query.filter_by(id_user_e=id).first():  
            etud = Etudiant.query.filter_by(id_user_e=id).first()
            db.session.delete(etud)
            db.session.commit()
            url="Admin.listeetudiant"
        elif Prof.query.filter_by(id_user_p=id).first():
            prof=Prof.query.filter_by(id_user_p=id).first()
            db.session.delete(prof)
            db.session.commit()
            url="Admin.listeprofs"
        else:
            url='Admin.other'
        db.session.delete(user)
        db.session.commit()

        return redirect(url_for(url))





#END GESTION USER