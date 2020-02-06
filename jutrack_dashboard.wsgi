#!/usr/bin/python
import getpass
import os
import sys
from dashboard import app


if getpass.getuser() == 'msfz':
	home = os.environ['HOME']
	sys.path.insert(0, home + '/JuTrack/jutrack-dashboard')
else:
	sys.path.insert(0, "/var/www/jutrack-dashboard")


server = app.server
application = server
