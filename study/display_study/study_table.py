import pandas as pd
import numpy as np
import dash_html_components as html


from exceptions.Exceptions import EmptyStudyTableException
from study.display_study.AppUser import AppUser


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

	return html.Div(id='study-table-and-legend-div', children=[
		html.Div(id='study-table-div', children=self.generate_html_table(study_df)),
		html.Div(id='legend-div', className='row', children=[
			html.Div(id='color-legend-div', children=self.get_color_legend()),
			html.Div(id='status-code-legend-div', children=self.get_status_code_legend())])])


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
		study_df[sensor + ' last_time_received'] = study_df[sensor + ' last_time_received'].replace(to_replace=['none'],
																									value=np.nan)
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
		self.user_list.append(
			AppUser(user_name=user, data=study_df[study_df['id'].str.match(user)], study_id=self.study_id,
					duration=self.duration))
