import os
import getpass

# Paths to storage directory and for the qrcodes + subject sheets
qr_path = 'QR-Codes'
sheets_path = 'Subject-Sheets'
storage_folder = '/mnt/jutrack_data'

os.makedirs(qr_path, exist_ok=True)
os.makedirs(sheets_path, exist_ok=True)
if getpass.getuser() == 'msfz':
    home = os.environ['HOME']
    storage_folder = home + '/mnt/jutrack_data'
    os.makedirs(storage_folder + '/studys', exist_ok=True)

studies_folder = storage_folder + '/studys'
users_folder = storage_folder + '/users'


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
