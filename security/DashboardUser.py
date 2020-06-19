from Exceptions import NoSuchUserException, WrongPasswordException, MissingCredentialsException
from security import auth_pairs


class DashboardUser:
	"""
	Class for dashboard users having name, role and authorized boolean
	"""

	name = None
	role = None
	authorized = False

	def login(self, name, password):
		"""
		login function that checks if entered username and password are correct
		:param name: username
		:param password: password
		:return:
		"""

		if name is None or password is None or name == '' or password == '':
			raise MissingCredentialsException

		user = auth_pairs.loc[auth_pairs['user'] == name]
		if user.shape[0] != 1:
			raise NoSuchUserException
		if user.iloc[0]['password'] != password:
			raise WrongPasswordException

		self.name = name
		self.role = user.iloc[0]['role']
		self.authorized = True





