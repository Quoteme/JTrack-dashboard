import dash_core_components as dcc
import dash_html_components as html
import os


def get_sensor_list():
    """Retrieves a list of possible used sensors

        Return
        ------
            List of sensors
    """

    sensors = ['Acceleration Sensor', 'App Usage Statistic', 'Barometer',
               'Detected Activity Sensor', 'Gravity', 'Gyroscope', 'Linear Acceleration',
               'Location Sensor', 'Magnetic Sensor', 'Rotation Vector Sensor']
    return sensors


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
        html.Div(children=[html.Span(children='Study duration: ', style={'padding-right': '31px'}),
                           dcc.Input(id='create-study-duration-input', placeholder='Days', type='number', min='0')]),
        html.Div(children=[html.Span(children='Number of subjects: '),
                           dcc.Input(id='create-study-subject-number', placeholder='Number of subjects', type='number', min='0')]),
        html.Br(),
        html.Div(children=[html.Span(children='Sensors: '),
                           dcc.Checklist(id='create-study-sensors', options=sensor_checkboxes,
                                         labelStyle={'display': 'block'}, style={'margin-left': '132px', 'margin-top': '-18px'})]),

        html.Button(id='create-study-button', children='Create', style={'margin-top': '24px'}),
        html.Div(id='create-study-output-state', style={'padding-top': '24px'}),
        ])
