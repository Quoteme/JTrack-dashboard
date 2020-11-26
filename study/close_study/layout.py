import dash_core_components as dcc
import dash_html_components as html


def get_close_study_div():
    """
    Returns the close studies div

    :return: close studies div
    """

    study_list = get_study_list_as_dict()

    return html.Div(id='close-studies-div', children=[
            html.H2('Close Studies'),
            html.Div(children=dcc.Dropdown(id='close-study-list', options=study_list)),
            html.Button(id='close-study-button', children='Close study'),
            html.P(id='close-selected-study-output-state'),
            dcc.ConfirmDialog(id='close-study-confirm-dialog', message='Please confirm closing the study'),
    ])


