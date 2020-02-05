import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import os


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

    n_subj = '4'
    return html.Div([
        html.P(id='number-enrolled-subjects', children='Number of enrolled subjects:\t' + n_subj),
        html.Div(id='create-users-div', children=[
            dcc.Input(id='create_users_input', placeholder='Enter number of new participants', type='number'),
            html.Button(id='create-users-button', children='Create new subjects'),
            html.Br(),
            html.Div(children=html.Span(id='create-users-output-state')),
            html.Br(),
            html.Div(
                children=html.A(id='download-pdfs-button', children='Download subject sheets', href='/download_pdfs/'),
                style={'padding-top': '8px'}),
            html.Br(),
            get_user_data_table(selected_study_dir)
        ])
    ])



