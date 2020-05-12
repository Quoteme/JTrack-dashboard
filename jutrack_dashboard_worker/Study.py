import json
import os

import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import qrcode
from datetime import datetime

from jutrack_dashboard_worker import studies_folder, storage_folder, csv_prefix, dash_study_folder, \
	qr_folder, sheets_folder, zip_file, archive_folder, get_sensor_list, timestamp_format
from jutrack_dashboard_worker.Exceptions import StudyAlreadyExistsException, EmptyStudyTableException
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
		self.sensors = study_json["sensor-list"]
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

	####################################################################
	# --------------------- Create and Close ------------------------ #
	####################################################################

	def create(self):
		"""
		Create study using underlying json data which contains study_name, initial number of subjects, study duration and a list
		of sensors to be used. The new study is created in the storage folder. Further,
		folders for qr codes and subjects sheets will be create within the dashboard project and filled with corresponding qr codes
		and pdfs. Lastly, a json file containing meta data of the study is stored.

		:return: True or False depending if creation succeeded. False if and only if study already exists.
		"""

		initial_subject_number = self.study_json["number-of-subjects"]
		if os.path.isdir(self.study_path):
			raise StudyAlreadyExistsException

		# creates study folder in storage folder
		os.makedirs(self.study_path)

		# generate folders for qr codes and subject sheets in dashboard folder of study
		os.makedirs(self.qr_path, exist_ok=True)
		os.makedirs(self.sheets_path, exist_ok=True)

		# store json file with meta data
		self.save_study_json()

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
		enrolled_subject_list = np.array([enrolled_subject + '.pdf' for enrolled_subject in self.get_enrolled_subjects()])
		not_enrolled_subjects = [self.sheets_path + '/' + not_enrolled_subject for not_enrolled_subject in np.setdiff1d(all_subject_list, enrolled_subject_list)]
		os.system('zip ' + zip_path + ' ' + ' '.join(not_enrolled_subjects))

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
		self.save_study_json()
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

		pdf.draw_input_line_filled('Subject ID', subject_name)
		pdf.draw_input_line('Clinical ID')
		pdf.ln(10)

		pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
		pdf.ln(15)

		pdf.qr_code(qr_codes, 5)

		pdf.output(pdf_path)

	####################################################################
	# ------------------------- JSON control ------------------------- #
	####################################################################

	def save_study_json(self):
		"""
		saves the study json file
		:return:
		"""
		with open(self.json_file_path, 'w') as f:
			json.dump(self.study_json, f, ensure_ascii=False, indent=4)

	def get_enrolled_subjects(self):
		enrolled_qr_codes = np.array(self.study_json["enrolled-subjects"])
		all_enrolled_subjects = np.unique([scanned[:-2] for scanned in enrolled_qr_codes])
		return all_enrolled_subjects

	####################################################################
	# ----------------------------- Divs ----------------------------- #
	####################################################################

	def get_study_info_div(self):
		"""
		Returns information of specified study as a div

		:return: Study information div
		"""

		try:
			active_subjects_table = self.get_subjects_table()
		except FileNotFoundError or KeyError:
			active_subjects_table = html.Div("No data available.")
		except KeyError:
			active_subjects_table = html.Div("No data available.")
		except EmptyStudyTableException:
			active_subjects_table = html.Div("No data available.")
		return html.Div([
			html.Br(),
			dcc.Loading(id='loading-study-details', children=[self.get_study_details()], type='circle'),
			html.Br(),
			html.Div(children=[
				dcc.Input(id='create-additional-subjects-input', placeholder='Number of new subjects', type='number', min='0'),
				html.Button(id='create-additional-subjects-button', children='Create new subjects')]),
			html.Br(),
			active_subjects_table,
			html.Br(),
			html.A(id='download-unused-sheets-button', children='Download unused study sheets', className='button'),
		])

	def get_study_details(self):
		"""
		get all relevant study information in a div (number of all subjects/enrolled subjects, duration, ...)

		:return: div with information
		"""

		duration = self.study_json["duration"]
		total_number_subjects = self.study_json["number-of-subjects"]
		enrolled_subject_list = self.get_enrolled_subjects()
		sensor_list = self.sensors
		description = self.study_json["description"]

		return html.Div(children=[
			html.P(description, style={'padding-left': '12px'}),
			html.P("Study duration: " + duration + " days", style={'padding-left': '24px'}),
			html.P(id='total-subjects', children="Total number of subjects: " + total_number_subjects, style={'padding-left': '24px'}),
			html.P("Number of enrolled subjects: " + str(len(enrolled_subject_list)), style={'padding-left': '24px'}),
			html.P("Sensors: ", style={'padding-left': '24px'}),
			html.Div(children=html.Ul(children=[html.Li(children=sensor) for sensor in sensor_list]), style={'padding-left': '48px'})
		], className='div-border', style={'width': '320px'})

	####################################################################
	# ----------------------------- Table ---------------------------- #
	####################################################################

	def get_subjects_table(self):
		"""
		This function returns a div displaying subjects' information which is stored in the data set for the study

		:return: Html-Table containing all the enrolled subjects information
		"""

		study_df = pd.read_csv(self.study_csv)
		if len(study_df.index) == 0:
			raise EmptyStudyTableException

		study_df = study_df.rename(columns={"subject_name": "id"})
		study_df = study_df.sort_values(by='id')
		study_df = self.add_user_column(study_df)
		study_df = self.drop_unused_sensor_columns(study_df)
		study_df = study_df.replace(to_replace=['none', 0], value='')

		return html.Div(children=[self.generate_html_table(study_df), self.get_legend()])

	def add_user_column(self, df):
		current_user = ''
		user_column = []

		for index, row in df.iterrows():
			next_user = str(row['id'])[:-2]
			if current_user != next_user:
				user_column.append(next_user)
				current_user = next_user
			else:
				user_column.append('')

		df.insert(loc=0, column='user', value=user_column)
		return df

	def generate_html_table(self, df):
		header = html.Tr([html.Th(col) for col in df.columns])
		body = self.get_study_table_body(df)
		return html.Table([html.Thead(header), html.Tbody(body)])

	def get_study_table_body(self, df):
		body = []
		for index, row in df.iterrows():
			body.append(self.get_table_row(row))
		return body

	def get_table_row(self, row):
		row_dict = {}
		for key, value in row.items():
			if key == 'user':
				row_dict[key] = (self.create_download_link_for_user(value))
			else:
				row_dict[key] = (html.Td(value))

		row_dict = self.give_color(row_dict)

		return html.Tr(list(row_dict.values()))

	def give_color(self, row_dict):
		id_color = ""
		registered_timestamp = datetime.strptime(row_dict["date_registered"].children, timestamp_format)
		left_timestamp = datetime.strptime(row_dict["date_left_study"].children, timestamp_format) if row_dict["date_left_study"].children != "" else ""
		time_in_study_days = int(str(row_dict["time_in_study"].children).split(" ")[0])
		last_times_received = [sensor + ' last_time_received' for sensor in self.sensors]

		for last_time_received in last_times_received:
			last_time_received_string  = row_dict[last_time_received].children

			last_time_received_dt = registered_timestamp if last_time_received_string == "" else datetime.strptime(last_time_received_string, timestamp_format)

			days_since_last_received = (datetime.now() - last_time_received_dt).days

			if days_since_last_received > 2:
				row_dict[last_time_received] = html.Td(children=last_time_received_string, className='red')
				id_color = 'red'

		if left_timestamp == "":
			if time_in_study_days - registered_timestamp.day > int(self.study_json["duration"]):
				id_color = 'light-green'

		else:
			if (left_timestamp - registered_timestamp).days >= int(self.study_json["duration"]):
				id_color = 'dark-green'
			elif (left_timestamp - registered_timestamp).days < int(self.study_json["duration"]):
				id_color = 'blue'

		row_dict['id'] = html.Td(children=row_dict['id'].children, className=id_color)

		return row_dict

	def get_legend(self):
		return html.Ul(children=[
			html.Li("No data sent for 2 days", className='red'),
			html.Li("Left study too early", className='blue'),
			html.Li("Study duration reached, not left", className='light-green'),
			html.Li("Study duration reached, left", className='dark-green')
		])


	def create_download_link_for_user(self, user):
		if user == '':
			return html.Td('')
		else:
			return html.Td(html.A(children=user, href='download-' + self.study_id + '-' + user))

	def drop_unused_sensor_columns(self, study_df):
		unused_sensors = np.setdiff1d(get_sensor_list(), self.sensors)
		for sensor in unused_sensors:
			study_df = study_df.drop(sensor + ' n_batches', axis=1)
			study_df = study_df.drop(sensor + ' last_time_received', axis=1)
		return study_df
