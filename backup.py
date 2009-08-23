# -*- coding: utf-8 -*-

import datetime
import db
import utils
import cherrypy

computers_id = db.getResourceId("Lab Computers")
laptops_id = db.getResourceId("Laptop Lab")
projectors_id = db.getResourceId("Projector")

def backupGetDateRange(type):
    entries = db.getAllEntries(type)
    dates = [datetime.datetime.strptime(x[1], "%Y-%m-%d").date() for x in entries]
    return (min(dates), max(dates))

#def backupTimeslot(type, weekOf, startTime):

#def backupWeekOf(type, weekOf):

def backupType(type):
    range = backupGetDateRange(type)
    week = range[0]

    if week.weekday():
        tmpdate = datetime.datetime.combine(week, datetime.time(0,0))
        tmpdate = tmpdate - datetime.timedelta(days=week.weekday())
        week = tmpdate.date()

    while(week < range[1]):
        week = datetime.datetime.combine(week, datetime.time(0,0))
        print week.strftime("%Y-%m-%d")
        week = (week + datetime.timedelta(weeks=1)).date()

print backupType(computers_id)