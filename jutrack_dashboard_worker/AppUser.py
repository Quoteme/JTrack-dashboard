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
		self.ids_with_missing_data = []

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
		"""
		Create link for downloading the study sheets of the app user
		:return: dash html data cell with link (a)
		"""
		return html.Td(html.A(children=self.user_name, href='download-' + self.study_enrolled_in + '-' + self.user_name))

	def give_color(self, row_dict):
		"""
		Highlight cells if conditions are true:
		red: delayed sensor data (>= 2 days)
		light-green: study duration reached, but not left
		dark-green: study duration reached,  left
		blue: left prematurely

		:param row_dict: dictionary with user's id data
		:return: edited row, returned as list without the dictionary keys (order remains still correct to match the header of the html table in Study.py)
		"""
		qr_id = row_dict['id'].children
		id_color = ''
		registered_timestamp_in_s = datetime.strptime(row_dict["date_registered"].children, timestamp_format)
		left_timestamp_in_s = datetime.strptime(row_dict["date_left_study"].children, timestamp_format) if row_dict["date_left_study"].children != "" else None
		last_mandatory_send_in_s = datetime.now() if not left_timestamp_in_s else left_timestamp_in_s
		time_in_study_days = int(str(row_dict["time_in_study"].children).split(" ")[0])
		last_times_received = [sensor + ' last_time_received' for sensor in self.sensors]
		missing_data = False

		for last_time_received in last_times_received:
			ltr_string = row_dict[last_time_received].children
			ltr_in_s = registered_timestamp_in_s if ltr_string == "" else datetime.strptime(ltr_string, timestamp_format)
			days_since_last_received = (last_mandatory_send_in_s - ltr_in_s).days

			if days_since_last_received >= 2:
				row_dict[last_time_received] = html.Td(children=ltr_string, className='red')
				missing_data = True

		if not left_timestamp_in_s:
			if self.check_multi_registration():
				id_color = 'orange'
			elif time_in_study_days > int(self.study_duration):
				id_color = 'light-green'
			elif missing_data:
				id_color = 'red'
				self.ids_with_missing_data.append(qr_id)
		else:
			if (left_timestamp_in_s - registered_timestamp_in_s).days >= int(self.study_duration):
				id_color = 'dark-green'
			elif (left_timestamp_in_s - registered_timestamp_in_s).days < int(self.study_duration):
				id_color = 'blue'

		row_dict['id'] = html.Td(children=qr_id, className=id_color)

		return list(row_dict.values())

	def check_multi_registration(self):
		"""
		check if there are multiple registrations (active qr codes) of one user. Look if more than one entry of date_left_study is empty
		:return: true if multiple qr codes are active
		"""
		time_left_col = self.data["date_left_study"]
		not_left = time_left_col[time_left_col == '']
		if not_left.size > 1:
			return True
		return False
