#!/usr/bin/python
import sys
from index import app

sys.path.insert(0, "/var/www/jutrack.inm7.de/www/dashboard")

server = app.server
application = server
