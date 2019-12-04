
import dash_core_components as dcc
import dash_html_components as html
from random import randint
import qrcode
import os
from fpdf import FPDF


def write_to_pdf(qr_code_path, study_dir, new_subj_name):
	sheets_dir = study_dir + '/subject-sheets'
	os.makedirs(sheets_dir, exist_ok=True)
	pdf_path = sheets_dir + '/' + new_subj_name + '.pdf'

	pdf = FPDF()
	pdf.add_page()
	pdf.set_font("Arial", size=12)
	pdf.cell(200, 10, txt=new_subj_name, ln=1, align="C")
	pdf.image(qr_code_path, x=10, y=8, w=100)
	pdf.output(pdf_path)


def create_qr_code_for_new_user(study_dir, new_subj_dir):
	os.makedirs(study_dir + '/QR-Codes', exist_ok=True)

	study_name = str(study_dir).split('/')[-1]
	new_subj_name = str(new_subj_dir).split('/')[-1]
	qr_code_path = study_dir + '/QR-Codes/' + new_subj_name + '.png'

	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_H,
		box_size=10,
		border=4,
	)

	data = "https://jutrack.inm7.de?username=%s&studyid=%s" % (new_subj_name, study_name)

	# Add data
	qr.add_data(data)
	qr.make(fit=True)

	# Create an image from the QR Code instance
	img = qr.make_image()

	# Save it somewhere, change the extension as needed:
	img.save(qr_code_path)
	write_to_pdf(qr_code_path, study_dir, new_subj_name)


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
