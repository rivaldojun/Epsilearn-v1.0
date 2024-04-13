import uuid
import json
from flask import render_template,jsonify,redirect,url_for,request,session,flash,Blueprint
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask_socketio import SocketIO, emit, send,join_room,disconnect
from App.Models.models import *
from App.Controllers.fonction import *

AdminBp = Blueprint("Admin",__name__,template_folder="templates")




