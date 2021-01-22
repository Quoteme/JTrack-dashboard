import os

import pandas as pd
import numpy as np

from app import storage_folder, csv_prefix
from exceptions.Exceptions import EmptyStudyTableException
from study import ema, table_columns, sensors_per_modality_dict, main, sep


def read_study_df(study_json):
    study_csv = os.path.join(storage_folder, csv_prefix + study_json["name"] + '.csv')
    study_df = pd.read_csv(study_csv)

    study_df = study_df.reindex(columns=table_columns)
    study_df = study_df.rename(columns={"subject_name": "id"})
    study_df = drop_unused_data(study_json, study_df)
    study_df = study_df.replace(to_replace=[np.nan, 'none', 0], value='')
    study_df = study_df.sort_values(by=['app', 'id']).reset_index(drop=True)
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

    unused_data = np.setdiff1d(sensors_per_modality_dict[main], study_json["sensor-list"]) if 'sensor-list' in study_json else sensors_per_modality_dict[main]
    if 'survey' not in study_json:
        unused_data = np.concatenate((unused_data, sensors_per_modality_dict[ema]), axis=None)

    for data in unused_data:
        study_df[data + ' n_batches'] = study_df[data + ' n_batches'].replace(to_replace=[0], value=np.nan)
        study_df[data + ' last_time_received'] = study_df[data + ' last_time_received'].replace(to_replace=['none'],
                                                                                                    value=np.nan)
    study_df = pd.DataFrame.dropna(study_df, axis=1, how='all')
    return study_df


def get_user_list(study_df):
    return np.sort(np.unique(['_'.join(str(registration_id).split('_')[:-1]) for registration_id in study_df['id']]))


def get_ids_and_app_with_missing_data(missing_data):
    missing_data_ids = []
    for app, missing_data_qr_code_per_app in missing_data.items():
        missing_data_ids.extend([missing_data_qr_codes + sep + app for missing_data_qr_codes in missing_data_qr_code_per_app])
    return sorted(missing_data_ids)


def get_ids_and_app_of_active_users(active_users):
    active_ids = []
    for app, active_qr_code_per_app in active_users.items():
        active_ids.extend([active_users_qr_codes + sep + app for active_users_qr_codes in active_qr_code_per_app])
    return sorted(active_ids)
