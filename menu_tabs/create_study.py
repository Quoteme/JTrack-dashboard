import dash_core_components as dcc
import dash_html_components as html
import os
from subject_configuration.create_subjects import create_subjects
import xml.etree.cElementTree as ET


def generate_study_meta_xml(study_path, sensors):
    """
    Generates xml file on study creation containing information like name, initial number of subjects and a list
    of selected sensors. Number of subjects is set to 0 in the beginning.

        Parameters
        ----------
            study_path
                Path to study. Also containing the study name in the end.
            sensors
                String list of sensors.
    """

    study_name = str(study_path).split('/')[-1]
    filename = study_name + '-info.xml'

    root = ET.Element('root')

    ET.SubElement(root, 'study-name', name='study-name').text = study_name
    ET.SubElement(root, 'number-subjects', name='number-subjects').text = '0'
    sensor_list = ET.SubElement(root, 'sensor-list', name='sensor-list')

    for sensor in sensors:
        ET.SubElement(sensor_list, 'Sensor', name=sensor).text = sensor

    tree = ET.ElementTree(root)
    tree.write(study_path + '/' + filename)


def create_study(study_path, number_subjects, sensors):
    """Function that controls the essential steps of study creation: Generate directory, xml and subjects

        Parameters
        ----------
            study_path
                Path to study.
            number_subjects
                Number of subjects that are enrolled at study start.
            sensors
                String list of selected sensors.
    """
    os.makedirs(study_path)
    generate_study_meta_xml(study_path, sensors)
    create_subjects(study_path, number_subjects)


def get_sensor_list():
    """Retrieves a list of possible used sensors

        Return
        ------
            List of sensors
    """

    sensors = ['acceleration-sensor', 'app-usage-statistic', 'barometer',
               'detected-activity-sensor', 'gravity', 'gyroscope', 'linear-acceleration',
               'location-sensor', 'magnetic-sensor', 'rotation-vector-sensor']
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
                           dcc.Input(id='create-study-duration-input', placeholder='Days', type='number', min='1')]),
        html.Div(children=[html.Span(children='Number of subjects: '),
                           dcc.Input(id='create-study-subject-number', placeholder='Number of subjects', type='number', min='0')]),
        html.Br(),
        html.Div(children=[html.Span(children='Sensors: '),
                           dcc.Checklist(id='create-study-sensors-checklist', options=sensor_checkboxes,
                                         labelStyle={'display': 'block'}, style={'margin-left': '132px', 'margin-top': '-18px'})]),
        html.Button(id='create-study-button', children='Create', style={'margin-top': '24px'}),
        html.P(id='create-study-output-state', style={'padding-top': '24px'}),
        ])
