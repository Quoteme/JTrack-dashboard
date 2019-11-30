import dash_core_components as dcc
import dash_html_components as html
from random import randint
import qrcode
import os


def create_qr_code_for_new_user(study_dir, new_subj_dir):
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_H,
		box_size=10,
		border=4,
	)
	study_name = str(study_dir).split('/')[-1]
	new_subj_name = str(new_subj_dir).split('/')[-1]
	data = "https://jutrack.inm7.de?username=%s&studyid=%s" % (new_subj_name, study_name)

	# Add data
	qr.add_data(data)
	qr.make(fit=True)

	# Create an image from the QR Code instance
	img = qr.make_image()

	# Save it somewhere, change the extension as needed:
	img.save(study_dir + '/QR-Codes/' + new_subj_name + '.jpg')


def create_users(study_dir, number_users):
	for subj_number in range(number_users):
		rand_subj_number = str(randint(1, 10000)).zfill(5)
		new_subj_dir = study_dir + '/Subject' + rand_subj_number
		if os.path.isdir(new_subj_dir):
			print(new_subj_dir + ' already exists')
			number_users += 1
			continue
		else:
			os.makedirs(study_dir + '/Subject' + rand_subj_number)
			create_qr_code_for_new_user(study_dir, new_subj_dir)
	return
