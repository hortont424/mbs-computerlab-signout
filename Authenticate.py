# -*- coding: utf-8 -*-

import datetime
import db
import hashlib
import utils
import cherrypy

password_hash = "1169352c31919b66930b14c0375cd34f"

def authSetDate(date):
    cherrypy.session["date"] = date

def authGetDate():
    try:
        return cherrypy.session.get("date")
    except:
        return None

def authSetID(id):
    cherrypy.session["id"] = id

def authGetID():
    try:
        return cherrypy.session.get("id")
    except:
        return None

def authLogin(id,passwd):
    m = hashlib.md5()
    m.update(passwd);
    if(m.hexdigest() != password_hash):
        return False
    cherrypy.session["id"] = id
    cherrypy.session["loggedIn"] = passwd
    return True

def authLogout():
    cherrypy.session["id"] = None
    cherrypy.session["loggedIn"] = None

def authGetLoggedIn():
    if authGetID() is not None and cherrypy.session.get("loggedIn") is not None:
        return True
    else:
        return False