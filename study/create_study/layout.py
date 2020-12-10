import dash_core_components as dcc
import dash_html_components as html

from study import sensor_list, frequency_list, modality_list


def get_create_study_div():
    """
    Returns the create study div

    :return: Create study div containing: title, input fields for study name, study duration and number of subjects and
            a list containing sensor + checkboxes
    """

    return html.Div(id='create-study-div', children=[
        html.H2(children='Create new study'),
        html.Div(children=[
            html.Div(children=[html.Span(className='create-span', children='Study name*:'),
                               dcc.Input(id='create-study-name', placeholder='Your study', type='text')]),
            html.Div(children=[html.Span(className='create-span', children='Study duration*:'),
                               dcc.Input(id='create-study-duration', placeholder='Days', type='number', min='1')]),
            html.Div(children=[html.Span(className='create-span', children='Number of subjects*:'),
                               dcc.Input(id='create-subject-number', placeholder='Number of subjects', type='number', min='0')]),
            html.Div(children=[html.Span(className='create-span', children='Study description:'),
                               dcc.Textarea(id='create-study-description', placeholder="Enter study description", maxLength='500')]),
            dcc.Checklist(id='modality-list', options=modality_list, labelStyle={'display': 'block'}),
            html.Div(id='data-div'),
            html.Button(id='create-study-button', children='Create study!'),
            # is filled if user tries to create study, reset also other input fields
            dcc.Loading(children=[html.P(id='create-study-output-state')], type='circle')])])


def get_passive_monitoring_part():
    """
    Create div for passive monitoring details

    :return: passive monitoring div
    """
    sensor_checkboxes = [{'label': sensor, 'value': sensor} for sensor in sensor_list]
    frequencies = [{'label': str(freq) + 'Hz', 'value': freq} for freq in frequency_list]

    return html.Div(id='passive-monitoring-data', children=[
        html.H4('Passive monitoring details'),
        html.Div(children=[html.Span(className='create-span', children='Recording frequency*:'),
                           dcc.Dropdown(id='frequency-list', options=frequencies)]),
        html.Div(id='sensors', children=[html.Span(className='create-span', children='Sensors*:'),
                                         dcc.Dropdown(id='create-study-sensors-list', options=sensor_checkboxes,
                                                      multi=True)]),

    ])


def get_ema_part():
    """
    Create div for ema details

    :return: ema details div
    """

    return html.Div(id='ema-data', children=[
        html.H4('Ecological momentary assessment'),
        html.Span("Upload for EMA JSON file*:"),
        dcc.Upload(id='upload-ema-json', className='upload', children=html.Div(['Drag and Drop or ', html.A('Select JSON File')]),
                   multiple=True,
                   accept='application/json'),
        html.Div(id='name-upload-json'),
        html.Span("Upload for EMA images zip file:"),
        dcc.Upload(id='upload-ema-images', className='upload', children=html.Div(['Drag and Drop or ', html.A('Select ZIP File')]),
                   multiple=True,
                   accept='application/zip '),
        html.Div(id='name-upload-images')
    ])


def uploaded_div(filename):
    return html.Div(filename + ' uploaded!')



