# -*- coding: utf-8 -*-

import cherrypy
import db
import os
from DisplayPage import tabbedSchedulePage
from SignoutPage import signoutPage
from cherrypy.lib import static
from utils import *

thisdir = os.path.dirname(__file__)

computers_id = db.getResourceId("Lab Computers")
laptops_id = db.getResourceId("Laptop Lab")
projectors_id = db.getResourceId("Projector")

root = tabbedSchedulePage(computers_id)

root.computers = root
root.computers.signout = signoutPage(computers_id)

root.laptoplab = tabbedSchedulePage(laptops_id)
root.laptoplab.signout = signoutPage(laptops_id)

root.projector = tabbedSchedulePage(projectors_id)
root.projector.signout = signoutPage(projectors_id)

cherrypy.tree.mount(root, config=os.path.join(thisdir, 'tutorial.conf'))

if __name__ == '__main__':
    cherrypy.quickstart(config=os.path.join(thisdir, 'tutorial.conf'))