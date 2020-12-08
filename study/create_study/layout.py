import dash_core_components as dcc
import dash_html_components as html

from study import get_sensor_list


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
                               dcc.Dropdown(id='create-study-sensors-list', options=sensor_checkboxes, multi=True)])]),
        html.Button(id='create-study-button', children='Create'),
        dcc.Upload(id='upload-ema-json', children=html.Div(['Drag and Drop or ', html.A('Select JSON File')]),
                   style={
                       'width': '25%',
                       'height': '60px',
                       'lineHeight': '60px',
                       'borderWidth': '1px',
                       'borderStyle': 'dashed',
                       'borderRadius': '5px',
                       'textAlign': 'center',
                       'margin': '10px'
                   },
                   multiple=False,
                   accept='application/json'),
        # is filled if user tries to create study, reset also other input fields
        dcc.Loading(id='loading-create-study', children=[html.P(id='create-study-output-state')], type='circle')
    ])



