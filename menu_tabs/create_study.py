import dash_core_components as dcc
import dash_html_components as html
import os


def get_create_study_div(study_dir):
    return html.Div([
        html.H2(children='Create new study', id='create-study-title'),
        dcc.Input(id='study-name', placeholder='Your study', type='text'),
        html.A(children=html.Button(id='create-study-button', children='Create')),
        html.Br(),
        html.Div(id='output-state'),
        html.Br(),
    ])
