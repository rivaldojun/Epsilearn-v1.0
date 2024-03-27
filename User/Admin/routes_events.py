from flask import render_template,jsonify,redirect,url_for,request,session,flash
from User.Models.models import *
from User.Controllers.fonction import *
from User.Admin.route_studenthub_admin import *
#GESTION EVENT
@AdminBp.route('/effacerevent/<int:idev>')
def effacerevent(idev):
    if session.get('admin')=='connect':
        event = Evenement.query.get(idev) 
        db.session.delete(event)
        db.session.commit()
        url='Event.evenement'
        return redirect(url_for(url))
    else:
        return redirect(url_for('Main.connexion'))


@AdminBp.route('/details_evenement/<int:idev>',methods=["POST","GET"])
def details_evenement(idev) :
    if session.get('admin')=='connect':
        evenement= Evenement.query.filter_by(id_evenement=idev).first()
        n=vue()
        return render_template('detailsevenement.html',evenement=evenement,n=n)
    else:
        return redirect(url_for('Main.connexion'))

@AdminBp.route('/evenements')
def evenements():
    if session.get('admin')=='connect':
        n=vue()
        return render_template('evenements.html',n=n)
    else:
        return redirect(url_for('Main.connexion'))


@AdminBp.route('/get_events', methods=['GET'])
def get_events():
    if session.get('admin')=='connect':
        try:
            joined_data = db.session.query(Evenement.id_evenement,Evenement.id_organisateur,Evenement.Nom, Evenement.date, Evenement.type_ev, Evenement.nbplace, Evenement.nbplace_occupe, Evenement.lien, Evenement.live, Evenement.vue, Evenement.description, Evenement.photo, Evenement.statut,User.nom,User.prenom,User.id).\
                join(User, User.id == Evenement.id_organisateur).all()
            professeurs_list = []
            for data in joined_data:
                prof_dict = {
                    'id':data.id_evenement,
                    'userid':data.id,
                    'organisateurid':data.id_organisateur,
                    'nomevent': data.Nom,
                    'nom': data.nom,
                    'prenom': data.prenom,
                    'date': data.date,
                    'type': data.type_ev,
                    'nbplace': data.nbplace,
                    'nbplace_occupe': data.nbplace_occupe,
                    'live': data.live,
                    'lien': data.lien,
                    'description' :data.description,
                    'photo' :data.photo,
                    'statut' :data.statut,
                    'vue' :data.vue,
                    'ig' :session.get('userid')
                }       
                professeurs_list.append(prof_dict)
            # Return the data as a JSON response
            return jsonify(professeurs_list)
        except Exception as e:
            # Handle the exception and return an error response
            return jsonify({'error': str(e)}), 500
    else:
        return redirect(url_for('Main.connexion'))

#END GESTION EVENT   