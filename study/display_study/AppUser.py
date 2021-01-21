import dash_html_components as html
import pandas as pd
from datetime import datetime

from study import sensors_per_modality_dict

timestamp_format = "%Y-%m-%d %H:%M:%S"


class AppUser:

	def __init__(self, user_name, data, study_id, duration):
		self.user_name = user_name
		self.data = pd.DataFrame(data).sort_values(by=['app', 'id']).reset_index(drop=True)
		self.study_enrolled_in = study_id
		self.study_duration = duration
		self.sensors = [sensor_column.split(' ')[0] for sensor_column in data.columns if 'n_batches' in sensor_column]
		self.ids_with_missing_data = {}

	def get_rows_for_user(self):
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
			row_id.insert(0, html.Td(html.A(children=self.user_name, href='download-' + self.study_enrolled_in + '-' + self.user_name)))
		else:
			row_id.insert(0, html.Td(''))
		return row_id

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

		time_registered = datetime.strptime(row_dict["date_registered"].children, timestamp_format)
		time_left = datetime.strptime(row_dict["date_left_study"].children, timestamp_format) if row_dict["date_left_study"].children != "" else None
		days_in_study = int(str(row_dict["time_in_study"].children).split(" ")[0])

		self.check_for_missing_data(qr_id, row_dict, time_registered, time_left)

		if not time_left:
			if self.check_multi_registration(row_dict):
				id_color = 'orange'
			elif days_in_study > int(self.study_duration):
				id_color = 'light-green'
			elif row_dict["app"].children in self.ids_with_missing_data and qr_id in self.ids_with_missing_data[row_dict["app"].children]:
				id_color = 'red'
		else:
			if (time_left - time_registered).days >= int(self.study_duration):
				id_color = 'dark-green'
			elif (time_left - time_registered).days < int(self.study_duration):
				id_color = 'blue'

		row_dict['id'] = html.Td(children=qr_id, className=id_color)

		return list(row_dict.values())

	def check_multi_registration(self, row_dict):
		"""
		check if there are multiple registrations (active qr codes) of one user. Look if more than one entry of date_left_study is empty
		:return: true if multiple qr codes are active
		"""
		time_left_col = self.data[self.data["app"] == row_dict["app"].children]["date_left_study"]
		not_left = time_left_col[time_left_col == '']
		if not_left.size > 1:
			return True
		return False

	def check_for_missing_data(self, qr_id, row_dict, time_registered, time_left):
		ltr_list = [sensor + ' last_time_received' for sensor in self.sensors if sensor in sensors_per_modality_dict[row_dict["app"].children]]
		time_last_possible_batch = time_left or datetime.now()

		for ltr in ltr_list:
			timestamp_ltr = row_dict[ltr].children
			time_ltr = datetime.strptime(timestamp_ltr, timestamp_format) if timestamp_ltr != "" else time_registered
			days_since_last_received = (time_last_possible_batch - time_ltr).days

			if days_since_last_received >= 2:
				row_dict[ltr] = html.Td(children=timestamp_ltr, className='red')
				if row_dict["app"].children in self.ids_with_missing_data:
					if qr_id not in self.ids_with_missing_data[row_dict["app"].children]:
						self.ids_with_missing_data[row_dict["app"].children].append(qr_id)
				else:
					self.ids_with_missing_data[row_dict["app"].children] = [qr_id]
