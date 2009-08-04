# -*- coding: utf-8 -*-

import cherrypy
import db
import os
from DisplayPage import DisplayPage
from cherrypy.lib import static
from utils import *

if __name__ == '__main__':
    import os.path
    thisdir = os.path.dirname(__file__)
    cherrypy.quickstart(DisplayPage(), config=os.path.join(thisdir, 'tutorial.conf'))