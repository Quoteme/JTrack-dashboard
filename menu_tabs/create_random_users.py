import os
import sys

study_name = sys.argv[1]
number_users = int(sys.argv[2])
study_dir = './studies/' + study_name

for i in range(number_users):
	os.makedirs(study_dir + '/Subject' + str(i+1))
