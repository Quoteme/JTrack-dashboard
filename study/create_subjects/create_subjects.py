import os

import qrcode

from study.create_subjects.SubjectPDF import SubjectPDF


def create_subject(self, subject_number):
	"""
	creates one subject, if he or she exists return

	:param subject_number: the number of one subject used as suffix
	:return:
	"""
	subject_name = self.study_id + '_' + str(subject_number).zfill(self.max_subjects)
	sheets_path = self.sheets_path
	if os.path.isfile(sheets_path + '/' + subject_name + '.pdf'):
		return
	else:
		self.create_qr_codes(subject_name)
		self.write_to_pdf(subject_name)


def create_qr_codes(self, subject_name):
	"""
	Function to create a QR-code which corresponds to the new subject given. The Code will be stored in a .png.

	:param subject_name: id of subject (study name + number)
	:return:
	"""
	for activation_number in range(1, self.number_of_activations + 1):
		current_qr_code = self.qr_path + '/' + subject_name + '_' + str(activation_number) + '.png'
		qr = qrcode.QRCode(
			version=1,
			error_correction=qrcode.constants.ERROR_CORRECT_H,
			box_size=10,
			border=4,
		)
		data = "https://jutrack.inm7.de?username=%s&studyid=%s" % (subject_name + '_' + str(activation_number), self.study_id)
		# Add data
		qr.add_data(data)
		qr.make(fit=True)
		# Create an image from the QR Code instance
		img = qr.make_image()
		# Save it somewhere, change the extension as needed:
		img.save(current_qr_code)


def write_to_pdf(self, subject_name):
	"""
	TODO: more information
	Function to generate a pdf based on QR-Code and other information.

	:param subject_name: id of subject
	:return:
	"""
	qr_codes = self.qr_path + '/' + subject_name
	pdf_path = self.sheets_path + '/' + subject_name + '.pdf'

	pdf = SubjectPDF(self.study_id)
	pdf.add_page()

	pdf.draw_input_line_filled('Subject ID', subject_name)
	pdf.draw_input_line('Clinical ID')
	pdf.ln(10)

	pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
	pdf.ln(15)

	pdf.qr_code(qr_codes, 5)

	pdf.output(pdf_path)
