import dash_core_components as dcc
import dash_html_components as html
import os


def get_current_studies_div(study_dir):
    """Returns the current studies div

            Parameters
            ----------
                study_dir
                    path to chosen study directory

            Return
            -------
            Current studies div
    """

    study_list = []
    current_studies = os.listdir(study_dir)
    current_studies.remove('.DS_Store')
    for study in current_studies:
        study_list.append({'label': study, 'value': study})
    return html.Div(id='current-studies-div', children=[
        html.Div(id='current-study-div', className='column-big', children=[html.H2('Current Studies'),
                                                                           dcc.Dropdown(id='current-study-list',
                                                                                        options=study_list),
                                                                           html.Div(id='current-selected-study')
                                                                           ]),
        html.Div(id='enrolled-subjects', style={'float': 'right'}, className='column',
                 )
    ])


def get_study_info_div(selected_study_dir):
    """Returns information of specified study as a div

            Parameters
            ----------
                selected_study_dir
                    path to selected study ('./studies/study_name')

            Return
            -------
            Study information div
    """

    n_subj = get_number_enrolled_subjects(selected_study_dir)
    return html.Div([
        html.P(id='number-enrolled-subjects', children='Number of enrolled subjects:\t' + n_subj),
        html.Div(id='create-users-div', children=[
            dcc.Input(id='create_users_input', placeholder='Enter number of new participants', type='number'),
            html.Button(id='create-users-button', children='Create users'),
            html.Br(),
            html.Span(id='create-users-output-state')])
    ])


def get_number_enrolled_subjects(selected_study_dir):
    """Returns the create study div

            Parameters
            ----------
                selected_study_dir
                    path to selected study ('./studies/study_name')

            Return
            -------
            Number of enrolled subjects in given study

    """
    enrolled_subjects = os.listdir(selected_study_dir)
    n_subj = str(max(0, len(enrolled_subjects) - 2))
    return n_subj


def get_list_enrolled_subjects(study_dir):
    enrolled_subject_list = os.listdir(study_dir)
    try:
        enrolled_subject_list.remove('subject-sheets')
    except ValueError:
        pass
    try:
        enrolled_subject_list.remove('QR-Codes')
    except ValueError:
        pass
    try:
        enrolled_subject_list.remove('.DS_Store')
    except ValueError:
        pass
    return enrolled_subject_list


def get_enrolled_subjects_div(study_dir):
    subjects = []
    subject_sheets = study_dir + '/subject-sheets'
    enrolled_subjects_list = get_list_enrolled_subjects(study_dir)

    for subj in enrolled_subjects_list:
        subjects.append({'label': subj, 'value': subj})

    dropdown = dcc.Dropdown(id='checklist', options=subjects)

    return html.Div(id='enrolled-subjects-div', children=[html.H3('Enrolled Subjects'), dropdown])
