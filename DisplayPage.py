import datetime

def generateComputersPage(weekOf):
    return weekOf.isoformat()

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
        	</div></a>"""
        
        if date is None:
            date = datetime.date(2009,9,4)
        
        yield generateComputersPage(date)
        
        yield """
        	</div>
        </body>
        </html>"""

    computers.exposed = True
    
    index = computers
    index.exposed = True