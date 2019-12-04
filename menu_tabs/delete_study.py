import dash_core_components as dcc
import dash_html_components as html
import os


def get_delete_study_div(study_dir):
    study_list = []
    current_studies = os.listdir(study_dir)
    current_studies.remove('.DS_Store')
    for study in current_studies:
        study_list.append({'label': study, 'value': study})

    return html.Div([
        html.H2(children='Delete study', id='delete-study-title'),
        dcc.Dropdown(id='to-delete-study-list', options=study_list),
        html.Button(id='delete-study-button', children='Delete'),
        html.Br(),
        html.Div(id='delete-study-output-state'),
        html.Br(),
    ])


def refresh_drop_down(study_dir):
    study_list = []
    current_studies = os.listdir(study_dir)
    for study in current_studies:
        study_list.append({'label': study, 'value': study})

    return study_list
