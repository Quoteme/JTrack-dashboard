import dash_html_components as html
import dash_core_components as dcc

from study import get_study_list_as_dict, open_study_json, get_enrolled_app_users_from_json, \
    get_enrolled_qr_codes_from_json, get_ids_with_missing_data


def get_current_studies_div():
    """
    Returns the current studies div

    :return: Current studies div

    """

    study_list = get_study_list_as_dict()

    return html.Div(id='current-study-div', children=[
        html.H2('Current Studies'),
        html.Div(dcc.Dropdown(id='current-study-list', options=study_list)),
        # is filled when study is selected
        dcc.Loading(html.Div(id='study-info-div'), type='circle'),
        html.Div(id='download-unused-sheets-link-div'),
        html.Div(id='study-data-div'),
        html.Div(id='push-notification-div')
    ])


def get_study_info_div(study_json):
    """
    Returns information of specified study as a div

    :return: Study information div
    """
    duration = study_json["duration"]
    total_number_subjects = study_json["number-of-subjects"]
    enrolled_subject_list = get_enrolled_app_users_from_json(study_json)
    sensor_list = study_json["sensor-list"]
    description = study_json["description"]

    return html.Div(id='study-info', children=[
        html.P(description),
        html.P('Study duration: ' + str(duration) + ' days'),
        html.P(id='total-subjects', children='Total number of subjects: ' + str(total_number_subjects)),
        html.Div(id='create-subject-div', children=[
            dcc.Input(id='create-additional-subjects-input', placeholder='Number of new subjects', type='number',
                      min='0'),
            html.Button(id='create-additional-subjects-button', children='Create new subjects')]),
        html.P('Number of enrolled subjects: ' + str(len(enrolled_subject_list))),
        html.P('Sensors: '),
        html.Div(children=html.Ul(children=[html.Li(children=sensor) for sensor in sensor_list]))
    ])


def get_push_notification_div(study_json, user_list):
    all_ids = [{'label': enrolled_qr_code, 'value': enrolled_qr_code} for enrolled_qr_code in
               get_enrolled_qr_codes_from_json(study_json)]

    return html.Div(id='push-notification', children=[
        html.H3('Push notifications'),
        html.Div(id='push-notification-information-div', children=[
            html.Div(id='push-notification-title-div',
                     children=dcc.Input(id='push-notification-title', placeholder='Message title', type='text')),
            html.Div(id='push-notification-text-div',
                     children=dcc.Textarea(id='push-notification-text', placeholder='Message text')),
            html.Div(id='push-notification-receiver-list-div', children=[
                dcc.Dropdown(id='receiver-list', options=all_ids, multi=True, placeholder='Receiver...')])]),
        html.Div(id='autofill-button-div', children=[
            html.Button(id='every-user-button', children='All IDs',
                        **{'data-user-list': get_enrolled_qr_codes_from_json(study_json)}),
            html.Button(id='user-with-missing-data-button', children='Missing data IDs',
                        **{'data-user-list': get_ids_with_missing_data(user_list)})]),
        html.Button(id='send-push-notification-button', children='Send notification'),
        html.Div(id='push-notification-output-state')
    ])
