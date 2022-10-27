import pandas as pd

# the passwd.csv file must be stored in ./Jrack-dashboard/security/passwd.csv
# the content should be like this:
#
# user,password,role
# testaccount,meintollespasswort,master

passwd_file = '/passwd.csv'
columns = ['user', 'password', 'role']
auth_pairs = pd.read_csv(passwd_file)
auth_pairs = auth_pairs.reindex(columns=columns)
