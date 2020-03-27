import json
import os

import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
import qrcode
from datalad.api import Dataset

from jutrack_dashboard_worker import studies_folder, storage_folder, csv_prefix, dash_study_folder, \
	qr_folder, sheets_folder, zip_file, archive_folder
from jutrack_dashboard_worker.Exceptions import StudyAlreadyExistsException
from jutrack_dashboard_worker.SubjectPDF import SubjectPDF


class Study:
	"""
		This class represents a study of JuTrack
	"""

	max_subjects = 5
	number_of_activations = 4

	def __init__(self, study_json):
		"""
		constructor for a study resolving especially paths to belonging folders and important files

		:param study_json: study_json containing the essential information
		"""

		self.study_json = study_json
		self.study_id = study_json["name"]
		self.qr_path = dash_study_folder + '/' + self.study_id + '/' + qr_folder
		self.sheets_path = dash_study_folder + '/' + self.study_id + '/' + sheets_folder
		self.study_csv = storage_folder + '/' + csv_prefix + self.study_id + '.csv'
		self.study_path = studies_folder + '/' + self.study_id
		self.json_file_path = self.study_path + "/" + self.study_id + ".json"

	@classmethod
	def from_json_dict(cls, study_json):
		"""
		creates a study object from given json file (if a study is supposed to be created completely from scratch)

		:param study_json: json containing relevant information
		:return: study object
		"""

		return cls(study_json)

	@classmethod
	def from_study_id(cls, study_id):
		"""
		creates a study object from existing sources (json is stored somewhere on the server)

		:param study_id: name of study to which the study object belongs
		:return: study object
		"""

		study_json_file_path = studies_folder + '/' + study_id + "/" + study_id + ".json"
		with open(study_json_file_path, 'r') as f:
			study_json = json.load(f)
		return cls(study_json)

	def create(self):
		"""
		Create study using underlying json data which contains study_name, initial number of subjects, study duration and a list
		of sensors to be used. The new study is created in the storage folder and deposited as a Datalad data set. Further,
		folders for qr codes and subjects sheets will be create within the dashboard project and filled with corresponding qr codes
		and pdfs. Lastly, a json file containing meta data of the study is stored within the Datalad data set.

		:return: True or False depending if creation succeeded. False if and only if study already exists.
		"""

		initial_subject_number = self.study_json["number-of-subjects"]
		if os.path.isdir(self.study_path):
			raise StudyAlreadyExistsException

		# creates study folder in storage folder and stores it as datalad data set
		os.makedirs(self.study_path)
		study_date_set = Dataset(self.study_path)
		study_date_set.create(self.study_path)

		# generate folders for qr codes and subject sheets in dashboard folder of study
		os.makedirs(self.qr_path, exist_ok=True)
		os.makedirs(self.sheets_path, exist_ok=True)

		# store json file with meta data
		self.save_study_json(
			"new file " + self.json_file_path + " for study, " + str(initial_subject_number) + ' subjects created')

		# create subjects depending on initial subject number
		self.create_sheets_wrt_total_subject_number()

	def close(self):
		"""
		close a study (moves it to archive folder)
		:return:
		"""
		archived_study_path = archive_folder + '/' + self.study_id
		os.makedirs(archived_study_path, exist_ok=True)
		os.rename(studies_folder + '/' + self.study_id, archived_study_path + '/' + self.study_id)
		if os.path.isfile(self.study_csv):
			os.rename(self.study_csv, archived_study_path + '/' + csv_prefix + self.study_id + '.csv')

	####################################################################
	# ----------------------- Sheets zipping ------------------------- #
	####################################################################

	def zip_unused_sheets(self):
		"""
		zip all unused study sheets in order to download it later
		:return:
		"""
		zip_path = dash_study_folder + '/' + self.study_id + '/' + zip_file
		if os.path.isfile(zip_path):
			os.remove(zip_path)
		all_subject_list = np.array(os.listdir(self.sheets_path))
		enrolled_subject_list = np.array(
			[enrolled_subject + '.pdf' for enrolled_subject in self.study_json['enrolled-subjects']])
		not_enrolled_subjects = [self.sheets_path + '/' + not_enrolled_subject for not_enrolled_subject in
								 np.setdiff1d(all_subject_list, enrolled_subject_list)]
		os.system('zip ' + zip_path + ' ' + ' '.join(not_enrolled_subjects))

	def zip_marked_sheets(self, marked_sheets):
		"""
		zip all marked study sheets of enrolled subjects
		:param marked_sheets: list of marked subjects
		:return:
		"""
		zip_path = dash_study_folder + '/' + self.study_id + '/' + zip_file
		if os.path.isfile(zip_path):
			os.remove(zip_path)
		marked_pdfs = [self.sheets_path + '/' + marked_sheet + '.pdf' for marked_sheet in marked_sheets]
		os.system('zip ' + zip_path + ' ' + ' '.join(marked_pdfs))

	####################################################################
	# ----------------------- Subject creation ----------------------- #
	####################################################################

	def create_additional_subjects(self, number_of_subjects):
		"""
		create additional subjects for the study
		:param number_of_subjects: number of subjects to create
		:return:
		"""
		self.study_json["number-of-subjects"] = str(int(self.study_json["number-of-subjects"]) + number_of_subjects)
		self.save_study_json(msg='number of current subjects set to ' + self.study_json["number-of-subjects"])
		self.create_sheets_wrt_total_subject_number()

	def create_sheets_wrt_total_subject_number(self):
		"""
		adjust the number of existing subject sheets according to the number of all subjects (creates for each subject a sheet)
		:return:
		"""
		n_subjects = int(self.study_json["number-of-subjects"])
		for subject_number in range(1, n_subjects + 1):
			self.create_subject(subject_number)

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

		qr_path = self.qr_path
		for i in range(1, self.number_of_activations + 1):
			activation_number = '_' + str(i)
			current_qr_code = qr_path + '/' + subject_name + activation_number + '.png'
			qr = qrcode.QRCode(
				version=1,
				error_correction=qrcode.constants.ERROR_CORRECT_H,
				box_size=10,
				border=4,
			)
			data = "https://jutrack.inm7.de?username=%s&studyid=%s" % (subject_name + activation_number, self.study_id)
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

		qr_path = self.qr_path
		sheets_path = self.sheets_path
		qr_codes = qr_path + '/' + subject_name
		pdf_path = sheets_path + '/' + subject_name + '.pdf'

		pdf = SubjectPDF(self.study_id)
		pdf.add_page()

		pdf.draw_input_line_filled('Subject-ID', subject_name)
		pdf.ln(10)

		pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
		pdf.ln(15)

		pdf.qr_code(qr_codes, 5)

		pdf.output(pdf_path)

	####################################################################
	# ------------------------- JSON control ------------------------- #
	####################################################################

	def save_study_json(self, msg):
		"""
		saves the study json file and saves it within Datalad
		:param msg: message for Datalad save operation
		:return:
		"""

		study_date_set = Dataset(self.study_path)
		with open(self.json_file_path, 'w') as f:
			json.dump(self.study_json, f, ensure_ascii=False, indent=4)
		study_date_set.save(self.study_json, message=msg, recursive=True)

	def refresh_json_with_active_subjects(self):
		"""
		saves the list of enrolled subjetcs into the json file (refreshes it)
		:return:
		"""
		df = pd.read_csv(self.study_csv)
		active_subjects = np.array(df['subject_name'].unique()).tolist()
		self.study_json["enrolled-subjects"] = active_subjects
		self.save_study_json(msg='active subjects list adjusted. Now ' + str(len(active_subjects)) + ' active subjects')

	####################################################################
	# ----------------------------- Divs ----------------------------- #
	####################################################################

	def get_study_info_div(self):
		"""
		Returns information of specified study as a div

		:return: Study information div
		"""

		try:
			self.refresh_json_with_active_subjects()
			active_subjects_table = self.get_active_subjects_data_table_div()
		except FileNotFoundError or KeyError:
			active_subjects_table = html.Div("No data available.")
		return html.Div([
			html.Br(),
			dcc.Loading(id='loading-study-details', children=[self.get_study_details_div()], type='circle'),
			html.Br(),
			html.Div(children=[
				dcc.Input(id='create-additional-subjects-input', placeholder='Number of new subjects', type='number',
						  min='0'),
				html.Button(id='create-additional-subjects-button', children='Create new subjects')]),
			html.Br(),
			active_subjects_table,
			html.Br(),
			html.A(id='download-unused-sheets-zip', children='Download unused study sheets', className='button'),
		])

	def get_active_subjects_data_table_div(self):
		"""
		This function returns a div displaying subjects' information which is stored in the data set for the study

		:return: Dcc-Table containing all the enrolled subjects information
		"""

		df = pd.read_csv(self.study_csv)
		study_df = pd.DataFrame.dropna(df.replace(to_replace='none', value=np.nan), axis=1, how='all')
		study_df = study_df.rename(columns={"subject_name": "id"})

		conditional_list = self.get_overdue_subjects(study_df)

		return html.Div(children=[dash_table.DataTable(
			id='table',
			columns=[{"name": i, "id": i} for i in study_df.columns],
			fixed_columns={'headers': True, 'data': 1},
			style_table={'maxWidth': '1000px'},
			data=study_df.to_dict('records'),
			style_cell={"fontFamily": "Arial", "size": 10, 'textAlign': 'left'},
			style_header={
				'backgroundColor': 'rgb(230, 230, 230)',
				'fontWeight': 'bold'
			},
			style_data_conditional=conditional_list,
			row_selectable='multi'),
			html.A(id='download-marked-sheets-zip', children='Download marked study sheets', className='button')])

	def get_study_details_div(self):
		"""
		get all relevant study information in a div (number of all subjects/enrolled subjects, duration, ...)

		:return: div with information
		"""

		duration = self.study_json["duration"]
		total_number_subjects = self.study_json["number-of-subjects"]
		enrolled_subject_list = self.study_json["enrolled-subjects"]
		sensor_list = self.study_json["sensor-list"]
		description = self.study_json["description"]

		return html.Div(children=[
			html.P(description, style={'padding-left': '12px'}),
			html.P("Study duration: " + duration + " days", style={'padding-left': '24px'}),
			html.P(id='total-subjects', children="Total number of subject: " + total_number_subjects,
				   style={'padding-left': '24px'}),
			html.P("Number of enrolled subjects: " + str(len(enrolled_subject_list)), style={'padding-left': '24px'}),
			html.P("Sensors: " + ", ".join(sensor_list), style={'padding-left': '24px'})
		], className='div-border', style={'width': '320px'})

	def get_overdue_subjects(self, study_df):
		"""
		Creates a list containing all subjects that are longer in the study as allowed

		:param study_df: dataframe containing information regarding enrolled subjects
		:return:
		"""
		study_duration = int(self.study_json["duration"])
		conditional_list = []
		overdue_subjects = []

		for i, time_in_study in enumerate(study_df['time_in_study']):
			days_in_study = int(str(time_in_study).split(' ')[0])
			if days_in_study > study_duration:
				overdue_subjects.append(i)
		for i in overdue_subjects:
			conditional_list.append({'if': {'row_index': i}, 'backgroundColor': '#FFA18C'})

		return conditional_list
