from flask import render_template,jsonify,redirect,url_for,request,session,flash
from datetime import datetime,timedelta
from flask_socketio import SocketIO, emit,join_room
from App.Models.models import *
from App import socketio
from App.Controllers.fonction import *
from App.Main.routes_about import MainBp
#MEETING PART
users = []
rooms = {}
socket_room = {}
socket_name = {}
mic_socket = {}
video_socket = {}
room_board = {}
@socketio.on('connect')
def on_connect():
   print("client connecte")

@MainBp.route('/room/<cd>', methods=['GET'])
def room(cd) :
    groupe=None
    demande=None
    live=None
    est_participant_ou_organisateur=None
    st=None
    warning_threshold = timedelta(minutes=15)
    user_id=session.get('userid')
    cours=Offre.query.filter_by(meet=cd).first()
    souscriptions = SubscriptionOffre.query.filter_by(id_offre=cours.id,id_participant=user_id).first()
    if souscriptions:
        date_fin=datetime.now()+timedelta(hours=5)
    abonnement = AbonnementLangue.query.filter_by(id_abonne=user_id).first()
    if abonnement:
        groupe = groupelangue.query.filter_by(id=abonnement.id_groupe, lien=cd).first()
        date_fin=abonnement.datefin
    st=StartLive.query.filter_by(id_participant=user_id,code=cd).first()
    if st:
       live = Live.query.filter_by(id=st.id_live).first()
       if live:
            demande = Demande.query.filter_by(id_demande=live.id_demande).first()
            date_fin=demande.date_fin
    evenement = Evenement.query.filter_by(cd=cd).first()
    if evenement:
        est_participant_ou_organisateur = (
            Participation.query.filter_by(id_evenement=evenement.id_evenement, id_participant=user_id).first()
            or evenement.id_organisateur == int(user_id)
        )
        date_fin=datetime.now()+timedelta(hours=5)
    
    if live or groupe or est_participant_ou_organisateur or abonnement or souscriptions:
       if date_fin-datetime.now()<warning_threshold:
          return render_template('meeting_warning.html', time_until_end=date_fin-datetime.now(),meet_url=f'https://meet.jit.si/{cd}')
       elif datetime.now()>date_fin:
          return redirect(url_for("Main.endmeet"))
       else:
         meet_url = f'https://meet.jit.si/{cd}'
        #  return f'<script>window.open("{meet_url}", "_blank");</script>'
         return redirect(meet_url)
    else:
       return redirect(url_for("Main.acces_interdit"))


@MainBp.route('/endmeet')
def endmeet():
    return render_template('endmeet.html')

@socketio.on('audio_transcription')
def handle_audio_transcription(data):
    transcription = data['transcription']
    transcription=traduire_vers_anglais(transcription)
    emit('subtitles', {'text': transcription})

@socketio.on('join room')
def on_join_room(data):
    roomid = data['roomid']
    username = data['username']
    join_room(roomid)
    socket_room[request.sid] = roomid
    socket_name[request.sid] = username
    mic_socket[request.sid] = 'off'
    video_socket[request.sid] = 'off'
    if roomid in rooms and len(rooms[roomid]) > 0:
        rooms[roomid].append(request.sid)
        emit('message', {'msg': f'{socket_name[request.sid]} join the chat.', 'username': 'Bot', 'timestamp': "now"}, room=roomid,broadcast=True)
        emit('join room', {'peers': [pid for pid in rooms[roomid] if pid != request.sid],
                           'socketname': socket_name, 'micSocket': mic_socket, 'videoSocket': video_socket}, room=request.sid,broadcast=True)
    else:
        rooms[roomid] = [request.sid]
        emit('join room', {'peers': None, 'socketname': None, 'micSocket': None, 'videoSocket': None}, room=request.sid,broadcast=True)
    emit('user count', len(rooms[roomid]), room=roomid,broadcast=True)

@socketio.on('action')
def on_action(msg):
    if msg == 'mute':
        mic_socket[request.sid] = 'off'
    elif msg == 'unmute':
        mic_socket[request.sid] = 'on'
    elif msg == 'videoon':
        video_socket[request.sid] = 'on'
    elif msg == 'videooff':
        video_socket[request.sid] = 'off'
    emit('action', {'msg':msg,'sid':request.sid}, room=socket_room[request.sid],broadcast=True)

@socketio.on('start-speaking')
def handle_start_speaking(nom):
    message = f' {nom}'
    emit('display-message', message, broadcast=True)

@socketio.on('video-offer')
def on_video_offer(data):
    offer, sid = data['offer'], data['sid']
    emit('video-offer', {
        'offer': offer,
        'sender_sid': request.sid,
        'sender_name': socket_name[request.sid],
        'mic_status': mic_socket[request.sid],
        'video_status': video_socket[request.sid]
    }, room=sid,broadcast=True)

@socketio.on('video-answer')
def on_video_answer(data):
    answer, sid = data['answer'], data['sid']
    emit('video-answer', {'answer': answer, 'sender_sid': request.sid}, room=sid,broadcast=True)


@socketio.on('new icecandidate')
def on_new_icecandidate(data):
    candidate, sid = data['candidate'], data['sid']
    emit('new icecandidate', {'candidate': candidate, 'sender_sid': request.sid}, room=sid,broadcast=True)


@socketio.on('message')
def on_message(data):
    msg, username, roomid, timestamp = data['msg'], data['username'], data['roomid'], data['timestamp']
    emit('message', {'msg': msg, 'username': username, 'timestamp': timestamp}, room=roomid,broadcast=True)


@socketio.on('getCanvas')
def on_get_canvas():
    if socket_room[request.sid] in room_board:
        emit('getCanvas', room_board[socket_room[request.sid]],broadcast=True)


@socketio.on('draw')
def on_draw(data):
    newx, newy, prevx, prevy, color, size = data['newx'], data['newy'], data['prevx'], data['prevy'], data['color'], data['size']
    emit('draw', {'newx': newx, 'newy': newy, 'prevx': prevx, 'prevy': prevy, 'color': color, 'size': size},
         room=socket_room[request.sid])


@socketio.on('clearBoard')
def on_clear_board():
    emit('clearBoard', room=socket_room[request.sid])


@socketio.on('store canvas')
def on_store_canvas(url):
    room_board[socket_room[request.sid]] = url


@socketio.on('disconnect')
def on_disconnect():
    chatroom = ChatRoom.query.filter_by(user_id=session.get("userid"), room_id=session.get("room")).first()
    if chatroom:
        db.session.delete(chatroom)
        db.session.commit()
    return
#END MEETING PART