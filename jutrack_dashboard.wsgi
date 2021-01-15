#!/usr/bin/python
import getpass
import os
import sys
from index import app

if getpass.getuser() == 'msfz' or getpass.getuser() == 'micst':
	home = os.path.expanduser('~')
	sys.path.insert(0, home + '/JuTrack/jutrack-dashboard')
else:
	sys.path.insert(0, "/var/www/jutrack.inm7.de/www/dashboard")

server = app.server
application = server
