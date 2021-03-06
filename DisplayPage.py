# -*- coding: utf-8 -*-

import datetime
import db
from utils import *
from auth import *

def generateDaySlots(weekOf, startTime, type):
    daySlots = ""
    day = datetime.datetime.combine(weekOf, startTime)
    
    for i in range(0, 5):
        entries = db.getEntries(day.date(), startTime, type)
        quantity = db.getResourceQuantity(type)
        
        if entries:
            daySlots += "<td class='tFilled'>"
        else:
            daySlots += "<td class='tBordered'>&nbsp;"
        
        for entry in entries:
            daySlots += "<div class='entry'>"
            daySlots += db.getTeacherName(entry[7])
            daySlots += " (%(q)d)" % {"q": entry[5]}
            daySlots += "</div>"
            quantity -= entry[5]
        
        if entries:
            daySlots += "<div class='leftEntryAfter'>%(q)d left</div>" % {"q": quantity}
        
        daySlots += "</td>"
        
        day = day + datetime.timedelta(days=1)
    
    return daySlots

def generateSchedulePage(weekOf,type):
    nextWeek = lastWeek = datetime.datetime.combine(weekOf, datetime.time(0,0))
    
    nextWeek = nextWeek + datetime.timedelta(weeks=1)
    nextWeekStr = nextWeek.strftime("%Y-%m-%d")
    
    lastWeek = lastWeek - datetime.timedelta(weeks=1)
    lastWeekStr = lastWeek.strftime("%Y-%m-%d")
    
    yield u"""
    <div id="schedule">
        <div id="scheduleHeader"><div class="smallbutton" onclick="window.location='%(last)s'"><a href="%(last)s">←</a></div> <span id='schedTitle'>Schedule for week of %(week)s</span> <div class="smallbutton" onclick="window.location='%(next)s'"><a href="%(next)s">→</a></div></div>
        <br />
        <table id="scheduleTable" cellpadding="0px" cellspacing="4px">
            <tr>
                <td class="tHide"></td>
                <td class="tHeader">Monday</td>
                <td class="tHeader">Tuesday</td>
                <td class="tHeader">Wednesday</td>
                <td class="tHeader">Thursday</td>
                <td class="tHeader">Friday</td>
            </tr>""" % {"week": weekOf.strftime("%B %d, %Y"),
                        "last": "?date=" + lastWeekStr,
                        "next": "?date=" + nextWeekStr}
    
    startTime = datetime.datetime.combine(weekOf, datetime.time(8,45))
    endTime = startTime + datetime.timedelta(minutes=db.getResourceDuration(type))
    
    for i in range(0,db.getResourceSlotCount(type)):
        yield """
        <tr>
            <td class="tTime">%(startTime)s - %(endTime)s</td>
            %(daySlots)s
        </tr>
        """ % {"startTime": startTime.strftime("%I:%M"),
               "endTime": endTime.strftime("%I:%M"),
               "daySlots": generateDaySlots(weekOf, startTime.time(), type)}
        
        startTime = startTime + datetime.timedelta(minutes=db.getResourceDuration(type)+5)
        endTime = endTime + datetime.timedelta(minutes=db.getResourceDuration(type)+5)

class tabbedSchedulePage:
    def __init__(self, t):
        self.type = t
        
    def index(self, date=None):
        date = normalizeDate(date)
        
        src = """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
        <head>
            <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
            <title>MBS Technology Signout</title>
            <link rel="stylesheet" href="/static/style.css" type="text/css" charset="utf-8" />
        </head>
        <body id="tab%(id)d">
            <div id="header">
                <img src="/static/signout-logo.png" id="logo"/>
                %(tabs)s
            </div>
            <a href="/%(slug)s/signout"><div id="signoutButton">
                <img src="/static/add.png" valign="top"/> Sign out %(slugN)s
            </div></a>
            <div id="schedule">""" % {
                "id": self.type,
                "name": db.getResourceName(self.type),
                "slug": db.getResourceSlug(self.type),
                "slugN": db.getResourceSlugN(self.type),
                "tabs": generateTabs(""),
                "date": date }

        src += "".join(list(generateSchedulePage(date,self.type)))

        src += """
            </div>
        </body>
        </html>"""
        
        return src
    index.exposed = True
