import json
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import numpy as np

from jutrack_dashboard_worker import studies_folder, storage_folder, csv_prefix, unused_sheets_path, used_sheets_path


class Study:
	"""
		This class represents a study of JuTrack
	"""

	def __init__(self, study_id):
		self.study_id = study_id
		study_meta_data = self.get_study_json()
		self.duration = study_meta_data["duration"]
		self.n_total_subj = study_meta_data["number-of-subjects"]
		self.sensor_list = study_meta_data["sensor-list"]
		self.enrolled_subjects_table = self.get_study_csv_as_dataframe()

		self.enrolled_subjects_list = self.enrolled_subjects_table['subject_name'].unique()
		self.move_unused_to_used()
		self.unused_subject_list = os.listdir(unused_sheets_path + '/' + study_id)

		self.n_enrolled_subj = len(self.enrolled_subjects_list)
		self.n_unused_subject_sheets = len(self.unused_subject_list)

	def move_unused_to_used(self):
		for enrolled_subject in self.enrolled_subjects_list:
			unused_sheet = unused_sheets_path + '/' + self.study_id + '/' + enrolled_subject + '.pdf'
			if os.path.isfile(unused_sheet):
				os.rename(unused_sheet, used_sheets_path + '/' + self.study_id + '/' + enrolled_subject + '.pdf')

		study_sheets_path = unused_sheets_path + '/' + self.study_id
		if os.path.isfile(study_sheets_path + '_subject_sheets.zip'):
			os.remove(study_sheets_path + '_subject_sheets.zip')
		os.system('zip ' + study_sheets_path + '_subject_sheets.zip ' + study_sheets_path + '/*.pdf')

	def get_study_csv_as_dataframe(self):
		"""This function returns a pandas dataframe object containing  data of the requested csv file

				Parameters
				----------
				study_id
					id of selected study

				Returns
				-------
					Pandas dataframe containing all the subjects information.
		"""

		csv_file = storage_folder + '/' + csv_prefix + self.study_id + '.csv'
		if os.path.isfile(csv_file):
			df = pd.read_csv(csv_file)
		else:
			df = pd.DataFrame(columns=['subject_name'])
		return df

	def get_study_json(self):
		study_json_file_path = studies_folder + '/' + self.study_id + "/" + self.study_id + ".json"
		with open(study_json_file_path, 'r') as f:
			data = json.load(f)
		return data

	def get_user_data_table(self):
		"""This function returns a div displaying subjects' information which is stored in the data set for the study

			Parameters
			----------
			 study_id
				 id of selected study

			Returns
			-------
				 Dcc-Table containing all the subjects information.
		"""

		if self.enrolled_subjects_table is not None:

			study_df = pd.DataFrame.dropna(self.enrolled_subjects_table.replace(to_replace='none', value=np.nan), axis=1, how='all')

			return dash_table.DataTable(
				id='table',
				columns=[{"name": i, "id": i} for i in study_df.columns],
				data=study_df.to_dict('records'),
			)
		else:
			return html.P('No data available (.csv file not available or empty)!')

	def get_study_info_div(self):
		"""Returns information of specified study as a div

				Parameters
				----------
					study_id
						id of selected study (within storage folder)

				Return
				-------
					Study information div
		"""

		try:
			return html.Div([
				html.Br(),
				html.Div(children=html.Span(id='create-users-output-state')),
				html.Br(),
				self.get_user_data_table(),
				html.Br(),
				html.Div(children=html.A(id='download-sheet-zip', children='Download study sheets'), style={'padding-top': '8px'}),
			])
		except FileNotFoundError:
			return html.P('Study not created appropriately (JSON missing)!')
