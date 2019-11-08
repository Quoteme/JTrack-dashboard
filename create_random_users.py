import os
import sys

study_name = sys.argv[1]
number_users = int(sys.argv[2])
study_dir = 'workingdir/studies/' + study_name

for i in range(number_users):
	os.system('mkdir ' + study_dir + '/Subject' + str(i+1))
