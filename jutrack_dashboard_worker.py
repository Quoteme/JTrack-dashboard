import os
import json
from study_info import get_study_info_div

storage_folder = '~/mnt/jutrack_data'
studies_folder = storage_folder + '/studies'
users_folder = storage_folder + '/users'


def create_study(json_data):
    study_id = json_data["name"]
    folder_name = studies_folder + "/" + study_id

    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)
        #datalad_dataset = Dataset(folder_name)
        file_name = studies_folder + "/" + study_id + "/" + study_id + ".json"
        with open(file_name, 'w') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        #datalad_dataset.save(file_name, message="new file " + file_name + " for study")
        return True
    else:
        return False


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


def list_studies():
    study_list = []
    for study in os.listdir(studies_folder):
        if study != "users" and study != "lost+found" and os.path.isdir(studies_folder + '/' + study):
            study_list.append(study)

    return study_list


def get_study_information(study_name):
    selected_study_dir = studies_folder + '/' + study_name
    return get_study_info_div(selected_study_dir)
