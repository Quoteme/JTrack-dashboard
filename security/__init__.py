import pandas as pd

passwd_file = 'passwd.csv'
columns = ['user', 'password', 'role']
auth_pairs = pd.read_csv(passwd_file)
auth_pairs = auth_pairs.reindex(columns=columns)
