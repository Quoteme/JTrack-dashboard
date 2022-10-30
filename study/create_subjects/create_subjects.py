import os

import qrcode

from app import dash_study_folder, sheets_folder, qr_folder
from study import max_subjects_exp, number_of_activations
from study.create_subjects.SubjectPDF import SubjectPDF


def create_subjects(study_id, number_to_create):
	"""
	creates one subject, if he or she exists return

	:return:
	"""
	for subject_number in range(1, number_to_create + 1):
		subject_name = study_id + '_' + str(subject_number).zfill(max_subjects_exp)
		if os.path.isfile(os.path.join(dash_study_folder, study_id, sheets_folder, subject_name + '.pdf')):
			continue
		else:
			create_qr_codes(study_id, subject_name)
			write_to_pdf(study_id, subject_name)


def create_qr_codes(study_id, subject_name):
	"""
	Function to create a QR-code which corresponds to the new subject given. The Code will be stored in a .png.

	:return:
	"""
	qr_path = os.path.join(dash_study_folder, study_id, qr_folder)
	for activation_number in range(1, number_of_activations + 1):
		user_activation_number = subject_name + '_' + str(activation_number)

		qr = qrcode.QRCode(
			version=1,
			error_correction=qrcode.constants.ERROR_CORRECT_H,
			box_size=10,
			border=4,
		)
		# os.environ['SERVER_URL']=http://remsys.ai is set in the Dockerfile
		data = f"{os.environ['SERVER_URL']}?username={user_activation_number}&studyid={study_id}"
		# Add data
		qr.add_data(data)
		qr.make(fit=True)
		# Create an image from the QR Code instance
		img = qr.make_image()
		# Save it somewhere, change the extension as needed:
		img.save(os.path.join(qr_path, user_activation_number + '.png'))


def write_to_pdf(study_id, subject_name):
	"""
	Function to generate a pdf based on QR-Code and other information.

	:return:
	"""
	qr_codes_path = os.path.join(dash_study_folder, study_id, qr_folder, subject_name)
	pdf_path = os.path.join(dash_study_folder, study_id, sheets_folder, subject_name + '.pdf')

	pdf = SubjectPDF(study_id)
	pdf.add_page()

	pdf.draw_input_line_filled('Subject ID', subject_name)
	pdf.draw_input_line('Clinical ID')
	pdf.ln(10)

	pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
	pdf.ln(15)

	pdf.qr_codes(qr_codes_path)

	pdf.output(pdf_path)
