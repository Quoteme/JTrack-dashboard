import dash_core_components as dcc
import dash_html_components as html
import os


def get_current_studies_div(study_dir):
    study_list = []
    current_studies = os.listdir(study_dir)
    for study in current_studies:
        study_list.append({'label': study, 'value': study})
    return html.Div(id='current-studies-div', children=[html.H2('Current Studies'),
                                                        dcc.Dropdown(id='current-study-list', options=study_list),
                                                        html.Div(id='current-selected-study')
                                                        ])


def get_study_info_div(selected_study_dir):
    n_subj = get_number_enrolled_subjects(selected_study_dir)
    return html.Div([
        html.H2(children=str(selected_study_dir).split('/')[-1]),
        html.P(id='number-enrolled-subjects', children='Number of enrolled subjects:\t' + n_subj),
        html.Div(id='create-users-div', children=[
            dcc.Input(id='create_users_input', placeholder='Enter number of new participants', type='number'),
            html.Button(id='create-users-button', children='Create users'),
            html.Br(),
            html.Span(id='create-users-output-state')])
    ])


def get_number_enrolled_subjects(selected_study_dir):
    enrolled_subjects = os.listdir(selected_study_dir)
    n_subj = str(len(enrolled_subjects)-1)
    return n_subj
