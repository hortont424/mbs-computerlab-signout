# -*- coding: utf-8 -*-

import datetime
import sqlite3
from utils import *

db = None

def getAllEntries(type):
    c = connect()
    c.execute("select * from entries where signee_id=?", (type,))
    return c.fetchall()

def getEntries(day,time,type):
    c = connect()
    c.execute("select * from entries where day=? and start_time=? and signee_id=?",
              (day.strftime("%Y-%m-%d"), time.strftime("%I:%M"), type))
    return c.fetchall()

def setEntry(day,time,type,t_id,num):
    db = sqlite3.connect('signout.db')
    c = db.cursor()
    c.execute("delete from entries where day=? and start_time=? and signee_id=? and signer_id=?",
              (day, time, type, t_id))
    if int(num) > 0:
        c.execute("insert into entries values (?,?,?,?,?,?,?,?)",
                  (None, day, time, time, "", num, type, t_id))
    db.commit()

def getTeachers():
    c = connect()
    c.execute("select * from teachers")
    return c.fetchall()

def getTeacherName(t_id):
    c = connect()
    c.execute("select name from teachers where id=?", (t_id,))
    return c.fetchone()[0]

def getTeacherId(t):
    c = connect()
    c.execute("select id from teachers where name=?", (t,))
    return c.fetchone()[0]

def getResources():
    c = connect()
    c.execute("select * from resources")
    return c.fetchall()

def getResourceId(res):
    c = connect()
    c.execute("select id from resources where name=?", (res,))
    return c.fetchone()[0]

def getResourceName(r_id):
    c = connect()
    c.execute("select name from resources where id=?", (r_id,))
    return c.fetchone()[0]

def getResourceSlug(r_id):
    c = connect()
    c.execute("select slug from resources where id=?", (r_id,))
    return c.fetchone()[0]

def getResourceSlugN(r_id):
    c = connect()
    c.execute("select slug from resources where id=?", (r_id,))
    sl = c.fetchone()[0]
    if sl == "laptoplab":
        sl = "laptop lab"
    return sl


def getResourceQuantity(r_id):
    c = connect()
    c.execute("select quantity from resources where id=?", (r_id,))
    return c.fetchone()[0]

def getResourceDuration(r_id):
    c = connect()
    c.execute("select duration from resources where id=?", (r_id,))
    return c.fetchone()[0]

def getResourceSlotCount(r_id):
    c = connect()
    c.execute("select slot_count from resources where id=?", (r_id,))
    return c.fetchone()[0]

def loadData(c):
    c.executescript(readFile("sql.txt"))
    c.execute("insert into resources values (?,?,?,?,?,?,?)", (1,"Lab Computers","computers","",24,35,9))
    c.execute("insert into resources values (?,?,?,?,?,?,?)", (2,"Laptop Lab","laptoplab","",1,185,2))
    c.execute("insert into resources values (?,?,?,?,?,?,?)", (3,"Projector","projector","",1,185,2))
    
    for t in ("Barnes", "Bonfigli", "Eaton", "Fitzpatrick", "Jamison", "Miles", "Rayner", "Schroeder"):
        c.execute("insert into teachers values (?,?,?)", (None,t,""))
    for t in ("Boucher", "Cheney", "Chittenden", "Gallas", "Hunt", "Kilmer", "Longchamp"):
        c.execute("insert into teachers values (?,?,?)", (None,t,""))
    for t in ("Bryer", "Buswell", "DiGrande", "Galati", "Powsner", "Renner", "Rogers", "Winchester"):
        c.execute("insert into teachers values (?,?,?)", (None,t,""))
    for t in ("Special Ed.", "Other"):
        c.execute("insert into teachers values (?,?,?)", (None,t,""))

def connect():
    db = sqlite3.connect('signout.db')
    c = db.cursor()
    return c

#db = sqlite3.connect('signout.db')
#c = db.cursor()
#loadData(c)
#db.commit()
