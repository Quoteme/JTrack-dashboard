import dash_html_components as html
import dash_core_components as dcc


def get_current_studies_div():
    """
    Returns the current studies div

    :return: Current studies div

    """

    study_list = get_study_list_as_dict()

    return html.Div(id='current-study-div', children=[
            html.H2('Current Studies'),
            html.Div(dcc.Dropdown(id='current-study-list', options=study_list)),
            # is filled when study is selected
            dcc.Loading(html.Div(id='study-info-wrapper'), type='circle'),
            html.Div(id='download-unused-sheets-link-wrapper'),
            html.Div(id='study-data-wrapper'),
            html.Div(id='push-notification-wrapper')
    ])