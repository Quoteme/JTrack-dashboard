#!/usr/bin/python
import sys
sys.path.insert(0, "/var/www/jutrack-dashboard")

from dashboard import app

server = app.server
application = server
