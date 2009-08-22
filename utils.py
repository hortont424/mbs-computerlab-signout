# -*- coding: utf-8 -*-

import codecs
import datetime
from Authenticate import *

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