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
    description = study_json["description"]
    n_enrolled_subject_list = len(get_enrolled_app_users_from_json(study_json))

    active_sensors_div = html.P('Sensors: ' + ', '.join(study_json["sensor-list"])) if 'sensor-list' in study_json else ''
    ema_active_json = html.P('EMA modality: active') if 'survey' in study_json else ''

    return html.Div(id='study-info', children=[
        html.P(description),
        html.P('Study duration: ' + str(duration) + ' days'),
        html.P(id='total-subjects', children='Total number of subjects: ' + str(total_number_subjects)),
        html.Div(id='create-subject-div', children=[
            dcc.Input(id='create-additional-subjects-input', placeholder='Number of new subjects', type='number',
                      min='0'),
            html.Button(id='create-additional-subjects-button', children='Create new subjects')]),
        html.P('Number of enrolled subjects: ' + str(n_enrolled_subject_list)),
        active_sensors_div,
        ema_active_json
    ])



