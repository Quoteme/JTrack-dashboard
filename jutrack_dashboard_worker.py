import os
import json
from study_info import get_study_info_div
from datalad.api import Dataset
from subject_configuration.create_subjects import create_subjects
import getpass


storage_folder = '/mnt/jutrack_data'

if getpass.getuser() == 'msfz':
    home = os.environ['HOME']
    storage_folder = home + '/mnt/jutrack_data'
    os.makedirs(storage_folder + '/studys', exist_ok=True)

studys_folder = storage_folder + '/studys'
users_folder = storage_folder + '/users'


def create_study(json_data):
    study_id = json_data["name"]
    initial_subject_number = json_data["number-of-subjects"]

    folder_name = studys_folder + "/" + study_id
    if os.path.isdir(folder_name):
        return False

    os.makedirs(folder_name)
    datalad_dataset = Dataset(folder_name)
    datalad_dataset.create(folder_name)

    create_subjects(folder_name, initial_subject_number)
    datalad_dataset.save(folder_name, message=str(initial_subject_number) + ' initial subjects and study sheets added')

    json_file_name = folder_name + "/" + study_id + ".json"
    with open(json_file_name, 'w') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    datalad_dataset.save(folder_name, message="new file " + json_file_name + " for study")

    return True


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


def list_studys():
    study_list = []
    for study in os.listdir(studys_folder):
        if study != "users" and study != "lost+found" and os.path.isdir(studys_folder + '/' + study):
            study_list.append(study)

    return study_list


def get_study_information(study_name):
    selected_study_dir = studys_folder + '/' + study_name
    return get_study_info_div(selected_study_dir)
