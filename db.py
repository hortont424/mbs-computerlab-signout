import sqlite3
from utils import *

def loadData(c):
    c.executescript(readFile("sql.txt"))
    c.execute("insert into resources values (?,?,?,?)", (None,"Computers","",25))
    c.execute("insert into resources values (?,?,?,?)", (None,"Laptops","",20))
    c.execute("insert into resources values (?,?,?,?)", (None,"Projectors","",2))
    
    c.execute("insert into teachers values (?,?,?)", (None,"Eaton",""))
    c.execute("insert into teachers values (?,?,?)", (None,"Cheney",""))
    c.execute("insert into teachers values (?,?,?)", (None,"DiGrande",""))
    c.execute("insert into teachers values (?,?,?)", (None,"Powsner",""))
    c.execute("insert into teachers values (?,?,?)", (None,"Kilmer",""))
    c.execute("insert into teachers values (?,?,?)", (None,"Fitzpatrick",""))
    
    c.execute('select id from resources where name=?', ("Computers",))
    c_id = c.fetchone()[0]
    c.execute('select id from teachers where name=?', ("Cheney",))
    e_id = c.fetchone()[0]
    c.execute("insert into entries values (?,?,?,?,?,?,?,?)",
        (None, "2009-02-05", "8:45", "9:20", "", 5, c_id, e_id))

db = sqlite3.connect(':memory:')
c = db.cursor()
loadData(c)