from flask import session
from datetime import datetime,timedelta
from email.mime.text import MIMEText
import smtplib
import math
import string
import re
import uuid
from sqlalchemy import or_
from sqlalchemy import func
import random
from googletrans import Translator
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import Counter
from User.Models.models import *
from User.Repository import *
from werkzeug.utils import secure_filename
import os
from User import redis_store


def determine_role(user):
    if Etudiant.query.filter_by(id_user_e=user.id).first():
        return "étudiant"
    elif Prof.query.filter_by(id_user_p=user.id).first():
        return "professeur"
    else:
        return "inconnu"
    
def update_aj_column_e():
    Demande.query.filter((Demande.aj_e == 'nouvelle') | (Demande.aj_e == 'modif'), ((Demande.statut_demande == 'enattente')|(Demande.statut_demande == 'refuse'))).update({'aj_e': 'ancienne'})
    db.session.commit()

def update_aj_column_p():
    Demande.query.filter((Demande.aj_p == 'nouvelle') | (Demande.aj_p == 'modif'), ((Demande.statut_demande == 'enattente')|(Demande.statut_demande == 'refuse'))).update({'aj_p': 'ancienne'})
    db.session.commit()

def update_aj_column_e_a():
    Demande.query.filter((Demande.aj_e == 'nouvelle') | (Demande.aj_e == 'modif'), ((Demande.statut_demande == 'accepte')|(Demande.statut_demande == 'report_demande')|(Demande.statut_demande == 'report_accepte'))).update({'aj_e': 'ancienne'})
    db.session.commit()

def update_aj_column_p_a():
    Demande.query.filter((Demande.aj_p == 'nouvelle') | (Demande.aj_p == 'modif'), ((Demande.statut_demande == 'accepte')|(Demande.statut_demande == 'report_demande')|(Demande.statut_demande == 'report_accepte'))).update({'aj_p': 'ancienne'})
    db.session.commit()

def notif(user_type):
    user_id=session.get("userid")
    user=User.query.filter_by(id=user_id).first()
    if user_type=='professeur':
        nd= Demande.query.filter(Demande.aj_p == "nouvelle",Demande.statut_demande=="enattente", Demande.id_prof ==user.id).count()
        np= Demande.query.filter(or_(Demande.statut_demande == "accepte", Demande.statut_demande == "report_accepte"),Demande.aj_p=="modif", Demande.id_prof == user.id).count()
    elif user_type=='etudiant':
        nd= Demande.query.filter(or_(Demande.aj_e == "nouvelle", Demande.aj_e == "modif"),or_(Demande.statut_demande=="enattente",Demande.statut_demande=="refuse"), Demande.id_etudiant == user.id).count()
        np= Demande.query.filter(or_(Demande.statut_demande == "accepte", Demande.statut_demande == "report_demande"),Demande.aj_e=="modif", Demande.id_etudiant == user.id).count()
    else:
        nd=""
        np=""
    return np,nd
    
def generate_confirmation_code():
    return ''.join(random.choice('0123456789ABCDEF') for i in range(6))

def is_strong_password(password):
    if (
        len(password) >= 8
        and re.search(r'[A-Z]', password)
        and re.search(r'\d', password)
    ):
        return True
    else:
        return False

def update_status():
    current_datetime = datetime.now()
    demandes_to_update = Demande.query.filter(Demande.date_fin < current_datetime).all()
    for demande in demandes_to_update:
        demande.statut_demande="termine"  # Update the status to "termine"
    db.session.commit() 

def delete_unpaid_demandes():
    current_datetime = datetime.now()
    # Query Demande instances with statut_payement="impayer" and date_acc<current_datetime
    demandes_to_delete = Demande.query.filter(
        Demande.statut_payement == "impayer",
        Demande.date_acc < current_datetime
    ).all()
    for demande in demandes_to_delete:
        db.session.delete(demande)  # Delete the demande instance
    db.session.commit()


def delete_expired_demandes():
    current_datetime = datetime.now()
    demandes_to_delete = Demande.query.filter(
        Demande.statut_demande == "enattente",
        Demande.date_acc < current_datetime
    ).all()
    for demande in demandes_to_delete:
        db.session.delete(demande)  # Delete the demande instance
    db.session.commit()

def obtenir_abonnements_et_utilisateurs_meme_groupe(id_abonne):
    abonne = AbonnementLangue.query.filter_by(id_abonne=id_abonne).first()
    id_groupe = abonne.id_groupe
    abonnements_meme_groupe = AbonnementLangue.query.filter_by(id_groupe=id_groupe).all()
    id_abonnes = [abonnement.id_abonne for abonnement in abonnements_meme_groupe]
    utilisateurs_meme_groupe = User.query.filter(User.id.in_(id_abonnes)).all()
    return abonnements_meme_groupe, utilisateurs_meme_groupe


def obtenir_dates_samedis_entre_debut_et_fin(id_abonne):
    abonnement = AbonnementLangue.query.filter_by(id_abonne=id_abonne).first()
    debut = abonnement.datedebut
    fin = abonnement.datefin
    dates_samedis = []
    current_date = debut
    while current_date <= fin:
        if current_date.weekday() == 5:  # 5 correspond à samedi
            dates_samedis.append(current_date+timedelta(hours=16))
        current_date += timedelta(days=1)
    return dates_samedis


def send_email(sender_email, recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    html_content = MIMEText(body, 'html')
    msg.attach(html_content)
    # Paramètres de connexion au serveur SMTP
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = 587
    smtp_username = os.getenv("OUR_MAIL")
    smtp_password = os.getenv("OUR_MAIL_PASSWORD")
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Activation du chiffrement TLS
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        return True
    except Exception as e:
        return False

def generate_pseudo(length=10):
    characters = string.ascii_letters + string.digits
    pseudo = ''.join(random.choice(characters) for _ in range(length))
    return pseudo

def uuidv4():
    choices = '0123456789abcdef'
    uuid = ''.join(random.choice(choices) for _ in range(8)) + '-' + \
           ''.join(random.choice(choices) for _ in range(4)) + '-' + \
           '4' + ''.join(random.choice(choices) for _ in range(3)) + '-' + \
           random.choice('89ab') + ''.join(random.choice(choices) for _ in range(3)) + '-' + \
           ''.join(random.choice(choices) for _ in range(12))
    return uuid


def supprimer_evenements_expirees():
    maintenant = datetime.utcnow()
    evenements_expirees = Evenement.query.filter(Evenement.date < maintenant - timedelta(hours=2)).all()
    
    for evenement in evenements_expirees:
        db.session.delete(evenement)
        db.session.commit()


def noteprof(tag,prof_id):
    prof=Prof.query.filter_by(id=prof_id).first()
    if tag=='negative':
        prof.nefatif=prof.nefatif+1
        db.session.commit()
    elif tag=='positive':
        prof.positif=prof.positif+1
        db.session.commit()
    else:
        a=0
    met= (prof.positif)/(prof.positif+prof.nefatif)
    prof.etoile=math.ceil(met*5)
    db.session.commit()
    

def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

def traduire_vers_anglais(texte):
    translator = Translator()
    traduction = translator.translate(texte, src='auto', dest='en')
    return traduction.text

def traduire_vers_francais(texte):
    translator = Translator()
    traduction = translator.translate(texte, src='auto', dest='fr')
    return traduction.text

def vue():
    nombre_reclamations_non_vues = Reclamation.query.filter_by(vue='non').count()
    return nombre_reclamations_non_vues


def generate_pseudo(length=10):
    characters = string.ascii_letters + string.digits
    pseudo = ''.join(random.choice(characters) for _ in range(length))
    return pseudo


def ajouter_participants_par_email(emails_concatenated, event_id):
    emails_list = emails_concatenated.split(';')
    users = User.query.filter(User.mail.in_(emails_list)).all()
    for user in users:
        participation = Participation(id_evenement=event_id, id_participant=user.id)
        db.session.add(participation)
    db.session.commit()


def get_user_likes(username, all_posts):
    user_likes = []
    for post in all_posts:
        if username.us in post["likeuser"]:
            user_likes.append({"content": post["content"]})
    return user_likes

def get_user_shares(username, all_posts):
    user_shares = []
    for post in all_posts:
        if username.us in post["username"]:
            user_shares.append({"content": post["content"]})
    return user_shares


def get_users_by_nationality(nationality):
    users = User.query.filter_by(nationalite=nationality).all()
    user_names = [f"{user.nom} {user.prenom}" for user in users]
    return user_names


def get_posts_by_usernames(posts, usernames):
    matching_posts = []
    for post in posts:
        if post["username"] in usernames:
            matching_posts.append(post)
            if len(matching_posts) >= 3:
                break

    return matching_posts[:3]

def add_hash_to_tags(tags):
    updated_tags = []
    for tag in tags:
        if not tag.startswith('#'):
            updated_tags.append('#' + tag)
        else:
            updated_tags.append(tag)
    return updated_tags

def suggestion(collection):
    total_posts = collection.count_documents({})
    # Sélectionnez trois indices aléatoires
    random_indices = random.sample(range(total_posts), 3)
    # Récupérez les trois posts aléatoires
    random_posts = [collection.find().skip(index).limit(1)[0] for index in random_indices]
    return random

def get_new_post_id():
    new_uuid = uuid.uuid4()
    new_id = str(new_uuid)[:12]  # Prend les 12 premiers caractères de l'UUID
    return new_id


def get_new_reply_id():
    new_uuid = uuid.uuid4()
    new_reply_id = str(new_uuid).replace("-", "")[:12]  # Supprime les tirets et prend les 12 premiers caractères
    return new_reply_id

def find_item_by_id(posts, item_id):
    for post in posts:
        if post['id'] == item_id:
            return post
        for reply in post['replies']:
            if reply['id'] == item_id:
                return reply
            for subreply in reply['replies']:
                if subreply['id'] == item_id:
                    return subreply
                for subsubreply in subreply['replies']:
                    if subsubreply['id'] == item_id:
                        return subreply
    return None

def calcul_age(birthdate):
    if birthdate:
            birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
            today = datetime.now()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            return age

online_users = []
# Simulation d'une tâche en arrière-plan
def background_task():
      global online_users
      if 'last_activity' in session:  
        last_activity = session.get('last_activity')
      else:
          last_activity =datetime.now()
      last_activity = last_activity.replace(tzinfo=None)
      if datetime.now() - last_activity > timedelta(minutes=1):
        online_users.pop(0)

def get_current_user():
    _current_user=None
    if session.get("userid"):
        user=User.query.get(session.get("userid"))
        if user:
            _current_user=user
    if _current_user is None:
        _current_user=User(
        nom="Visiteur",
        prenom="Anonyme",
        nationalite="Inconnue",
        mail="",
        code="Rabver129G@gh%&B&8bg^gtf",
        pseudo="VisiteurAnonyme",
        date_naiss=datetime.now(),
        ter="non",
        age=0,
        confirmer="non",
        mdp="",
        role="Visiteur",
        photo="static/Profil/unknown.jpg"
    )
    return _current_user

def find_stat(prix):
    if float(prix)==0:
        stat="gratuit"
    else:
        stat="payant"
    return stat

def format_date_bib(date_added):
    return date_added.strftime('%I:%M %p | %b %d')

def create_new_post(new_post_id, user, title, description, ph, realfilename, username, rol, p, stat, formatted_date, discipline, course_type, prix):
    new_post = {
        "id": new_post_id,
        "user_id": user.id,
        "titre": title,
        "description": description,
        "repo": ph,
        "repo_realname": realfilename,
        "username": username,
        "user_star": ['personne'],
        "user_save": ['personne'],
        "profil": user.photo,
        "role": rol,
        "starnumber": 0,
        "image": p,
        "stat": stat,
        "date_added": str(formatted_date),
        "discipline": discipline,
        "type": course_type,
        "prix": prix,
        "downloadnumber": 0
    }
    return new_post

def save_profile_picture(uploaded_files, static_path, subdirectory):
    real_filenames = []
    paths = []

    for profile_picture in uploaded_files:
        if profile_picture:
            real_filenames.append(profile_picture.filename)
            current_date = datetime.now()
            date_string = current_date.strftime("%Y%m%d%H%M%S")
            file_extension = profile_picture.filename.split('.')[-1]
            filename = f"{secure_filename(profile_picture.filename.replace('.', '_'))}_{date_string}.{file_extension}"
            path = os.path.join(static_path, subdirectory)
            if not os.path.exists(path):
                os.makedirs(path)
            file_path = os.path.join(path, filename)
            profile_picture.save(file_path)
            paths.append(os.path.join("static", subdirectory, filename))
        else:
            paths = ""
    return real_filenames, paths


def save_file(file, static_path, subdirectory):
    if file:
        current_date = datetime.now()
        date_string = current_date.strftime("%Y%m%d%H%M%S")
        file_extension = file.filename.split('.')[-1]
        filename = f"{secure_filename(file.filename.replace('.', '_'))}_{date_string}.{file_extension}"
        path = os.path.join(static_path, subdirectory)
        if not os.path.exists(path):
            os.makedirs(path)
        file_path = os.path.join(path, filename)
        file.save(file_path)
        p = os.path.join("static", subdirectory, filename)
    else:
        p = ""
    return p
    
def get_prof_list():
    professeurs = (
        db.session.query(Prof, User)
        .join(User, Prof.id_user_p == User.id)
        .filter(Prof.etoile >= 1)  # Filtrer les professeurs avec au moins 3 étoiles
        .all()
    )
    if professeurs:
        return professeurs
    else:
        return []

def nombre_accepte():
    return Demande.query.filter_by(statut_demande="accepte").count()



def nombre_np():
    if session.get('role') in ["etudiant","professeur"]:
        np,_=notif(session.get("role"))    
        nombre= np_nombre(us=np)
    else:
        nombre= np_nombre(us=0)
    return nombre

def nombre_nd():
    if session.get('role') in ["etudiant","professeur"]:
        _,nd=notif(session.get("role"))
        nombre= nd_nombre(us=nd)
    else:
        nd=0
        nombre= nd_nombre(us=nd)
    return nombre

def nombre_nstud():
    if session.get('role') in ["etudiant","professeur"]:
        n_stud=get_unviewed_actu_count(username)
        nombre= nstud_nombre(us=n_stud)
    else:
        nombre= nstud_nombre(us=0)
    return nombre

def nombre_r():
    if session.get('role') in ["etudiant","professeur"]:
        nr= number_request()
        nombre_req=nb_req(nr=nr)
    else:
        nombre_req=nb_req(nr=0)
    return nombre_req
    
    

def username_fromproxy():
    if session.get('role') in ["etudiant","professeur"]:
        username = user.nom + " " + user.prenom
        name=username_fp(us=username)
    else:
        name=username_fp(us="personne")
    return name


user=LocalProxy(lambda : get_current_user())
current_user=LocalProxy(lambda : get_current_user())
professeurs=LocalProxy(lambda : get_prof_list())
nb=LocalProxy(lambda: nombre_accepte())
np=LocalProxy(lambda: nombre_np())
nd=LocalProxy(lambda: nombre_nd())
username=LocalProxy(lambda: username_fromproxy())
n_stud=LocalProxy(lambda: nombre_nstud())
nr=LocalProxy(lambda: nombre_r())

