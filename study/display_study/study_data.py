import os

import pandas as pd
import numpy as np

from app import storage_folder, csv_prefix
from exceptions.Exceptions import EmptyStudyTableException
from study import ema, table_columns, sensors_per_modality_dict, main
from study.display_study.AppUser import AppUser


def read_study_df(study_json):
    study_csv = os.path.join(storage_folder, csv_prefix + study_json["name"] + '.csv')
    study_df = pd.read_csv(study_csv)

    study_df = study_df.reindex(columns=table_columns)
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

    unused_data = np.setdiff1d(sensors_per_modality_dict[main], study_json["sensor-list"]) if 'sensor-list' in study_json else sensors_per_modality_dict[main]
    if 'survey' not in study_json:
        unused_data = np.concatenate((unused_data, sensors_per_modality_dict[ema]), axis=None)

    for data in unused_data:
        study_df[data + ' n_batches'] = study_df[data + ' n_batches'].replace(to_replace=[0], value=np.nan)
        study_df[data + ' last_time_received'] = study_df[data + ' last_time_received'].replace(to_replace=['none'],
                                                                                                    value=np.nan)
    study_df = pd.DataFrame.dropna(study_df, axis=1, how='all')
    return study_df


def get_app_users(study_json, study_df):
    """
    return list of app user objects that store necessary data for each user that comes from the different qr code activations

    :param study_df: study data frame
    :return: list with app user objects
    """
    user_list = []
    enrolled_users = np.sort(np.unique(['_'.join(str(scanned).split('_')[:-1]) for scanned in study_df['id']]))

    for user in enrolled_users:
        user_list.append(AppUser(user_name=user, data=study_df[study_df['id'].str.match(user)], study_id=study_json["name"], duration=study_json["duration"]))
    return user_list


def get_ids_with_missing_data(user_list):
    missing_data_ids = []
    for user in user_list:
        missing_data_ids.extend(user.ids_with_missing_data)
    return missing_data_ids
