import json
import os

from app import studies_folder

max_subjects_exp = 5
number_of_activations = 4

timestamp_format = "%Y-%m-%d %H:%M:%S"

passive_monitoring = 'passive_monitoring'
main = 'main'
ema = 'ema'
modalities = [ema, main]
sep = ':'

sensors_per_modality_dict = {
    main: [
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
    ],
    ema: [
        'ema'
    ]
}

frequency_dict = {'50Hz': 50,
                  '100Hz': 100,
                  '150Hz': 150,
                  '200Hz': 200}

labeling_dict = {'No labeling': 0,
                  'Active labeling': 1,
                  'Manual active labeling': 2}

modality_dict = {'Ecological momentary assessment': ema,
                 'Passive monitoring': passive_monitoring}

table_columns = ['subject_name',
                 'app',
                 'device_id',
                 'date_registered',
                 'date_left_study',
                 'time_in_study',
                 'status_code',
                 'accelerometer n_batches',
                 'accelerometer last_time_received',
                 'activity n_batches',
                 'activity last_time_received',
                 'application_usage n_batches',
                 'application_usage last_time_received',
                 'barometer n_batches',
                 'barometer last_time_received',
                 'gravity_sensor n_batches',
                 'gravity_sensor last_time_received',
                 'gyroscope n_batches',
                 'gyroscope last_time_received',
                 'location n_batches',
                 'location last_time_received',
                 'magnetic_sensor n_batches',
                 'magnetic_sensor last_time_received',
                 'rotation_vector n_batches',
                 'rotation_vector last_time_received',
                 'linear_acceleration n_batches',
                 'linear_acceleration last_time_received',
                 'ema n_batches',
                 'ema last_time_received']


def list_studies():
    """
    retrieves study list
    :return: list with active studies
    """
    study_list = []
    for study in os.listdir(studies_folder):
        if os.path.isdir(os.path.join(studies_folder, study)) and os.path.isfile(os.path.join(studies_folder, study, study + '.json')):
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


def open_study_json(study_id):
    study_json_file_path = os.path.join(studies_folder, study_id, study_id + '.json')
    with open(study_json_file_path, 'r') as f:
        study_json = json.load(f)
    return study_json


def save_study_json(study_id, study_json):
    study_json_file_path = os.path.join(studies_folder, study_id, study_id + '.json')
    with open(study_json_file_path, 'w') as jf:
        json.dump(study_json, jf, ensure_ascii=False, indent=4)
