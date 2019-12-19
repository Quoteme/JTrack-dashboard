import dash_core_components as dcc
import dash_html_components as html
import os


def get_delete_study_div(study_dir):
    """Returns the delete study div

            Parameters
            ----------
                study_dir
                    path to chosen study directory

            Return
            -------
            Delete study div
    """

    study_list = []
    current_studies = os.listdir(study_dir)
    try:
        current_studies.remove('.DS_Store')
    except ValueError:
        pass

    for study in current_studies:
        study_list.append({'label': study, 'value': study})
    return html.Div(id='delete-study-div', children=[
        html.Div(id='delete-study-sub-div', className='column-big',
                 children=[html.H2(children='Delete study', id='delete-study-title'),
                           dcc.Dropdown(id='delete-study-list', options=study_list),
                           html.Button(id='delete-study-button', children='Delete'),
                           html.Br(),
                           html.Div(id='delete-study-output-state'),
                           html.Br(),
                           ])
    ])


def refresh_drop_down(studies_dir):
    """Returns the create study div

            Parameters
            ----------
                studies_dir
                    path to studies ('./studies')

            Return
            -------
            List of remaining studies
    """

    study_list = []
    current_studies = os.listdir(studies_dir)
    try:
        current_studies.remove('.DS_Store')
    except ValueError:
        pass
    for study in current_studies:
        study_list.append({'label': study, 'value': study})

    return study_list
