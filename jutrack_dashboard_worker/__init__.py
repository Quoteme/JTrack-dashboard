import os
import getpass

# Paths to storage directory and for the qrcodes + subject sheets
dash_study_folder = 'Studies'
os.makedirs(dash_study_folder, exist_ok=True)
sheets_folder = 'Subject-Sheets'
qr_folder = 'QR-Codes'
zip_file = 'sheets.zip'

storage_folder = '/mnt/jutrack_data'
csv_prefix = 'jutrack_dashboard_'
if getpass.getuser() == 'msfz':
    home = os.environ['HOME']
    storage_folder = home + '/mnt/jutrack_data'
    os.makedirs(storage_folder + '/studies', exist_ok=True)
    os.makedirs(storage_folder + '/archive', exist_ok=True)

studies_folder = storage_folder + '/studies'
archive_folder = storage_folder + '/archive'
users_folder = storage_folder + '/users'


def get_sensor_list():
    """Retrieves a list of possible used sensors

        Return
        ------
            List of sensors
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
    study_list = []
    for study in os.listdir(studies_folder):
        if study != "users" and study != "lost+found" and os.path.isdir(studies_folder + '/' + study):
            study_list.append(study)

    return study_list


def get_study_list_as_dict():
    current_studies = list_studies()
    study_list = []
    for study in current_studies:
        study_list.append({'label': study, 'value': study})
    return study_list
