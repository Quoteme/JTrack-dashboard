import dash_html_components as html


def get_study_data_table(study_df, user_list):
	"""
	This function returns a div displaying subjects' information which is stored in the data set for the study

	:return: Html-Table containing all the enrolled subjects information
	"""
	return html.Div(id='study-table-and-legend-div', children=[
		html.Div(id='study-table-div', children=generate_html_table(study_df, user_list)),
		html.Div(id='legend-div', className='row', children=[
			html.Div(id='color-legend-div', children=get_color_legend()),
			html.Div(id='status-code-legend-div', children=get_status_code_legend())])])


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


def generate_html_table(study_df, user_list):
	"""
	generate html table with dash containing header and data body

	:param study_df: study data frame
	:return: dash html table
	"""
	header = get_study_table_header(study_df)
	body = get_study_table_body(user_list)
	return html.Table(id='study-table', children=[
		html.Thead(header),
		html.Tbody(body)])


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


def get_study_table_body(user_list):
	"""
	create dash html body, iterates over a list of app user objects which contain necessary information about each user. The actual list of
	active users is returned by get_enrolled_app_users_from_json

	:param study_df:
	:return:
	"""
	body = []
	for user in user_list:
		body.extend(user.get_rows_for_user())
	return body

