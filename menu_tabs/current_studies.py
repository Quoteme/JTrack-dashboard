import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
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
    try:
        current_studies.remove('.DS_Store')
    except ValueError:
        pass
    for study in current_studies:
        study_list.append({'label': study, 'value': study})
    return html.Div(id='current-studies-div', children=[
        html.Div(id='current-study-div', className='column-big', children=[html.H2('Current Studies'),
                                                                           dcc.Dropdown(id='current-study-list',
                                                                                        options=study_list),
                                                                           html.Div(id='current-selected-study')
                                                                           ])
    ])


def get_user_data_table(selected_study_dir):
    """This function returns a div displaying subjects' information which is stored in the data set for the study

        Parameters
        ----------
            selected_study_dir
                Path to study directory.

        Returns
        -------
            Dcc-Table containing all the subjects information.
    """

    columns = ['SubjectID', 'Date enrolled', 'Days in study', 'Sensors']

    return dt.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in columns],
        style_cell={'textAlign': 'center'},
    )


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
            html.Button(id='create-users-button', children='Create new subjects'),
            html.Br(),
            html.Div(children=html.Span(id='create-users-output-state')),
            html.Br(),
            get_user_data_table(selected_study_dir)
        ])
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
    n_subj = str(max(0, len(enrolled_subjects) - 3))
    return n_subj

