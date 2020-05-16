import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import datetime

from jutrack_dashboard_worker import timestamp_format


class AppUser:

	def __init__(self, user_name, data, study_id, duration):
		self.user_name = user_name
		self.data = pd.DataFrame.reset_index(data, drop=True)
		self.study_enrolled_in = study_id
		self.study_duration = duration
		self.sensors = [sensor_column.split(' ')[0] for sensor_column in data.columns if 'n_batches' in sensor_column]

	def get_rows_for_all_ids(self):
		"""
		Get dash html rows for every scanned qr code of one app user. Data is a pandas data frame according to the user's data.
		Iterates through the rows resulting in multiple pandas series resp. dictionaries. Highlighting if certain conditions are true.
		If id is the first one, the username will be added in front of the row.

		:return: A list of dash html table rows containing data. Will be used to extend the overall table in Study.py
		"""
		user_data = []
		for index, row in self.data.iterrows():
			row_dict = {column: html.Td(value) for column, value in row.items()}
			tr_row = self.give_color(row_dict)
			tr_row = self.put_user_name_in_front(index, tr_row)
			user_data.append(html.Tr(tr_row))
		return user_data

	def put_user_name_in_front(self, index, row_id):
		"""
		Put the username as a download link in front of the row if it is the first id

		:param index: index of the row, according to overall number of qr code activations
		:param row_id: row of the id
		:return:
		"""
		if index == 0:
			row_id.insert(0, self.create_download_link_for_user())
		else:
			row_id.insert(0, html.Td(''))
		return row_id

	def create_download_link_for_user(self):
		return html.Td(html.A(children=self.user_name, href='download-' + self.study_enrolled_in + '-' + self.user_name))

	def give_color(self, row_dict):
		id_color = ""
		registered_timestamp = datetime.strptime(row_dict["date_registered"].children, timestamp_format)
		left_timestamp = datetime.strptime(row_dict["date_left_study"].children, timestamp_format) if row_dict["date_left_study"].children != "" else ""
		time_in_study_days = int(str(row_dict["time_in_study"].children).split(" ")[0])
		last_times_received = [sensor + ' last_time_received' for sensor in self.sensors]

		for last_time_received in last_times_received:
			last_time_received_string = row_dict[last_time_received].children

			last_time_received_dt = registered_timestamp if last_time_received_string == "" else datetime.strptime(
				last_time_received_string, timestamp_format)

			days_since_last_received = (datetime.now() - last_time_received_dt).days

			if days_since_last_received >= 2:
				row_dict[last_time_received] = html.Td(children=last_time_received_string, className='red')
				id_color = 'red'

		if left_timestamp == "":
			if time_in_study_days - registered_timestamp.day > int(self.study_duration):
				id_color = 'light-green'

		else:
			if (left_timestamp - registered_timestamp).days >= int(self.study_duration):
				id_color = 'dark-green'
			elif (left_timestamp - registered_timestamp).days < int(self.study_duration):
				id_color = 'blue'

		row_dict['id'] = html.Td(children=row_dict['id'].children, className=id_color)

		return list(row_dict.values())

