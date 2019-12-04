import dash_core_components as dcc
import dash_html_components as html
import os


def get_create_study_div():
    """Returns the create study div

            Return
            -------
            Create study div
    """

    return html.Div([
        html.H2(children='Create new study', id='create-study-title'),
        dcc.Input(id='create-study-input', placeholder='Your study', type='text'),
        html.Button(id='create-study-button', children='Create'),
        html.Br(),
        html.Div(id='create-study-output-state'),
        html.Br(),
        ])
