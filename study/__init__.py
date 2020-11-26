import os



def get_sensor_list():
    """
    Retrieves a list of possible used sensors

    :return: list of sensors
    """

    sensors = [
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

    return sensors


def list_studies():
    """
    retrieves study list
    :return: list with active studies
    """
    study_list = []
    for study in os.listdir(studies_folder):
        if study != "users" and study != "lost+found" and os.path.isdir(studies_folder + '/' + study):
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
