import os
import json
import qrcode

from SubjectPDF import SubjectPDF
from study_info import get_study_info_div
from datalad.api import Dataset
import getpass

qr_path = 'QR-Codes'
sheets_path = 'Subject-Sheets'
storage_folder = '/mnt/jutrack_data'

os.makedirs(qr_path, exist_ok=True)
os.makedirs(sheets_path, exist_ok=True)
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

    os.makedirs(qr_path + '/' + study_id)
    os.makedirs(sheets_path + '/' + study_id)
    create_subjects(study_id, initial_subject_number)

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


def get_study_information(study_id):
    return get_study_info_div(studys_folder, study_id)


def create_subjects(study_id, number_new_subjects):
    """
    Function that is executed if the create new subjects button is clicked. It creates new subject directories and
    corresponding QR-codes.

            Parameters
            ----------
                study_id
                    path to the directory of the study where new subjects should be dropped. ('./studies/study_name')
                number_new_subjects
                    number of new subjects that should be enrolled
            Return
            -------

    """

    current_number_subjects = 0
    study_json_file_path = studys_folder + '/' + study_id + "/" + study_id + ".json"

    if os.path.isfile(study_json_file_path):
        with open(study_json_file_path, 'r') as f:
            data = json.load(f)
            current_number_subjects = data['number-of-subjects']
            data['number-of-subjects'] = current_number_subjects+number_new_subjects
            json.dump(data, f)

    for subj_number in range(current_number_subjects+1, current_number_subjects+number_new_subjects+1):
        subj_name = study_id + '_' + str(subj_number).zfill(4)
        create_qr_code_for_new_user(study_id, subj_name)

    zip_subject_sheet_folder(study_id)
    return


def create_qr_code_for_new_user(study_id, subj_name):
    """
    Function to create a QR-code which corresponds to the new subject given. The Code will be stored in a .png as well
    as in a pdf which contains additional information. (png: ./study_dir/QR-Codes; pdf: ./study-dir/subject-sheets)

            Parameters
            ----------
                study_id
                    path to the directory of the study ('./studies/study_name').
                subj_name
                    path to the directory of the new subject containing particularly its name ('./studies/study-name/Subject00000').
            Return
            -------

    """

    qr_code_path = qr_path + '/' + study_id
    for i in range(1, 5):
        activation_number = '_' + str(i)
        current_qr_code = qr_code_path + '/' + subj_name + activation_number + '.png'
        print(current_qr_code)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        data = "https://jutrack.inm7.de?username=%s&studyid=%s" % (subj_name + activation_number, study_id)

        # Add data
        qr.add_data(data)
        qr.make(fit=True)

        # Create an image from the QR Code instance
        img = qr.make_image()

        # Save it somewhere, change the extension as needed:
        img.save(current_qr_code)
    write_to_pdf(qr_code_path, study_id, subj_name)


def zip_subject_sheet_folder(study_id):
    study_sheets_path = sheets_path + '/' + study_id
    os.system('zip ' + study_sheets_path + '_subject_sheets.zip ' + study_sheets_path + '/*.pdf')


def write_to_pdf(qr_code_path, study_id, new_subj_name):
    """
    TODO: more information
    Function to generate a pdf based on QR-Code and other information.

            Parameters
            ----------
                qr_code_path
                    path to QR-code referring to given new subject (.png)
                study_id
                    path to the directory of the study ('./studies/study_name').
                new_subj_name
                    name of subject (Subject00000).
            Return
            -------

    """
    qr_codes = qr_code_path + '/' + new_subj_name
    pdf_path = sheets_path + '/' + study_id + '/' + new_subj_name + '.pdf'

    pdf = SubjectPDF(study_id)
    pdf.add_page()

    pdf.draw_input_line_filled('Subject-ID', new_subj_name)
    pdf.ln(10)

    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
    pdf.ln(15)

    pdf.qr_code(qr_codes, 5)

    pdf.output(pdf_path)


