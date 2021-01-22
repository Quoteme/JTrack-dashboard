import dash_html_components as html
from datetime import datetime

from study import modalities, timestamp_format, sensors_per_modality_dict
from study.display_study.study_data import get_user_list


def get_study_data_table(study_json, study_df):
	"""
	This function returns a div displaying subjects' information which is stored in the data set for the study

	:return: Html-Table containing all the enrolled subjects information
	"""

	header = get_study_table_header(study_df)
	body, missing_data_dict, active_users_dict = get_study_table_body(study_json, study_df)
	study_table = html.Table(id='study-table', children=[html.Thead(header), html.Tbody(body)])

	return html.Div(id='study-table-and-legend-div', children=[
		html.Div(id='study-table-div', children=study_table),
		html.Div(id='legend-div', className='row', children=[
			html.Div(id='color-legend-div', children=get_color_legend()),
			html.Div(id='status-code-legend-div', children=get_status_code_legend())])]), missing_data_dict, active_users_dict


def get_color_legend():
	"""
	color legend beneath the table to identify meaning of highlights
	:return: unordered list with color information
	"""
	return html.Ul(children=[
		html.Li("No data sent for 2 days", className='red'),
		html.Li("Left study too early", className='blue'),
		html.Li("Study duration reached, not left", className='light-green'),
		html.Li("Study duration reached, left", className='dark-green'),
		html.Li("Multiple QR Codes of one user active", className='orange')
	])


def get_status_code_legend():
	"""
	legend for status codes empty,1,2
	:return:
	"""
	return html.Ul(children=[
		html.Li("Empty - Everything is fine"),
		html.Li("1 - User left study with this QR Code"),
		html.Li("2 - User reached study duration and left automatically"),
		html.Li("3 - Missing data")
	])


def get_study_table_header(study_df):
	"""
	retrieves header for the html table, if there is a sensor that should not be in the study and has data it will be highlighted

	:param study_df: study data frame
	:return: dash html table row which will be the header row
	"""
	header_row = [html.Th(children='user', className='clean')]
	for col in study_df.columns:
		header_row.append(html.Th(children=col, className='clean'))
	return html.Tr(header_row)


def get_study_table_body(study_json, study_df):
	"""
	create dash html body, iterates over a list of app user objects which contain necessary information about each user. The actual list of
	active users is returned by get_enrolled_app_users_from_json

	:param study_json:
	:param study_df:
	:return:
	"""
	table_rows = []
	missing_data = {modality: set() for modality in modalities}
	active_users = {modality: set() for modality in modalities}

	for user in get_user_list(study_df):
		user_data = study_df[study_df['id'].str.match(user)].reset_index(drop=True)

		for index, row in user_data.iterrows():
			row_dict = {column: html.Td(value) for column, value in row.items()}

			check_for_missing_data(row_dict, missing_data)
			give_color(row_dict, missing_data, active_users, study_json, user_data)

			row = put_user_name_in_front(row_dict, index, user, study_json)
			table_rows.append(html.Tr(row))

	return table_rows, missing_data, active_users


def check_for_missing_data(row_dict, missing_data):
	sensors = [sensor_key.split(' ')[0] for sensor_key in row_dict.keys() if 'n_batches' in sensor_key]

	time_registered = datetime.strptime(row_dict["date_registered"].children, timestamp_format)
	time_left = datetime.strptime(row_dict["date_left_study"].children, timestamp_format) if row_dict["date_left_study"].children != "" else None

	ltr_list = [sensor + ' last_time_received' for sensor in sensors if sensor in sensors_per_modality_dict[row_dict["app"].children]]
	time_last_possible_batch = time_left or datetime.now()

	for ltr in ltr_list:
		timestamp_ltr = row_dict[ltr].children
		time_ltr = datetime.strptime(timestamp_ltr, timestamp_format) if timestamp_ltr != "" else time_registered
		days_since_last_received = (time_last_possible_batch - time_ltr).days

		if days_since_last_received >= 2:
			row_dict[ltr] = html.Td(children=timestamp_ltr, className='red')

			if not time_left:
				missing_data[row_dict["app"].children].add(row_dict['id'].children)


def give_color(row_dict, missing_data, active_users, study_json, user_data):
	"""
	Highlight cells if conditions are true:
	red: delayed sensor data (>= 2 days)
	light-green: study duration reached, but not left
	dark-green: study duration reached,  left
	blue: left prematurely

	:param row_dict: dictionary with user's id data
	:return: edited row, returned as list without the dictionary keys (order remains still correct to match the header of the html table in Study.py)
	"""
	id_color = ''

	time_registered = datetime.strptime(row_dict["date_registered"].children, timestamp_format)
	time_left = datetime.strptime(row_dict["date_left_study"].children, timestamp_format) if row_dict["date_left_study"].children != "" else None
	days_in_study = int(str(row_dict["time_in_study"].children).split(" ")[0])
	study_duration = study_json["duration"]

	if not time_left:
		active_users[row_dict["app"].children].add(row_dict['id'].children)

		if check_multi_registration(row_dict, user_data):
			id_color = 'orange'
		elif days_in_study > int(study_duration):
			id_color = 'light-green'
		elif row_dict['id'].children in missing_data[row_dict["app"].children]:
			id_color = 'red'
	else:
		if (time_left - time_registered).days >= int(study_duration):
			id_color = 'dark-green'
		elif (time_left - time_registered).days < int(study_duration):
			id_color = 'blue'

	row_dict['id'] = html.Td(children=row_dict['id'].children, className=id_color)


def check_multi_registration(row_dict, user_data):
	"""
	check if there are multiple registrations (active qr codes) of one user. Look if more than one entry of date_left_study is empty
	:return: true if multiple qr codes are active
	"""
	time_left_col = user_data[user_data["app"] == row_dict["app"].children]["date_left_study"]
	not_left = time_left_col[time_left_col == '']
	if not_left.size > 1:
		return True
	return False


def put_user_name_in_front(row_dict, index, user, study_json):
	"""
	Put the username as a download link in front of the row if it is the first id

	:param study_json:
	:param user:
	:param index: index of the row, according to overall number of qr code activations
	:param row: row
	:return:
	"""
	row = list(row_dict.values())

	if index == 0:
		row.insert(0, html.Td(html.A(children=user, href='download-' + study_json["name"] + '-' + user)))
	else:
		row.insert(0, html.Td(''))
	return row
