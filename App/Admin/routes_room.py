from flask import render_template,jsonify,redirect,url_for,request,session,flash
from App.Models.models import *
from App.Controllers.fonction import *
from App.Admin.route_studenthub_admin import *
#GESTION ROOM
@AdminBp.route('/room_list')
def room_list():
    if session.get('admin')=='connect':
        rooms = Room.query.all()
        return render_template('room_list.html', rooms=rooms)
    else:
        return redirect(url_for('Main.connexion'))


@AdminBp.route('/delete_room/<int:room_id>')
def delete_room(room_id):
    if session.get('admin')=='connect':
        room = Room.query.get(room_id)
        if room:
            db.session.delete(room)
            db.session.commit()
        return redirect(url_for('Room.room_list'))
    else:
        return redirect(url_for('Main.connexion'))
#END GESTION ROOM