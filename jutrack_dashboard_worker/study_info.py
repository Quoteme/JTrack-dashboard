from jutrack_dashboard_worker import studies_folder
import json
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt


def get_user_data_table(studys_folder, study_id):
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


def get_study_info_div(study_id):
    """Returns information of specified study as a div

            Parameters
            ----------
                study_id
                    path to selected study ('./studies/study_name')

            Return
            -------
            Study information div
    """

    study_json_file_path = studies_folder + '/' + study_id + "/" + study_id + ".json"

    with open(study_json_file_path, 'r') as f:
        data = json.load(f)
        n_subj = data['number-of-subjects']
    return html.Div([
        html.P(id='number-enrolled-subjects', children='Number of enrolled subjects:\t' + str(n_subj)),
        html.Div(id='create-users-div', children=[
            dcc.Input(id='create_users_input', placeholder='Not working yet', type='number'),
            html.Button(id='create-users-button', children='Create new subjects'),
            html.Br(),
            html.Div(children=html.Span(id='create-users-output-state')),
            html.Br(),
            html.Div(children=html.A(id='download-sheet-zip', children='Download study sheets'), style={'padding-top': '8px'}),
            html.Br(),
            get_user_data_table(studies_folder, study_id)
        ])
    ])



