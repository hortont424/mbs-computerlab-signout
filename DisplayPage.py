# -*- coding: utf-8 -*-

import datetime
import db

resid = db.getResourceId("Lab Computers")

def generateDaySlots(weekOf, startTime):
    daySlots = ""
    day = datetime.datetime.combine(weekOf, startTime)
    
    for i in range(0, 5):
        entries = db.getEntries(day.date(), startTime, resid)
        quantity = db.getResourceQuantity(resid)
        
        if entries:
            daySlots += "<td class='tFilled'>"
        else:
            daySlots += "<td>"
        
        for entry in entries:
            daySlots += "<div class='entry'>"
            daySlots += db.getTeacher(entry[7])
            daySlots += " (%(q)d)" % {"q": entry[5]}
            daySlots += "</div>"
            quantity -= entry[5]
        
        if entries:
            daySlots += "<div class='leftEntryAfter'>%(q)d left</div>" % {"q": quantity}
        
        daySlots += "</td>"
        
        day = day + datetime.timedelta(days=1)
    
    return daySlots

def generateComputersPage(weekOf):
    nextWeek = lastWeek = datetime.datetime.combine(weekOf, datetime.time(0,0))
    
    nextWeek = nextWeek + datetime.timedelta(weeks=1)
    nextWeekStr = nextWeek.strftime("%Y-%m-%d")
    
    lastWeek = lastWeek - datetime.timedelta(weeks=1)
    lastWeekStr = lastWeek.strftime("%Y-%m-%d")
    
    yield u"""
    <div id="schedule">
        <div id="scheduleHeader">%(last)s Schedule for week of %(week)s %(next)s</div>
        <table id="scheduleTable" cellpadding="0px" cellspacing="4px">
            <tr>
                <td class="tHide"></td>
                <td class="tHeader">Monday</td>
                <td class="tHeader">Tuesday</td>
                <td class="tHeader">Wednesday</td>
                <td class="tHeader">Thursday</td>
                <td class="tHeader">Friday</td>
            </tr>""" % {"week": weekOf.strftime("%B %d, %Y"),
                        "last": "<a href='?date=" + lastWeekStr + u"'>←</a>",
                        "next": "<a href='?date=" + nextWeekStr + u"'>→</a>"}
    
    startTime = datetime.datetime.combine(weekOf, datetime.time(8,45))
    endTime = startTime + datetime.timedelta(minutes=35)
    
    for i in range(0,9):
        yield """
        <tr>
            <td class="tTime">%(startTime)s - %(endTime)s</td>
            %(daySlots)s
        </tr>
        """ % {"startTime": startTime.strftime("%I:%M"),
               "endTime": endTime.strftime("%I:%M"),
               "daySlots": generateDaySlots(weekOf, startTime.time())}
        
        startTime = startTime + datetime.timedelta(minutes=40)
        endTime = endTime + datetime.timedelta(minutes=40)

class DisplayPage:
    def computers(self, date=None):
        yield """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
        <head>
            <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
            <title>MBS Technology Signout</title>
            <link rel="stylesheet" href="/static/style.css" type="text/css" charset="utf-8" />
        </head>
        <body id="tab1">
            <div id="header">
                <a href="/"><img src="/static/signout-logo.png" id="logo"/></a>
                <ul id="tabnav">
                    <li class="tab1"><a href="/computers">Lab Computers</a></li>
                    <li class="tab2"><a href="/laptops">Laptops</a></li>
                    <li class="tab3"><a href="/projectors">Projectors</a></li>
                </ul>
            </div>
            <a href="signout_computers.html"><div id="signoutButton">
                <img src="/static/add.tiff" valign="top"/> Sign out computers
            </div></a>
            <div id="schedule">"""
        
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
        
        yield "".join(list(generateComputersPage(date)))
        
        yield """
            </div>
        </body>
        </html>"""

    computers.exposed = True
    
    index = computers
    index.exposed = True