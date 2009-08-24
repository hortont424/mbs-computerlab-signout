# -*- coding: utf-8 -*-

import datetime
import db
from utils import *
from auth import *

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
        
        if not entries:
            daySlots += "&nbsp;"

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
               "daySlots": generateSignoutDaySlots(weekOf, startTime.time(), type)}
        
        startTime = startTime + datetime.timedelta(minutes=db.getResourceDuration(type)+5)
        endTime = endTime + datetime.timedelta(minutes=db.getResourceDuration(type)+5)

def generateTeachersDropdown():
    yield "<select name='teacher' onchange='changedNameSelection()' id='teacher'>"
    yield "<option></option>"
    yield "<optgroup label='3rd Grade'>"
    
    for t in db.getTeachersOfGrade(3):
        yield "<option name='%(name)s'>%(name)s</option>" % { "name": t }
    
    yield "</optgroup><optgroup label='4th Grade'>"
    
    for t in db.getTeachersOfGrade(4):
        yield "<option name='%(name)s'>%(name)s</option>" % { "name": t }
    
    yield "</optgroup><optgroup label='5th Grade'>"
    
    for t in db.getTeachersOfGrade(5):
        yield "<option name='%(name)s'>%(name)s</option>" % { "name": t }
    
    yield "</optgroup><optgroup label='Misc.'>"
    
    for t in db.getTeachersOfGrade(0):
        yield "<option name='%(name)s'>%(name)s</option>" % { "name": t }
    
    yield "</optgroup></select>"

class signoutPage:
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

                for (var i = 0, l = $("#teacher")[0].length; i < l; ++i)
                {
                    if ((o = $("#teacher")[0].options[i]).selected)
                        teacher = o.text;
                }

                if(((teacher == "Other" && ot != "") ||
                    (teacher != "Other" && teacher != "")))
                    signout.css("display", "block");
                else
                    signout.css("display", "none");
            }

            function changedNameSelection()
            {
                updateOtherField();
                updateContinuable();
            }
            </script>
        </head>
        <body>
            <div id="header">
                <a href="/"><img src="/static/signout-logo.png" id="logo"/></a>
            </div>
            <div id="headerButton">
                Signing out %(slugN)s
            </div>
            <form id="signinForm" name="signinForm" action="choose" method="post">
                <div class="headerButtonSmall" style="text-align: left;">
                    <table border="0px" cellpadding="6px" width="100%%">
                    <tr>
                        <td style="text-align: right;" width="50%%"><b>Name:</b></td>
                        <td width="50%%">%(teachers)s</td>
                    </tr>
                    <tr id="otherText" style="display: none;">
                        <td style="text-align: right;"><b>Other:</b></td>
                        <td><input type="text" name="other"/></td>
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
                "slugN": db.getResourceSlugN(self.type),
                "q": db.getResourceQuantity(self.type),
                "teachers": "".join(list(generateTeachersDropdown())) }
        return src

    index.exposed = True
        
    def choose(self, date=None, teacher=None, other=None, time=None, signout=None, day=None, logout=None):
        date = normalizeDate(date)
        
        if logout is not None:
            authLogout()
            print "logout"
            return """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
            <script>window.location='/'</script></html>"""
        
        if (teacher == None) and not authGetLoggedIn():
            print "not logged in, missing data"
            return """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
            <script>window.location='/'</script></html>"""
        
        if (teacher != None) and not authLogin(teacher):
            return """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
            Wrong password! Go back and try again...</html>"""
        
        if not authGetLoggedIn():
            print "still not logged in"
            return """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
            <script>window.location='/'</script></html>"""
        
        teacher = authGetID()
        
        if signout is not None:
            db.setEntry(day,time,self.type,db.getTeacherId(teacher),signout)
            return """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
            <script>window.location='?'</script></html>"""
        
        src = """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
        <head>
            <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
            <title>MBS Technology Signout</title>
            <link rel="stylesheet" href="/static/style.css" type="text/css" charset="utf-8" />
            <script src="/static/jquery.min.js"></script>
            <script>
            function signout(name, currentQ, leftQ, date, time)
            {
                var moreStr = "";
                
                if(currentQ != 0)
                    moreStr = "(" + leftQ + " more) ";
                
                res = prompt("You currently have " + currentQ +
                             " %(slugN)s signed out for " + time + " on " + date + ".\\n\\n" +
                             "You can sign out up to " + (currentQ + leftQ) + " %(slugN)s " + moreStr + "in that slot:\\n", currentQ);
                
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
                    alert("You requested " + (res - currentQ) + " additional %(slugN)s. However, there are only " + leftQ + " available. Please try again.");
                    signout(name, currentQ, leftQ, date, time);
                    return;
                }
                
                window.location = "?signout=" + res + ";day=" + date + ";time=" + time;
            }
            </script>
        </head>
        <body id="tab%(id)d">
            <div id="header">
                <a href="/"><img src="/static/signout-logo.png" id="logo"/></a>
                %(tabs)s
            </div>
            <div id="headerButton">
                Signing out %(slugN)s<br/><small><small>as "%(name)s"</small></small>
                <div id="headerButtonSub">
                    The number of remaining seats in each time slot is indicated below. Click on a time slot to change the number of seats <em>you</em> need. When you are done, click the button below to continue.<br/><br/>
                    Each slot has %(q)d %(slugN)s available unless otherwise noted.
                </div>
            </div>
            <a href="?logout=1"><div id="signoutButton">
                <img src="/static/play.png" valign="top"/> Done
            </div></a>
            <div id="schedule">""" % {
                "id": self.type,
                "name": db.getResourceName(self.type),
                "slug": db.getResourceSlug(self.type),
                "slugN": db.getResourceSlugN(self.type),
                "q": db.getResourceQuantity(self.type),
                "tabs": generateTabs("/signout/choose"),
                "name": teacher }

        src += "".join(list(generateSignoutSchedulePage(date,self.type)))

        src += """
            </div>
        </body>
        </html>"""
        
        return src
    choose.exposed = True
