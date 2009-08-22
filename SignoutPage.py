# -*- coding: utf-8 -*-

import datetime
import db
import utils
from Authenticate import *

def generateSignoutDaySlots(weekOf, startTime, type):
    daySlots = ""
    day = datetime.datetime.combine(weekOf, startTime)
    currentUser = authGetID()
    
    for i in range(0, 5):
        entries = db.getEntries(day.date(), startTime, type)
        quantity = db.getResourceQuantity(type)
        currentUserInBox = 0
        
        for entry in entries:
            if db.getTeacherName(entry[7]) == currentUser:
                currentUserInBox = entry[5]
            quantity -= entry[5]
        
        if entries:
            if currentUserInBox:
                daySlots += "<td class='tFilled tSignout ts' "
            else:
                daySlots += "<td class='tFilled ts' "
        else:
            daySlots += "<td class='ts' "
        
        daySlots += " onclick='signout(\"" + currentUser + "\"," + str(currentUserInBox) + "," + str(quantity) + ", \"" + day.strftime("%Y-%m-%d") + "\",\"" + startTime.strftime("%I:%M") + "\")'>"
        
        for entry in entries:
            if db.getTeacherName(entry[7]) == currentUser:
                daySlots += "<div class='signoutEntry'>"
            else:
                daySlots += "<div class='entry'>"
            daySlots += db.getTeacherName(entry[7])
            daySlots += " (%(q)d)" % {"q": entry[5]}
            daySlots += "</div>"
        
        if entries:
            daySlots += "<div class='leftEntryAfter'>%(q)d left</div>" % {"q": quantity}
        
        daySlots += "</td>"
        
        day = day + datetime.timedelta(days=1)
    
    return daySlots

def generateSignoutSchedulePage(weekOf,type):
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
    endTime = startTime + datetime.timedelta(minutes=db.getResourceDuration(type))
    
    for i in range(0,db.getResourceSlotCount(type)):
        yield """
        <tr>
            <td class="tTime">%(startTime)s - %(endTime)s</td>
            %(daySlots)s
        </tr>
        """ % {"startTime": startTime.strftime("%I:%M"),
               "endTime": endTime.strftime("%I:%M"),
               "daySlots": generateSignoutDaySlots(weekOf, startTime.time(), type)}
        
        startTime = startTime + datetime.timedelta(minutes=db.getResourceDuration(type)+5)
        endTime = endTime + datetime.timedelta(minutes=db.getResourceDuration(type)+5)

def generateTeachersDropdown():
    yield "<select name='teacher' onchange='changedNameSelection()' id='teacher'>"
    yield "<option></option>"
    yield "<optgroup label='3rd Grade'>"
    
    for t in ("Barnes", "Bonfigli", "Eaton", "Fitzpatrick", "Jamison", "Miles", "Rayner", "Schroeder"):
        yield "<option name='%(name)s'>%(name)s</option>" % { "name": t }
    
    yield "</optgroup><optgroup label='4th Grade'>"
    
    for t in ("Boucher", "Cheney", "Chittenden", "Gallas", "Hunt", "Kilmer", "Longchamp"):
        yield "<option name='%(name)s'>%(name)s</option>" % { "name": t }
    
    yield "</optgroup><optgroup label='5th Grade'>"
    
    for t in ("Bryer", "Buswell", "DiGrande", "Galati", "Powsner", "Renner", "Rogers", "Winchester"):
        yield "<option name='%(name)s'>%(name)s</option>" % { "name": t }
    
    yield "</optgroup><optgroup label='Misc.'><option name='Special Ed.'>Special Ed.</option><option name='Other'>Other</option></optgroup></select>"

class signoutPage:
    def __init__(self, t):
        self.type = t
    
    def index(self, date=None):
        date = utils.normalizeDate(date)
        
        yield """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
        <head>
            <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
            <title>MBS Technology Signout</title>
            <link rel="stylesheet" href="/static/style.css" type="text/css" charset="utf-8" />
            <style type="text/css">
            #header
            {
                border-bottom: 1px solid #666;
            }

            #logo
            {
                padding: 20px 15px 20px 15px;
            }
            
            #signinForm
            {
                text-align: left;
            }
            
            td
            {
                border: 0px;
            }
            </style>
            <script src="/static/jquery.min.js"></script>
            <script src="/static/jquery.md5.js"></script>
            <script>
            function updateOtherField()
            {
                var ot = $("#otherText");
                
                if($("#teacher")[0].value == "Other")
                    ot.css("display", "table-row");
                else
                    ot.css("display", "none");
            }
            
            function updateContinuable()
            {
                var signout = $("#signoutButton");
                var teacher = $("#teacher")[0].value;
                var ot = $("#otherText")[0].value;
                var password = $("#passwd")[0].value;
                
                if(((teacher == "Other" && ot != "") ||
                    (teacher != "Other" && teacher != "")) &&
                   ($.md5(password) == "%(pw)s"))
                    signout.css("display", "block");
                else
                    signout.css("display", "none");
            }

            function changedNameSelection()
            {
                updateOtherField();
                updateContinuable();
            }
            
            function changedPassword()
            {
                updateContinuable();
            }
            </script>
        </head>
        <body>
            <div id="header">
                <a href="/"><img src="/static/signout-logo.png" id="logo"/></a>
            </div>
            <div id="headerButton">
                Signing out %(slug)s
            </div>
            <form id="signinForm" name="signinForm" action="choose" method="post">
                <div class="headerButtonSmall" style="text-align: left;">
                    <table border="0px" cellpadding="6px" width="100%%">
                    <tr>
                        <td style="text-align: right;"><b>Name:</b></td>
                        <td>%(teachers)s</td>
                    </tr>
                    <tr id="otherText" style="display: none;">
                        <td style="text-align: right;"><b>Other:</b></td>
                        <td><input type="text" name="other"/></td>
                    </tr>
                    <tr>
                        <td style="text-align: right;"><b>Password:</b></td>
                        <td><input type="password" id="passwd" name="passwd" onchange='changedPassword()' onkeyup='changedPassword()' /></td>
                    </tr>
                    </table>
                </div>
            </form>
            <a href="javascript:document.signinForm.submit()"><div id="signoutButton" style="display: none;">
                <img src="/static/play.png" valign="top"/> Continue to time slot selection
            </div></a>
        </body>
        </html>
            """ % {
                "id": self.type,
                "name": db.getResourceName(self.type),
                "slug": db.getResourceSlug(self.type),
                "q": db.getResourceQuantity(self.type),
                "teachers": "".join(list(generateTeachersDropdown())),
                "pw": password_hash }

    index.exposed = True
        
    def choose(self, date=None, teacher=None, passwd=None, other=None):
        date = utils.normalizeDate(date)
        
        if (passwd == None or teacher == None) and not authGetLoggedIn():
            yield """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
            Missing data! Go back and try again...</html>"""
            return
        
        if (passwd != None and teacher != None) and not authLogin(teacher, passwd):
            yield """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
            Wrong password! Go back and try again...</html>"""
            return
        
        if not authGetLoggedIn():
            yield """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
            Something broke! Go back and try again...</html>"""
            return
        
        teacher = authGetID()
        
        yield """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
        <head>
            <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
            <title>MBS Technology Signout</title>
            <link rel="stylesheet" href="/static/style.css" type="text/css" charset="utf-8" />
            <style type="text/css">
            #header
            {
                border-bottom: 1px solid #666;
            }

            #logo
            {
                padding: 20px 15px 20px 15px;
            }
            </style>
            <script src="/static/jquery.min.js"></script>
            <script>
            function signout(name, currentQ, leftQ, date, time)
            {
                var moreStr = "";
                
                if(currentQ != 0)
                    moreStr = "(" + leftQ + " more) ";
                
                res = prompt("You currently have " + currentQ +
                             " %(slug)s signed out for " + time + " on " + date + ".\\n\\n" +
                             "You can sign out up to " + (currentQ + leftQ) + " %(slug)s " + moreStr + "in that slot:\\n", currentQ);
                
                if(res == null)
                    return;
                
                if(isNaN(res))
                {
                    alert("'" + res + "' is not a number between 0 and (currentQ + leftQ). Please try again.");
                    signout(name, currentQ, leftQ, date, time);
                    return;
                }
                
                if(res > (currentQ + leftQ))
                {
                    alert("You requested " + (res - currentQ) + " additional %(slug)s. However, there are only " + leftQ + " available. Please try again.");
                    signout(name, currentQ, leftQ, date, time);
                    return;
                }
                
                alert("got " + res)
            }
            </script>
        </head>
        <body id="tab%(id)d">
            <div id="header">
                <a href="/"><img src="/static/signout-logo.png" id="logo"/></a>
            </div>
            <div id="headerButton">
                Signing out %(slug)s<br/><small><small>as "%(name)s"</small></small>
                <div id="headerButtonSub">
                    The number of remaining seats in each time slot is indicated below. Click on a time slot to change the number of seats <em>you</em> need. When you are done, click the button below to continue.<br/><br/>
                    Each slot has %(q)d %(slug)s available unless otherwise noted.
                </div>
            </div>
            <a href="#"><div id="signoutButton">
                <img src="/static/play.png" valign="top"/> Done
            </div></a>
            <div id="schedule">""" % {
                "id": self.type,
                "name": db.getResourceName(self.type),
                "slug": db.getResourceSlug(self.type),
                "q": db.getResourceQuantity(self.type),
                "name": teacher }

        yield "".join(list(generateSignoutSchedulePage(date,self.type)))

        yield """
            </div>
        </body>
        </html>"""
    choose.exposed = True
