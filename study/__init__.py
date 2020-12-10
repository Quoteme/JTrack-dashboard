import os

from app import studies_folder

passive = 'passive'
ema = 'ema'

sensor_list = [
    'accelerometer',
    'activity',
    'application_usage',
    'barometer',
    'gravity_sensor',
    'gyroscope',
    'location',
    'magnetic_sensor',
    'rotation_vector',
    'linear_acceleration'
]

frequency_list = [50, 100, 150, 200]

modality_list = [{'label': 'Ecological momentary assessment', 'value': 'ema'}, {'label': 'Passive monitoring', 'value': 'passive'}]


def list_studies():
    """
    retrieves study list
    :return: list with active studies
    """
    study_list = []
    for study in os.listdir(studies_folder):
        if study != "users" and study != "lost+found" and os.path.isdir(os.path.join(studies_folder, study)):
            study_list.append(study)

    return study_list


def get_study_list_as_dict():
    """
    dict for drop downs consisting of key for access and value for displaying a study
    :return: dict with active studies
    """
    current_studies = list_studies()
    study_list = []
    for study in current_studies:
        study_list.append({'label': study, 'value': study})
    return study_list
