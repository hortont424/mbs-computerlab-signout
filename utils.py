# -*- coding: utf-8 -*-

import codecs
import datetime
from auth import *

def readFile(fn):
    fileHandle = codecs.open(fn, encoding='utf-8')
    fileContents = fileHandle.read()
    fileHandle.close()
    return fileContents

def normalizeDate(date):
    if date is None:
        date = authGetDate()
        if date is None:
            date = datetime.date.today()
    else:
        try:
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        except:
            date = datetime.date.today()

    if date.weekday():
        tmpdate = datetime.datetime.combine(date, datetime.time(0,0))
        tmpdate = tmpdate - datetime.timedelta(days=date.weekday())
        date = tmpdate
    
    authSetDate(date)
    
    return date

def generateTabs(append):
    t = "<ul id='tabnav'>"

    for res in db.getResources():
        t += "<li class='tab%(id)d'><a href='/%(slug)s%(app)s'>%(name)s</a></li>" % {
            "id": res[0], "name": res[1], "slug": res[2], "app": append}

    t += "</ul>"
    return t