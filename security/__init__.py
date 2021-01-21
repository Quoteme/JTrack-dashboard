import getpass
import pandas as pd

auth_pairs = pd.DataFrame({'user': ['admin', 'investigator', 'viewer'],
						   'password': ['ju7r4cK!', 'juInvest!', 'juView!'],
						   'role': ['master', 'invest', 'view']})
if getpass.getuser() == 'msfz' or getpass.getuser() == 'micst':
	auth_pairs = pd.DataFrame(
		{'user': ['ms', 'admin', 'investigator', 'viewer'],
		 'password': ['ms', 'ju7r4cK!', 'juInvest!', 'juView!'],
		 'role': ['master', 'master', 'invest', 'view']})
