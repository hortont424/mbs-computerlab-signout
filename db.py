# -*- coding: utf-8 -*-

import datetime
import sqlite3
from utils import *

def getEntries(day,time,type):
    c = connect()
    c.execute("select * from entries where day=? and start_time=? and signee_id=?",
              (day.strftime("%Y-%m-%d"), time.strftime("%I:%M"), type))
    return c.fetchall()

def getTeacher(t_id):
    c = connect()
    c.execute("select name from teachers where id=?", (t_id,))
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

def loadData(c):
    c.executescript(readFile("sql.txt"))
    c.execute("insert into resources values (?,?,?,?,?)", (1,"Lab Computers","computers","",25))
    c.execute("insert into resources values (?,?,?,?,?)", (2,"Laptops","laptops","",20))
    c.execute("insert into resources values (?,?,?,?,?)", (3,"Projectors","projectors","",2))
    
    c.execute("insert into teachers values (?,?,?)", (None,"Eaton",""))
    c.execute("insert into teachers values (?,?,?)", (None,"Cheney",""))
    c.execute("insert into teachers values (?,?,?)", (None,"DiGrande",""))
    c.execute("insert into teachers values (?,?,?)", (None,"Powsner",""))
    c.execute("insert into teachers values (?,?,?)", (None,"Kilmer",""))
    c.execute("insert into teachers values (?,?,?)", (None,"Fitzpatrick",""))
    
    c_id = 1
    c.execute('select id from teachers where name=?', ("Cheney",))
    cheney_id = c.fetchone()[0]
    c.execute('select id from teachers where name=?', ("Eaton",))
    eaton_id = c.fetchone()[0]
    c.execute("insert into entries values (?,?,?,?,?,?,?,?)",
        (None, "2009-08-05", "08:45", "09:20", "", 5, c_id, eaton_id))
    c.execute("insert into entries values (?,?,?,?,?,?,?,?)",
        (None, "2009-08-06", "08:45", "09:20", "", 5, c_id, eaton_id))
    c.execute("insert into entries values (?,?,?,?,?,?,?,?)",
        (None, "2009-08-07", "08:45", "09:20", "", 5, c_id, eaton_id))
    c.execute("insert into entries values (?,?,?,?,?,?,?,?)",
        (None, "2009-08-05", "09:25", "10:00", "", 15, c_id, cheney_id))
    c.execute("insert into entries values (?,?,?,?,?,?,?,?)",
        (None, "2009-08-05", "09:25", "10:00", "", 5, c_id, eaton_id))

def connect():
    db = sqlite3.connect(':memory:')
    c = db.cursor()
    loadData(c)
    return c