import base64
import json

import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Output, Input, State

from app import app
from exceptions.Exceptions import StudyAlreadyExistsException
from study import ema, passive_monitoring
from study.create_study.create import create_study
from study.create_study.layout import get_ema_part, get_passive_monitoring_part, uploaded_div


@app.callback(Output('create-study-output-state', 'children'),
			  [Input('create-study-button', 'n_clicks')],
			  [State('modality-list', 'value'),
			   State('study-details', 'data'),
			   State('ema-details', 'data'),
			   State('passive-monitoring-details', 'data')])
def create_study_callback(create_btn, modality_list, study_data, ema_data, passive_monitoring_data):
	"""
	 Callback to create a new study on button click. Reacting if the create study button is clicked. Creates a new study
	if input field contains a valid input und the study does not exist yet.
	"""

	if create_btn:
		study_dict = {}

		if not modality_list:
			return 'Please select at least one modality!'

		if not (study_data['name'] and study_data['duration'] and study_data['number-of-subjects']):
			return 'Please fill out general study information(*)!'
		study_dict.update(study_data)

		if ema in modality_list:
			if not ema_data['survey']:
				return 'Please upload JSON file for EMA(*)!'
			study_dict.update(ema_data)

		if passive_monitoring in modality_list:
			if not (passive_monitoring_data['frequency'] and passive_monitoring_data['sensor-list']):
				return 'Please specify frequency and sensors(*)!'
			study_dict.update(passive_monitoring_data)

		try:
			create_study(study_dict)
			return 'Study created!'
		except StudyAlreadyExistsException:
			return 'Study already exists!'

	raise PreventUpdate


@app.callback(Output('data-div', 'children'),
			  [Input('modality-list', 'value')])
def update_data_div_callback(modaliy_checklist_values):
	if modaliy_checklist_values:
		ema_div = get_ema_part() if ema in modaliy_checklist_values else ''
		passive_monitoring_div = get_passive_monitoring_part() if passive_monitoring in modaliy_checklist_values else ''
		return [ema_div, passive_monitoring_div]
	else:
		PreventUpdate


@app.callback([Output('name-upload-json', 'children'),
			   Output('name-upload-images', 'children')],
			  [Input('upload-ema-json', 'filename'),
			   Input('upload-ema-images', 'filename')])
def update_uploaded_ema_details_callback(json_filename, zip_filename):
	json_div = uploaded_div(json_filename) if json_filename else ''
	zip_div = uploaded_div(zip_filename) if zip_filename else ''
	return [json_div, zip_div]


@app.callback(Output('study-details', 'data'),
			  [Input('create-study-name', 'value'),
			   Input('create-study-duration', 'value'),
			   Input('create-subject-number', 'value'),
			   Input('create-study-description', 'value')],
			  State('study-details', 'data'))
def update_study_details_callback(name, duration, subject_number, description, data):
	data = data or get_default_study_details_dict()
	data['name'] = name
	data['duration'] = duration
	data['number-of-subjects'] = subject_number
	data['description'] = description
	return data


@app.callback(Output('ema-details', 'data'),
			  [Input('upload-ema-json', 'contents'),
			   Input('upload-ema-images', 'contents')],
			  State('ema-details', 'data'))
def update_ema_details_callback(ema_json, ema_images_zip, data):
	data = data or get_default_ema_details_dict()

	ctx = dash.callback_context
	if len(ctx.triggered) > 0:
		if ctx.triggered[0]['value']:
			button_id = ctx.triggered[0]['prop_id'].split('.')[0]

			if button_id == 'upload-ema-json':
				_, ema_json_content = ema_json.split(',')
				ema_json_bytes = base64.b64decode(ema_json_content)
				data['survey'] = json.loads(ema_json_bytes)

			elif button_id == 'upload-ema-images':
				_, ema_images_content = ema_images_zip.split(',')
				data['images'] = ema_images_content
	return data


@app.callback(Output('passive-monitoring-details', 'data'),
			  [Input('frequency-list', 'value'),
			   Input('create-study-sensors-list', 'value')],
			  State('passive-monitoring-details', 'data'))
def update_passive_monitoring_details_callback(frequency, sensor_list, data):
	data = data or get_default_passive_monitoring_details_dict()
	data['frequency'] = frequency
	data['sensor-list'] = sensor_list
	return data


def get_default_study_details_dict():
	return {
		'name': None,
		'duration': None,
		'number-of-subjects': None,
		'description': None,
		'enrolled-subjects': [],
		'sensor-list': []
	}


def get_default_ema_details_dict():
	return {
		'survey': None,
		'images': None
	}


def get_default_passive_monitoring_details_dict():
	return {
		'frequency': None,
		'sensor-list': None
	}
