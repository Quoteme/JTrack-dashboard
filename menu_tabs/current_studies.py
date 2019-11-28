import dash_core_components as dcc
import dash_html_components as html
import os


def get_current_studies_div(study_dir):
    study_list = []
    current_studies = os.listdir(study_dir)
    for study in current_studies:
        study_list.append({'label': study, 'value': study})
    return html.Div(id='current-studies-div', children=[dcc.Dropdown(id='study-list', options=study_list),
                                                        html.Div(id='selected-study')])

