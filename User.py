import getpass

import pandas as pd

from jutrack_dashboard_worker.Exceptions import NoSuchUserException, WrongPasswordException

auth_pairs = pd.DataFrame({'user': ['admin'], 'password': ['ju7r4cK!'], 'role': ['master']})
if getpass.getuser() == 'msfz':
	auth_pairs = pd.DataFrame({'user': ['ms'], 'password': ['ms'], 'role': ['master']})


class User:
	name = None
	role = None
	authorized = False

	def login(self, name, passwd):
		user = auth_pairs.loc[auth_pairs['user'] == name]
		if user.shape[0] != 1:
			raise NoSuchUserException
		if user.iloc[0]['password'] != passwd:
			raise WrongPasswordException

		self.name = name
		self.role = user.iloc[0]['role']
		self.authorized = True





