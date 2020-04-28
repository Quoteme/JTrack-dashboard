import dash_core_components as dcc
import dash_html_components as html
from jutrack_dashboard_worker import list_studies, get_sensor_list, get_study_list_as_dict


def create_menu():
    """
    Create the menu list on the left site of the page

    :return: Div containing buttons for navigation

    """

    return html.Div(id='menu-items', style={'padding': '12px'}, children=[
        html.Button(id='create-button', children='Create Study', className='menu-button'),
        html.Br(),
        html.Button(id='current-studies', children='Current Studies', className='menu-button'),
        html.Br(),
        html.Button(id='close-button', children='Close Study', className='menu-button'),
        html.Br(),
        html.Button(id='about-button', children='About', className='menu-button'),
        html.Br(),
        html.Button(id='home-button', children='Home', className='menu-button')
    ])


def get_create_study_div():
    """
    Returns the create study div

    :return: Create study div containing: title, input fields for study name, study duration and number of subjects and
            a list containing sensor + checkboxes
    """

    sensor_checkboxes = [{'label': sensor, 'value': sensor} for sensor in get_sensor_list()]
    frequencies = [{'label': str(freq) + 'Hz', 'value': freq} for freq in [50, 100, 150, 200]]

    return html.Div([
        html.H2(children='Create new study'),
        html.Div(children=[html.Span(children='Study name: ', style={'padding-right': '49px'}),
                           dcc.Input(id='create-study-name-input', placeholder='Your study', type='text')]),
        html.Div(children=[html.Span(children='Study duration: ', style={'padding-right': '30px'}),
                           dcc.Input(id='create-study-duration-input', placeholder='Days', type='number', min='1')]),
        html.Div(children=[html.Span(children='Number of subjects: '),
                           dcc.Input(id='create-study-subject-number', placeholder='Number of subjects', type='number',
                                     min='0')]),
        html.Div(children=[html.P(children='Study description:'),
                           dcc.Textarea(id='create-study-description', placeholder="Enter study description",
                                        maxLength='256',
                                        style={'height': '48px', 'width': '25%'})]),
        html.Br(),
        html.Div(children=[html.P(children='Recording frequency: ', style={'padding-top': '8px'}),
                           dcc.Dropdown(className='column-medium', id='frequency-list', options=frequencies)],
                 style={'margin-top': '8px'}),
        html.Br(),
        html.Br(),
        html.Div(style={'margin-bottom': '96px'}, children=[html.P(children='Sensors: '),
                                                            dcc.Dropdown(className='column-medium', id='create-study-sensors-checklist',
                                                                         options=sensor_checkboxes, multi=True, style={'margin-top': '8px'})]),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Button(id='create-study-button', children='Create', style={'margin-top': '24px'}),
        # is filled if user tries to create study, reset also other input fields
        dcc.Loading(id='loading-create-study',
                    children=[html.P(id='create-study-output-state', style={'padding-top': '30px'})], type='circle')
    ])


def get_current_studies_div():
    """
    Returns the current studies div

    :return: Current studies div

    """

    study_list = get_study_list_as_dict()

    return html.Div(id='current-studies-div', children=[
        html.Div(id='current-study-div', className='column-big', children=[
            html.H2('Current Studies'),
            html.Div(className='column-medium', children=dcc.Dropdown(id='current-study-list', options=study_list)),
            html.Br(),
            # is filled when study is selected
            html.Div(id='current-selected-study', className='row', style={'padding-top': '24px'}),
        ])
    ])


def get_close_study_div():
    """
    Returns the current studies div

    :return: Current studies div
    """

    study_list = get_study_list_as_dict()

    return html.Div(id='close-studies-div', children=[
        html.Div(id='close-study-div', className='column-big', children=[
            html.H2('Close Studies'),
            html.Div(className='column-medium', children=dcc.Dropdown(id='close-study-list', options=study_list)),
            html.Br(),
            html.Br(),
            html.Button(id='close-study-button', children='Close study'),
            html.Br(),
            html.Div(id='close-selected-study-output-state', className='row', style={'padding-top': '24px'}),
        ])
    ])


def get_about_div():
    """
    Returns the about div

    :return: About Div
    """

    return html.Div(id='about1-div', children=html.P(id='about1-p', children=[
        html.H2(children='About'),
        html.P('This application serves as a interface between Jutrack Service and researchers or study leaders. '
               'It provides different methods like creating new studies or displaying currently available information to studies.'),
        html.Div(children=[
            html.Span('Responsible: '),
            html.A('Michael Stolz',
                   href='https://www.fz-juelich.de/inm/inm-7/EN/UeberUns/Mitarbeiter/mitarbeiter_node.html?cms_notFirst=true&cms_docId=2552232')]),
        html.Br(),
        html.Div(children=[
            html.Span('Mail to: '),
            html.A('m.stolz@fz-juelich.de', href='mailto:m.stolz@fz-juelich.de')])
    ]))
