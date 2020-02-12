import os

from jutrack_dashboard_worker import studies_folder, storage_folder, csv_prefix
import json
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


def get_user_data_table(study_id):
    """This function returns a div displaying subjects' information which is stored in the data set for the study

        Parameters
        ----------
         study_id
             id of selected study

        Returns
        -------
             Dcc-Table containing all the subjects information.
    """

    study_df = get_study_csv_as_dataframe(study_id)
    if study_df is not None:

        # Header
        columns = [html.Tr([html.Th(col) for col in study_df.columns])]

        # Data
        rows = [html.Tr([html.Td(study_df.iloc[i][col]) for col in study_df.columns]) for i in range(len(study_df))]
        return html.Table(
            columns + rows, style={'width': '90%', 'height': '480px'}
        )
    else:
        return html.P('No data available (.csv file not available)!')


def get_study_info_div(study_id):
    """Returns information of specified study as a div

            Parameters
            ----------
             study_id
                 id of selected study (within storage folder)

            Return
            -------
                 Study information div
    """

    study_json_file_path = studies_folder + '/' + study_id + "/" + study_id + ".json"

    try:
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
                get_user_data_table(study_id),
                html.Br(),
                html.Div(children=html.A(id='download-sheet-zip', children='Download study sheets'),
                         style={'padding-top': '8px'}),
            ])
        ])
    except FileNotFoundError:
        return html.P('Study not created appropriately (JSON missing)!')


def get_study_csv_as_dataframe(study_id):
    """This function returns a pandas dataframe object containing  data of the requested csv file

           Parameters
           ----------
            study_id
                id of selected study

           Returns
           -------
                Pandas dataframe containing all the subjects information.
       """

    csv_file = storage_folder + '/' + csv_prefix + study_id + '.csv'
    if os.path.isfile(csv_file):
        return pd.read_csv(csv_file)
    else:
        return None



