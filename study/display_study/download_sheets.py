import os
import dash_core_components as dcc
import dash_html_components as html
import numpy as np

from app import dash_study_folder, zip_file, sheets_folder
from study import open_study_json


def zip_unused_sheets(study_id):
	"""
	zip all unused study sheets in order to download it later

	:return:
	"""
	study_json = open_study_json(study_id)
	sheets_path = os.path.join(dash_study_folder, study_id, sheets_folder)
	zip_path = os.path.join(dash_study_folder, study_id, zip_file)

	if os.path.isfile(zip_path):
		os.remove(zip_path)

	all_subject_list = np.array(os.listdir(sheets_path))
	enrolled_subject_list = np.array([enrolled_subject + '.pdf' for enrolled_subject in get_enrolled_app_users_from_json(study_json)])
	not_enrolled_subjects = [os.path.join(sheets_path, not_enrolled_subject) for not_enrolled_subject in np.setdiff1d(all_subject_list, enrolled_subject_list)]

	os.system('zip ' + zip_path + ' ' + ' '.join(not_enrolled_subjects))
