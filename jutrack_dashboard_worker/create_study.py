from jutrack_dashboard_worker import studies_folder, sheets_path, qr_path
from jutrack_dashboard_worker.create_subjects import create_subjects
from datalad.api import Dataset
import os
import json


def create_study(json_data):
    """
    Create study using underlying json data which contains study_name, initial number of subjects, study duration and a list
    of sensors to be used. The new study is created in the storage folder and deposited as a Datalad data set. Further,
    folders for qrcodes and subjects sheets will be create within the dashboard project and filled with corresponding qrcodes
    and pdfs. Lastly, a json file containing meta data of the study is stored within the Datalad data set.

            Parameters
            ----------
             json_data
                 JSON file containing information w.r.t. the study (name, initial number of subjects, duration, sensor list)

            Return
            ------
                 True or False depending if creation succeeded. False if and only if study already exists.
    """

    study_id = json_data["name"]
    initial_subject_number = json_data["number-of-subjects"]

    study_path = studies_folder + "/" + study_id
    if os.path.isdir(study_path):
        return False

    os.makedirs(study_path)
    study_date_set = Dataset(study_path)
    study_date_set.create(study_path)

    os.makedirs(qr_path + '/' + study_id)
    os.makedirs(sheets_path + '/' + study_id)
    create_subjects(study_id, initial_subject_number)

    json_file_name = study_path + "/" + study_id + ".json"
    with open(json_file_name, 'w') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    study_date_set.save(study_path, message="new file " + json_file_name + " for study")

    return True
