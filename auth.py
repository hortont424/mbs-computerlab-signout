# -*- coding: utf-8 -*-

import datetime
import db
import utils
import cherrypy

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

def authLogin(id):
    cherrypy.session["id"] = id
    cherrypy.session["loggedIn"] = id
    return True

def authLogout():
    cherrypy.session["id"] = None
    cherrypy.session["loggedIn"] = None

def authGetLoggedIn():
    if authGetID() is not None and cherrypy.session.get("loggedIn") is not None:
        return True
    else:
        return False