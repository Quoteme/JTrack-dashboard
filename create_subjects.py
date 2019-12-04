import dash_core_components as dcc
import dash_html_components as html
from random import randint
import qrcode
import os
from fpdf import FPDF

from SubjectPDF import SubjectPDF


def write_to_pdf(qr_code_path, study_dir, new_subj_name):
	"""
	TODO: more information
	Function to generate a pdf based on QR-Code and other information.

			Parameters
			----------
				qr_code_path
					path to QR-code referring to given new subject (.png)
				study_dir
					path to the directory of the study ('./studies/study_name').
				new_subj_name
					name of subject (Subject00000).
			Return
			-------

	"""
	study_name = study_dir.split('/')[-1]
	sheets_dir = study_dir + '/subject-sheets'
	os.makedirs(sheets_dir, exist_ok=True)
	pdf_path = sheets_dir + '/' + new_subj_name + '.pdf'

	pdf = SubjectPDF(new_subj_name)
	pdf.add_page()
	pdf.set_font("Arial", size=12)
	
	pdf.image(qr_code_path, x=100, y=50, w=50)
	pdf.output(pdf_path)


def create_qr_code_for_new_user(study_dir, new_subj_dir):
	"""
	Function to create a QR-code which corresponds to the new subject given. The Code will be stored in a .png as well
	as in a pdf which contains additional information. (png: ./study_dir/QR-Codes; pdf: ./study-dir/subject-sheets)

			Parameters
			----------
				study_dir
					path to the directory of the study ('./studies/study_name').
				new_subj_dir
					path to the directory of the new subject containing particularly its name ('./studies/study-name/Subject00000').
			Return
			-------

	"""

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


def create_subjects(study_dir, number_users):
	"""
	Function that is executed if the create new subjects button is clicked. It creates new subject directories and
	corresponding QR-codes.

			Parameters
			----------
				study_dir
					path to the directory of the study where new subjects should be dropped. ('./studies/study_name')
				number_users
					number of new subjects that should be enrolled
			Return
			-------

	"""

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


if __name__ == '__main__':
	name = 'Subject06754'
	study = 'new'
	studies_dir = './studies'
	sdir = studies_dir + '/' + study
	qr = sdir + '/QR-Codes/' + name + '.png'
	write_to_pdf(qr, sdir, name)
