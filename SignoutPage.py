# -*- coding: utf-8 -*-

import datetime
import db

def generateTeachersDropdown():
    yield "<select style='font-size: 1em'>"
    
    teachers = db.getTeachers()
    
    for t in teachers:
        yield "<option name='%(id)d'>%(name)s</option>" % {
            "id": t[0],
            "name": t[1] }
    
    yield "</select>"

class signoutPage:
    def __init__(self, t):
        self.type = t
    
    def index(self, date=None):
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
            </style>
        </head>
        <body>
            <div id="header">
                <a href="/"><img src="/static/signout-logo.png" id="logo"/></a>
            </div>
            <div id="headerButton">
        		Signing out %(slug)s
        	</div>
        	<form id="signinForm">
            	<div class="headerButton" style="text-align: left;">
            		Name: %(teachers)s
            	</div>
        	</form>
        	<a href="#"><div id="signoutButton">
        		<img src="/static/play.png" valign="top"/> Continue to time slot selection
        	</div></a>
    	</body>
        </html>
            """ % {
                "id": self.type,
                "name": db.getResourceName(self.type),
                "slug": db.getResourceSlug(self.type),
                "q": db.getResourceQuantity(self.type),
                "teachers": "".join(list(generateTeachersDropdown())) }

    index.exposed = True
        
    def choose(self, date=None):
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
        		Signing out %(slug)s
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
                "q": db.getResourceQuantity(self.type) }

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
