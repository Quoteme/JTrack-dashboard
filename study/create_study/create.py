import base64
import json
import os

from app import studies_folder, dash_study_folder, qr_folder, sheets_folder, image_resources_folder
from exceptions.Exceptions import StudyAlreadyExistsException
from study import save_study_json
from study.create_subjects.create_subjects import create_subjects


def create_study(study_dict):
	"""
	Create study using underlying json data which contains study_name, initial number of subjects, study duration and a list
	of sensors to be used. The new study is created in the storage folder. Further,
	folders for qr codes and subjects sheets will be create within the dashboard project and filled with corresponding qr codes
	and pdfs. Lastly, a json file containing meta data of the study is stored.

	:return: True or False depending if creation succeeded. False if and only if study already exists.
	"""
	study_path = os.path.join(studies_folder, study_dict['name'])
	if os.path.isdir(study_path):
		raise StudyAlreadyExistsException
	os.makedirs(study_path)
	os.makedirs(os.path.join(dash_study_folder, study_dict['name'], qr_folder), exist_ok=True)
	os.makedirs(os.path.join(dash_study_folder, study_dict['name'], sheets_folder), exist_ok=True)

	if 'images' in study_dict and study_dict['images']:
		ema_images_bytes = base64.b64decode(study_dict['images'])
		with open(os.path.join(image_resources_folder, study_dict['name'] + '.zip'), 'wb') as zf:
			zf.write(ema_images_bytes)
			study_dict['images'] = True

	if 'active_labeling' in study_dict and study_dict['active_labeling'] != 0:
		study_dict['sensor-list'].append('active_labeling')

	# store json file with data
	save_study_json(study_dict['name'], study_dict)

	# create subjects depending on initial subject number
	create_subjects(study_dict['name'], study_dict['number-of-subjects'])
