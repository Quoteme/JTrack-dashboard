import tarfile
import zipfile

import qrcode
import os
from subject_configuration.SubjectPDF import SubjectPDF
import xml.etree.ElementTree as ET


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

	pdf = SubjectPDF(study_name)
	pdf.add_page()

	pdf.draw_input_line_filled('Subject-ID', new_subj_name)
	pdf.ln(10)

	pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
	pdf.ln(15)

	pdf.qr_code(qr_code_path, 5)

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
	qr_code_path = study_dir + '/QR-Codes/' + new_subj_name
	for i in range(1, 5):
		activation_number = '_' + str(i)
		current_qr_code = qr_code_path + activation_number +'.png'

		qr = qrcode.QRCode(
			version=1,
			error_correction=qrcode.constants.ERROR_CORRECT_H,
			box_size=10,
			border=4,
		)

		data = "https://jutrack.inm7.de?username=%s&studyid=%s" % (new_subj_name + activation_number, study_name)

		# Add data
		qr.add_data(data)
		qr.make(fit=True)

		# Create an image from the QR Code instance
		img = qr.make_image()

		# Save it somewhere, change the extension as needed:
		img.save(current_qr_code)
	write_to_pdf(qr_code_path, study_dir, new_subj_name)


def zip_subject_sheet_folder(study_dir):
	print("Ich zippe")
	os.system('zip ' + study_dir + '/subject_sheets.zip ' + study_dir + '/subject-sheets/*')


def create_subjects(study_dir, number_new_subjects):
	"""
	Function that is executed if the create new subjects button is clicked. It creates new subject directories and
	corresponding QR-codes.

			Parameters
			----------
				study_dir
					path to the directory of the study where new subjects should be dropped. ('./studies/study_name')
				number_new_subjects
					number of new subjects that should be enrolled
			Return
			-------

	"""

	study_name = str(study_dir).split('/')[-1]
	study_xml_path = study_dir + '/' + study_name + '-info.xml'
	study_xml = ET.parse(study_xml_path)
	root = study_xml.getroot()

	number_subjects_element = next(root.iter('number-subjects'))
	current_number_subjects = int(number_subjects_element.text)

	for subj_number in range(current_number_subjects+1, current_number_subjects+number_new_subjects+1):
		new_subj_dir = study_dir + '/' + study_name + '_' + str(subj_number).zfill(5)

		os.makedirs(new_subj_dir)
		create_qr_code_for_new_user(study_dir, new_subj_dir)

	zip_subject_sheet_folder(study_dir)
	number_subjects_element.text = str(current_number_subjects + number_new_subjects)
	study_xml.write(study_xml_path)
	return


if __name__ == '__main__':
	name = 'Subject00090'
	study = 'new'
	studies_dir = './studies'
	sdir = studies_dir + '/' + study
	qr_path = sdir + '/QR-Codes/' + name + '.png'
	write_to_pdf(qr_path, sdir, name)
