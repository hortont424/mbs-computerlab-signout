# -*- coding: utf-8 -*-

import datetime
import sqlite3
from utils import *

db = None

def getEntries(day,time,type):
    c = connect()
    c.execute("select * from entries where day=? and start_time=? and signee_id=?",
              (day.strftime("%Y-%m-%d"), time.strftime("%I:%M"), type))
    return c.fetchall()

def setEntry(day,time,type,t_id,num):
    db = sqlite3.connect('signout.db')
    c = db.cursor()
    print "deleting"
    print day
    print time
    print type
    print t_id
    print c.execute("delete from entries where day=? and start_time=? and signee_id=? and signer_id=?",
              (day, time, type, t_id)).rowcount
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
    c.execute("insert into resources values (?,?,?,?,?,?,?)", (1,"Lab Computers","computers","",25,35,9))
    c.execute("insert into resources values (?,?,?,?,?,?,?)", (2,"Laptops","laptops","",20,185,2))
    c.execute("insert into resources values (?,?,?,?,?,?,?)", (3,"Projectors","projectors","",2,185,2))
    
    c.execute("insert into teachers values (?,?,?)", (None,"Eaton",""))
    c.execute("insert into teachers values (?,?,?)", (None,"Cheney",""))
    c.execute("insert into teachers values (?,?,?)", (None,"DiGrande",""))
    c.execute("insert into teachers values (?,?,?)", (None,"Powsner",""))
    c.execute("insert into teachers values (?,?,?)", (None,"Kilmer",""))
    c.execute("insert into teachers values (?,?,?)", (None,"Fitzpatrick",""))
    
    c_id = 1
    cheney_id = 3
    eaton_id = 4
    c.execute("insert into entries values (?,?,?,?,?,?,?,?)",
        (None, "2009-08-18", "08:45", "09:20", "", 5, c_id, eaton_id))
    c.execute("insert into entries values (?,?,?,?,?,?,?,?)",
        (None, "2009-08-19", "08:45", "09:20", "", 5, c_id, eaton_id))
    c.execute("insert into entries values (?,?,?,?,?,?,?,?)",
        (None, "2009-08-20", "08:45", "09:20", "", 5, c_id, eaton_id))
    c.execute("insert into entries values (?,?,?,?,?,?,?,?)",
        (None, "2009-08-18", "09:25", "10:00", "", 15, c_id, cheney_id))
    c.execute("insert into entries values (?,?,?,?,?,?,?,?)",
        (None, "2009-08-18", "09:25", "10:00", "", 5, c_id, eaton_id))

def connect():
    db = sqlite3.connect('signout.db')
    c = db.cursor()
    return c

#db = sqlite3.connect('signout.db')
#c = db.cursor()
#loadData(c)
#db.commit()
