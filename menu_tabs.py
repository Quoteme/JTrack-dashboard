import dash_core_components as dcc
import dash_html_components as html
from jutrack_dashboard_worker import get_sensor_list, get_study_list_as_dict


def get_create_study_div():
    """
    Returns the create study div

    :return: Create study div containing: title, input fields for study name, study duration and number of subjects and
            a list containing sensor + checkboxes
    """

    sensor_checkboxes = [{'label': sensor, 'value': sensor} for sensor in get_sensor_list()]
    frequencies = [{'label': str(freq) + 'Hz', 'value': freq} for freq in [50, 100, 150, 200]]

    return html.Div(id='create-study-div', children=[
        html.H2(children='Create new study'),
        html.Div(id='data-div', children=[
            html.Div(children=[html.Span(className='create-span', children='Study name:'),
                               dcc.Input(id='create-study-name-input', placeholder='Your study', type='text')]),
            html.Div(children=[html.Span(className='create-span', children='Study duration:'),
                               dcc.Input(id='create-study-duration-input', placeholder='Days', type='number', min='1')]),
            html.Div(children=[html.Span(className='create-span', children='Number of subjects:'),
                               dcc.Input(id='create-study-subject-number', placeholder='Number of subjects', type='number', min='0')]),
            html.Div(children=[html.Span(className='create-span', children='Study description:'),
                               dcc.Textarea(id='create-study-description', placeholder="Enter study description", maxLength='500')]),
            html.Div(children=[html.Span(className='create-span', children='Recording frequency:'),
                               dcc.Dropdown(id='frequency-list', options=frequencies)]),
            html.Div(id='sensors', children=[html.Span(className='create-span', children='Sensors:'),
                               dcc.Dropdown(id='create-study-sensors-checklist', options=sensor_checkboxes, multi=True)])]),
        html.Button(id='create-study-button', children='Create'),
        # is filled if user tries to create study, reset also other input fields
        dcc.Loading(id='loading-create-study', children=[html.P(id='create-study-output-state')], type='circle')
    ])


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
            html.Div(id='study-table-wrapper')
    ])


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
    ])


def get_about_div():
    """
    Returns the about div

    :return: About Div
    """

    return html.Div(id='about-div', children=[
        html.H2(children='About'),
        html.P('This application serves as a interface between Jutrack Service and researchers or study leaders. '
               'It provides different methods like creating new studies or displaying currently available information to studies.'),
        html.P(children=['Responsible: ', html.A('Michael Stolz', href='https://www.fz-juelich.de/inm/inm-7/EN/UeberUns/Mitarbeiter/mitarbeiter_node.html?cms_notFirst=true&cms_docId=2552232')]),
        html.P(children=['Mail to: ', html.A('m.stolz@fz-juelich.de', href='mailto:m.stolz@fz-juelich.de')])])
