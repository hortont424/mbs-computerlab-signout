# -*- coding: utf-8 -*-

import datetime
import db
import hashlib
import utils

password_hash = "1169352c31919b66930b14c0375cd34f"

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
        print date
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
                <input type='hidden' name='date' value='%(date)s'>
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
                "pw": password_hash,
                "date": date }

    index.exposed = True
        
    def choose(self, date=None, teacher=None, passwd=None, other=None):
        date = utils.normalizeDate(date)
        
        if passwd == None or teacher == None:
            yield """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
            Missing data! Go back and try again...</html>"""
            return
        
        m = hashlib.md5()
        m.update(passwd);
        if(m.hexdigest() != password_hash):
            yield """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
            Wrong password! Go back and try again...</html>"""
            return
        
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
        </head>
        <body id="tab%(id)d">
            <div id="header">
                <a href="/"><img src="/static/signout-logo.png" id="logo"/></a>
            </div>
            <div id="headerButton">
                Signing out %(slug)s<br/><small><small>as "%(name)s"</small></small>
                <div id="headerButtonSub">
                    The number of remaining seats in each time slot is indicated below. Click on a time slot to change the number of seats <em>you</em> need. When you are done, click the button below to continue.<br/><br/>
                    Each slot has %(q)d %(slug)s available unless otherwise noted. %(date)s
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
                "name": teacher,
                "date": date }

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

        #yield "".join(list(generateSchedulePage(date,self.type)))
        yield "ohi!!"

        yield """
            </div>
        </body>
        </html>"""
    choose.exposed = True
