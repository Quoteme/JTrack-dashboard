import dash_core_components as dcc
import dash_html_components as html
from jutrack_dashboard_worker import list_studies, get_sensor_list


def create_menu():
    """Create the menu list on the left site of the page

            Returns
            -------
            Div containing buttons for navigation
    """

    return html.Div(id='menu-items', style={'padding': '12px'}, children=[
        html.Button(id='create-button', children='Create Study'),
        html.Br(),
        html.Button(id='current-studies', children='Current Studies'),
        html.Br(),
        html.Button(id='about-button', children='About')
    ])


def get_create_study_div():
    """Returns the create study div

            Return
            -------
            Create study div containing: title, input fields for study name, study duration and number of subjects and
            a list containing sensor + checkboxes
    """

    sensor_checkboxes = [{'label': sensor, 'value': sensor} for sensor in get_sensor_list()]

    return html.Div([
        html.H2(children='Create new study'),
        html.Div(children=[html.Span(children='Study name: ', style={'padding-right': '49px'}),
                           dcc.Input(id='create-study-name-input', placeholder='Your study', type='text')]),
        html.Div(children=[html.Span(children='Study duration: ', style={'padding-right': '30px'}),
                           dcc.Input(id='create-study-duration-input', placeholder='Days', type='number', min='1')]),
        html.Div(children=[html.Span(children='Number of subjects: '),
                           dcc.Input(id='create-study-subject-number', placeholder='Number of subjects', type='number',
                                     min='0')]),
        html.Div(children=[html.Span(children='Study description:', style={'padding-right': '16px'}),
                           dcc.Textarea(id='create-study-description', placeholder="Enter study description", maxLength='128',
                                        style={'height': '48px', 'widht': '96px', 'margin-top': '12px'})]),
        html.Br(),
        html.Div(children=[html.Span(children='Sensors: '),
                           dcc.Checklist(id='create-study-sensors-checklist', options=sensor_checkboxes,
                                         labelStyle={'display': 'block'},
                                         style={'margin-left': '132px', 'margin-top': '-18px'})]),
        html.Button(id='create-study-button', children='Create', style={'margin-top': '24px'}),
        # is filled if user tries to create study, reset also other input fields
        dcc.Loading(id='loading-create-study', children=[html.P(id='create-study-output-state', style={'padding-top': '30px'})], type='circle')
    ])


def get_current_studies_div():
    """Returns the current studies div

            Return
            ------
            Current studies div
    """

    current_studies = list_studies()
    study_list = []
    for study in current_studies:
        study_list.append({'label': study, 'value': study})
    return html.Div(id='current-studies-div', children=[
        html.Div(id='current-study-div', className='column-big', children=[
            html.H2('Current Studies'),
            html.Div(className='column-medium', children=dcc.Dropdown(id='current-study-list', options=study_list)),
            html.Br(),
            # is filled when study is selected
            dcc.Loading(id='loading-current-study', children=[html.Div(id='current-selected-study', className='row', style={'padding-top': '24px'})],
                        type='circle')
        ])
    ])


def get_about_div():
    """Returns the about div

            Return
            ------
            About Div
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
