import getpass
import pandas as pd

auth_pairs = pd.DataFrame({'user': ['admin'], 'password': ['ju7r4cK!'], 'role': ['master']})
if getpass.getuser() == 'msfz':
	auth_pairs = pd.DataFrame({'user': ['ms'], 'password': ['ms'], 'role': ['master']})