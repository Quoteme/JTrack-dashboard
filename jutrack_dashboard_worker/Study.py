import json
import os

import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import qrcode

from jutrack_dashboard_worker import studies_folder, storage_folder, csv_prefix, dash_study_folder, \
	qr_folder, sheets_folder, zip_file, archive_folder, get_sensor_list, timestamp_format
from Exceptions import StudyAlreadyExistsException, EmptyStudyTableException
from jutrack_dashboard_worker.SubjectPDF import SubjectPDF
from jutrack_dashboard_worker.AppUser import AppUser


class Study:
	"""
	This class represents a study of JuTrack
	"""
	# subject names from ...00001 - ...99999
	max_subjects = 5
	# 4 qr code activations per user -> if >=10 get_enrolled_app_users has to be adjusted
	number_of_activations = 4

	def __init__(self, study_json):
		"""
		constructor for a study resolving especially paths to belonging folders and important files

		:param study_json: study_json containing the essential information
		"""
		self.study_json = study_json
		self.study_id = study_json["name"]
		self.sensors = study_json["sensor-list"]
		self.duration = study_json["duration"]
		self.qr_path = dash_study_folder + '/' + self.study_id + '/' + qr_folder
		self.sheets_path = dash_study_folder + '/' + self.study_id + '/' + sheets_folder
		self.study_csv = storage_folder + '/' + csv_prefix + self.study_id + '.csv'
		self.study_path = studies_folder + '/' + self.study_id
		self.json_file_path = self.study_path + "/" + self.study_id + ".json"
		self.user_list = []

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
		if os.path.isdir(self.study_path):
			raise StudyAlreadyExistsException

		# creates study folder in storage folder
		os.makedirs(self.study_path)

		# generate folders for qr codes and subject sheets in dashboard folder of study
		os.makedirs(self.qr_path)
		os.makedirs(self.sheets_path)

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
		os.makedirs(archived_study_path)
		os.rename(studies_folder + '/' + self.study_id, archived_study_path + '/' + self.study_id)
		if os.path.isfile(self.study_csv):
			os.rename(self.study_csv, archived_study_path + '/' + csv_prefix + self.study_id + '.csv')

	####################################################################
	# ----------------------- Sheets zipping ------------------------- #
	####################################################################

	def get_download_link_unused_sheets(self):
		"""
		Create download button for unused study sheets

		:return: Link which looks like a button to download sheets
		"""
		return html.A(id='download-unused-sheets-link', children='Download unused study sheets', className='button', href='/download-' + self.study_id)

	def zip_unused_sheets(self):
		"""
		zip all unused study sheets in order to download it later

		:return:
		"""
		zip_path = dash_study_folder + '/' + self.study_id + '/' + zip_file
		if os.path.isfile(zip_path):
			os.remove(zip_path)
		all_subject_list = np.array(os.listdir(self.sheets_path))
		enrolled_subject_list = np.array([enrolled_subject + '.pdf' for enrolled_subject in self.get_enrolled_app_users_from_json()])
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

	def get_unused_sensors(self):
		return np.setdiff1d(get_sensor_list(), self.sensors)

	####################################################################
	# ------------------------ User management ----------------------- #
	####################################################################

	def get_enrolled_app_users_from_json(self):
		"""
		get list of all app users that have ever scanned at least one qr code

		:return: list of active app users
		"""
		enrolled_qr_codes = np.array(self.study_json["enrolled-subjects"])
		all_enrolled_app_users = np.unique([scanned[:-2] for scanned in enrolled_qr_codes])
		sorted_list = np.sort(all_enrolled_app_users)
		return sorted_list

	def get_enrolled_qr_codes_from_json(self):
		"""
		get list of all app users that have ever scanned at least one qr code

		:return: list of active app users
		"""
		enrolled_qr_codes = np.array(self.study_json["enrolled-subjects"])
		sorted_list = np.sort(enrolled_qr_codes)
		return sorted_list

	def get_ids_with_missing_data(self):
		missing_data_ids = []
		for user in self.user_list:
			missing_data_ids.extend(user.ids_with_missing_data)
		return missing_data_ids

	####################################################################
	# ----------------------- Study information ---------------------- #
	####################################################################

	def get_study_info_div(self):
		"""
		Returns information of specified study as a div

		:return: Study information div
		"""
		duration = self.study_json["duration"]
		total_number_subjects = self.study_json["number-of-subjects"]
		enrolled_subject_list = self.get_enrolled_app_users_from_json()
		sensor_list = self.sensors
		description = self.study_json["description"]

		return html.Div(id='study-info', children=[
				html.P(description),
				html.P('Study duration: ' + duration + ' days'),
				html.P(id='total-subjects', children='Total number of subjects: ' + total_number_subjects),
				html.Div(id='create-subject-wrapper', children=[
					dcc.Input(id='create-additional-subjects-input', placeholder='Number of new subjects', type='number', min='0'),
					html.Button(id='create-additional-subjects-button', children='Create new subjects')]),
				html.P('Number of enrolled subjects: ' + str(len(enrolled_subject_list))),
				html.P('Sensors: '),
				html.Div(children=html.Ul(children=[html.Li(children=sensor) for sensor in sensor_list]))
		])

	####################################################################
	# -------------------------- Study Table ------------------------- #
	####################################################################

	def get_study_data_table(self):
		"""
		This function returns a div displaying subjects' information which is stored in the data set for the study

		:return: Html-Table containing all the enrolled subjects information
		"""
		study_df = pd.read_csv(self.study_csv)
		if len(study_df.index) == 0:
			raise EmptyStudyTableException

		study_df = study_df.rename(columns={"subject_name": "id"})
		study_df = study_df.sort_values(by='id')
		study_df = self.drop_unused_sensor_columns(study_df)
		study_df = study_df.replace(to_replace=[np.nan, 'none', 0], value='')

		return html.Div(id='study-table-and-legend-wrapper', children=[
			html.Div(id='study-table-wrapper', children=self.generate_html_table(study_df)),
			html.Div(id='legend-wrapper', className='row', children=[
				html.Div(id='color-legend-wrapper', children=self.get_color_legend()),
				html.Div(id='status-code-legend-wrapper', children=self.get_status_code_legend())])])

	def drop_unused_sensor_columns(self, study_df):
		"""
		Drops columns of sensors which are not selected in the study. Only if completely empty (-> if actual unused sensors contain
		data they will be highlighted)

		:param study_df: data frame of study
		:return: edited data frame without unused sensors
		"""
		unused_sensors = self.get_unused_sensors()
		for sensor in unused_sensors:
			study_df[sensor + ' n_batches'] = study_df[sensor + ' n_batches'].replace(to_replace=[0], value=np.nan)
			study_df[sensor + ' last_time_received'] = study_df[sensor + ' last_time_received'].replace(to_replace=['none'], value=np.nan)
		study_df = pd.DataFrame.dropna(study_df, axis=1, how='all')
		return study_df

	def generate_html_table(self, study_df):
		"""
		generate html table with dash containing header and data body

		:param study_df: study data frame
		:return: dash html table
		"""
		header = self.get_study_table_header(study_df)
		body = self.get_study_table_body(study_df)
		return html.Table(id='study-table', children=[
			html.Thead(header),
			html.Tbody(body)])

	def get_study_table_header(self, study_df):
		"""
		retrieves header for the html table, if there is a sensor that should not be in the study and has data it will be highlighted

		:param study_df: study data frame
		:return: dash html table row which will be the header row
		"""
		header_row = [html.Th(children='user', className='clean')]
		unused_sensor_ltr_list = [sensor + ' last_time_received' for sensor in self.get_unused_sensors()]
		unused_sensor_batches_list = [sensor + ' n_batches' for sensor in self.get_unused_sensors()]

		for col in study_df.columns:
			if col in unused_sensor_ltr_list or col in unused_sensor_batches_list:
				header_row.append(html.Th(children=col, className='not-clean'))
			else:
				header_row.append(html.Th(children=col, className='clean'))
		return html.Tr(header_row)

	def get_study_table_body(self, study_df):
		"""
		create dash html body, iterates over a list of app user objects which contain necessary information about each user. The actual list of
		active users is returned by get_enrolled_app_users_from_json

		:param study_df:
		:return:
		"""
		body = []
		self.get_app_user_objects_from_table(study_df)
		for user in self.user_list:
			body.extend(user.get_rows_for_all_ids())
		return body

	def get_app_user_objects_from_table(self, study_df):
		"""
		return list of app user objects that store necessary data for each user that comes from the different qr code activations

		:param study_df: study data frame
		:return: list with app user objects
		"""
		active_users = self.get_enrolled_app_users_from_json()
		for user in active_users:
			self.user_list.append(AppUser(user_name=user, data=study_df[study_df['id'].str.match(user)], study_id=self.study_id, duration=self.duration))

	@staticmethod
	def get_color_legend():
		"""
		color legend beneath the table to identify meaning of highlights
		:return: unordered list with color information
		"""
		return html.Ul(children=[
			html.Li("No data sent for 2 days", className='red'),
			html.Li("Sensor was not chosen", className='not-clean'),
			html.Li("Left study too early", className='blue'),
			html.Li("Study duration reached, not left", className='light-green'),
			html.Li("Study duration reached, left", className='dark-green'),
			html.Li("Multiple QR Codes of one user active", className='orange')
		])

	@staticmethod
	def get_status_code_legend():
		"""
		legend for status codes empty,1,2
		:return:
		"""
		return html.Ul(children=[
			html.Li("Empty - everything is fine"),
			html.Li("1 - User left study with this QR Code"),
			html.Li("2 - Inform an admin"),
		])

	####################################################################
	# ---------------------- Push notifications ---------------------- #
	####################################################################

	def get_push_notification_div(self):
		all_ids = [{'label': enrolled_qr_code, 'value': enrolled_qr_code} for enrolled_qr_code in self.get_enrolled_qr_codes_from_json()]
		return html.Div(id='push-notification', children=[
			html.H3('Push notifications'),
			html.Div(id='push-notification-information-wrapper', children=[
				html.Div(id='push-notification-title-wrapper', children=dcc.Input(id='push-notification-title', placeholder='Message title', type='text')),
				html.Div(id='push-notification-text-wrapper', children=dcc.Textarea(id='push-notification-text', placeholder='Message text')),
				html.Div(id='push-notification-receiver-list-wrapper', children=[
					dcc.Dropdown(id='receiver-list', options=all_ids, multi=True, placeholder='Receiver...')])]),
			html.Div(id='autofill-button-wrapper', children=[
				html.Button(id='every-user-button', children='All IDs', **{'data-user-list': self.get_enrolled_qr_codes_from_json()}),
				html.Button(id='user-with-missing-data-button', children='Missing data IDs', **{'data-user-list': self.get_ids_with_missing_data()})]),
			html.Button(id='send-push-notification-button', children='Send notification'),
			html.Div(id='push-notification-output-state')
		])
