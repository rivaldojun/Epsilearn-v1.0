from flask import session,redirect,url_for, request
from functools import wraps

def student_login_required(f):
    @wraps(f)
    def _student_login_required(*args,**kwargs):
        if "role" in session and session.get("role")=="etudiant":
            return f(*args,**kwargs)
        else:
            session['next_url'] =request.url
            print(request.url)
            return redirect(url_for('Main.connexion'))
    return _student_login_required

def login_required(f):
    @wraps(f)
    def _login_required(*args,**kwargs):
        if "role" in session:
            return f(*args,**kwargs)
        else:
            session['next_url'] =request.url
            print(request.url)
            return redirect(url_for('Main.connexion'))
    return _login_required

def prof_login_required(f):
    @wraps(f)
    def _prof_login_required(*args,**kwargs):
        if "role" in session and session.get("role")=="professeur":
            return f(*args,**kwargs)
        else:
            session['next_url'] = request.url
            print(request.url)
            return redirect(url_for('Main.connexion'))
    return _prof_login_required

def student_prof_login_required(f):
    @wraps(f)
    def _student_prof_login_required(*args,**kwargs):
        if "role" in session and session.get('role') in ["professeur", "etudiant"]:
            return f(*args,**kwargs)
        else:
            session['next_url'] = request.url
            print(request.url)
            return redirect(url_for('Main.connexion'))
    return _student_prof_login_required

##ACCES INTERDIT

def prof_login_required_AI(f):
    @wraps(f)
    def _prof_login_required_AI(*args,**kwargs):
        if "role" not in session :
            session['next_url'] = request.url
            print(request.url)
            return redirect(url_for('Main.connexion'))
        elif session.get("role")!="professeur":
            session['next_url'] = request.url
            print(request.url)
            return redirect(url_for('Main.acces_interdit'))
        else:
            return f(*args,**kwargs)
    return _prof_login_required_AI

def student_login_required_AI(f):
    @wraps(f)
    def _student_login_required_AI(*args,**kwargs):
        if "role" not in session :
            session['next_url'] = request.url
            print(request.url)
            return redirect(url_for('Main.connexion'))
        elif session.get("role")!="etudiant":
            session['next_url'] = request.url
            print(request.url)
            return redirect(url_for('Main.acces_interdit'))
        else:
            return f(*args,**kwargs)
    return _student_login_required_AI

def student_prof_login_required_AI(f):
    @wraps(f)
    def _student_prof_login_required_AI(*args,**kwargs):
        if "role" not in session :
            session['next_url'] = request.url
            return redirect(url_for('Main.connexion'))
        elif session.get('role') not in ["professeur", "etudiant"]:
            session['next_url'] = request.url
            print(request.url)
            return redirect(url_for('Main.acces_interdit'))
        else:
            return f(*args,**kwargs)
    return _student_prof_login_required_AI
