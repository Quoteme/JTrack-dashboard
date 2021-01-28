import os
import dash_core_components as dcc
import dash_html_components as html
import numpy as np

from app import dash_study_folder, zip_file, sheets_folder
from exceptions.Exceptions import EmptyStudyTableException
from study import open_study_json
from study.display_study.study_data import read_study_df, get_user_list


def zip_unused_sheets(study_id):
	"""
	zip all unused study sheets in order to download it later

	:return:
	"""
	study_json = open_study_json(study_id)

	try:
		study_df = read_study_df(study_json)
		enrolled_subject_list = get_user_list(study_df)
	except (FileNotFoundError, KeyError, EmptyStudyTableException):
		enrolled_subject_list = []

	sheets_path = os.path.join(dash_study_folder, study_id, sheets_folder)
	zip_path = os.path.join(dash_study_folder, study_id, zip_file)
	if os.path.isfile(zip_path):
		os.remove(zip_path)

	all_subjects_pdfs = np.array(os.listdir(sheets_path))
	enrolled_subjects_pdfs = np.array([enrolled_subject + '.pdf' for enrolled_subject in enrolled_subject_list])
	not_enrolled_subjects_pdfs = [os.path.join(sheets_path, not_enrolled_subject) for not_enrolled_subject in np.setdiff1d(all_subjects_pdfs, enrolled_subjects_pdfs)]

	os.system('zip ' + zip_path + ' ' + ' '.join(not_enrolled_subjects_pdfs))


def get_download_unused_sheets_button(study_json):
	return html.A(id='download-unused-sheets-link', children='Download unused study sheets',
				  className='button', href='/download-' + study_json["name"])