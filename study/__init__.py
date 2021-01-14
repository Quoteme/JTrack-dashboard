import json
import os

from app import studies_folder, storage_folder, csv_prefix
import numpy as np
import pandas as pd

from exceptions.Exceptions import EmptyStudyTableException
from study.display_study.AppUser import AppUser

max_subjects_exp = 5
number_of_activations = 4

passive_monitoring = 'passive_monitoring'
passive_monitoring_suffix = ''
ema = 'ema'
ema_suffix = 'ema'

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

modality_list = [{'label': 'Ecological momentary assessment', 'value': ema}, {'label': 'Passive monitoring', 'value': passive_monitoring}]


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


def open_study_json(study_id):
    study_json_file_path = os.path.join(studies_folder, study_id, study_id + '.json')
    with open(study_json_file_path, 'r') as f:
        study_json = json.load(f)
    return study_json


def save_study_json(study_id, study_json):
    study_json_file_path = os.path.join(studies_folder, study_id, study_id + '.json')
    with open(study_json_file_path, 'w') as jf:
        json.dump(study_json, jf, ensure_ascii=False, indent=4)


def read_study_df(study_json):
    study_csv = os.path.join(storage_folder, csv_prefix + study_json["name"] + '.csv')

    study_df = pd.read_csv(study_csv)
    study_df = study_df.rename(columns={"subject_name": "id"})
    study_df = drop_unused_data(study_json, study_df)
    study_df = study_df.replace(to_replace=[np.nan, 'none', 0], value='')

    if len(study_df.index) == 0:
        raise EmptyStudyTableException

    return study_df


def drop_unused_data(study_json, study_df):
    """
    Drops columns of sensors which are not selected in the study. Only if completely empty (-> if actual unused sensors contain
    data they will be highlighted)

    :param study_df: data frame of study
    :return: edited data frame without unused sensors
    """

    unused_data = np.setdiff1d(sensor_list, study_json["sensor-list"]) if 'sensor-list' in study_json else sensor_list
    if 'survey' not in study_json:
        unused_data = np.append(unused_data, ema)

    for data in unused_data:
        study_df[data + ' n_batches'] = study_df[data + ' n_batches'].replace(to_replace=[0], value=np.nan)
        study_df[data + ' last_time_received'] = study_df[data + ' last_time_received'].replace(to_replace=['none'],
                                                                                                    value=np.nan)
    study_df = pd.DataFrame.dropna(study_df, axis=1, how='all')
    return study_df


def get_enrolled_app_users_from_json(study_json):
    """
    get list of all app users that have ever scanned at least one qr code

    :return: list of active app users
    """
    enrolled_qr_codes = np.array(study_json["enrolled-subjects"])
    all_enrolled_app_users = np.unique([scanned[:-2] for scanned in enrolled_qr_codes])
    sorted_list = np.sort(all_enrolled_app_users)
    return sorted_list


def get_enrolled_qr_codes_from_json(study_json):
    """
    get list of all app users that have ever scanned at least one qr code

    :return: list of active app users
    """
    enrolled_qr_codes = np.array(study_json["enrolled-subjects"])
    sorted_list = np.sort(enrolled_qr_codes)
    return sorted_list


def get_app_user_objects_from_study_df(study_json, study_df):
    """
    return list of app user objects that store necessary data for each user that comes from the different qr code activations

    :param study_df: study data frame
    :return: list with app user objects
    """
    user_list = []
    active_users = get_enrolled_app_users_from_json(study_json)
    for user in active_users:
        user_list.append(AppUser(user_name=user, data=study_df[study_df['id'].str.match(user)], study_id=study_json["name"], duration=study_json["duration"]))
    return user_list


def get_ids_with_missing_data(user_list):
    missing_data_ids = []
    for user in user_list:
        missing_data_ids.extend(user.ids_with_missing_data)
    return missing_data_ids




