# -*- coding: utf-8 -*-

import datetime
import db
import utils
import cherrypy
import os
import codecs
import sys

computers_id = db.getResourceId("Lab Computers")
laptops_id = db.getResourceId("Laptop Lab")
projectors_id = db.getResourceId("Projector")

def backupGetDateRange(type):
    entries = db.getAllEntries(type)
    dates = [datetime.datetime.strptime(x[1], "%Y-%m-%d").date() for x in entries]
    if not dates:
        return (None, None)
    else:
        return (min(dates), max(dates))

def backupTimeslot(type, weekOf, startTime):
    tstr = startTime.strftime("%I:%M") + ","
    day = datetime.datetime.combine(weekOf, startTime)
    
    for i in range(0, 5):
        tstr += "\""
        entries = db.getEntries(day.date(), startTime, type)
        for entry in entries:
            tstr += db.getTeacherName(entry[7]) + " (" + str(entry[5]) + ")\n"
        day = day + datetime.timedelta(days=1)
        tstr += "\""
        if i != 4:
            tstr += ","
    
    tstr += "\n"
    
    return tstr

def backupWeekOf(type, weekOf):
    startTime = datetime.datetime.combine(weekOf, datetime.time(8,45))
    endTime = startTime + datetime.timedelta(minutes=db.getResourceDuration(type))
    
    weekstr = db.getResourceName(type) + " for the week of " + weekOf.strftime("%Y-%m-%d") + "\n\n"
    
    weekstr += ",M,T,W,Th,F\n"
    
    for i in range(0,db.getResourceSlotCount(type)):
        weekstr += backupTimeslot(type, weekOf.date(), startTime.time())
        startTime = startTime + datetime.timedelta(minutes=db.getResourceDuration(type)+5)
        endTime = endTime + datetime.timedelta(minutes=db.getResourceDuration(type)+5)
    
    return weekstr

def backupType(type):
    range = backupGetDateRange(type)
    week = range[0]
    
    if week == None:
        return

    if week.weekday():
        tmpdate = datetime.datetime.combine(week, datetime.time(0,0))
        tmpdate = tmpdate - datetime.timedelta(days=week.weekday())
        week = tmpdate.date()

    mydir = os.path.join("backup", db.getResourceSlug(type))
    if not os.path.exists(mydir):
        os.makedirs(mydir)

    while(week < range[1]):
        week = datetime.datetime.combine(week, datetime.time(0,0))
        filename = os.path.join(mydir, week.strftime("%Y-%m-%d") + ".csv")
        data = backupWeekOf(type, week)
        dataFile = codecs.open(filename, encoding='utf-8', mode='w+')
        dataFile.write(data)
        dataFile.close()
        week = (week + datetime.timedelta(weeks=1)).date()

backupType(computers_id)
backupType(laptops_id)
backupType(projectors_id)