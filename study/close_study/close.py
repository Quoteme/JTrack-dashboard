import os

from app import archive_folder, csv_prefix, studies_folder, storage_folder


def close_study(study_id):
	"""
	close a study (moves it to archive folder)

	:return:
	"""
	archived_study_path = os.path.join(archive_folder, study_id)
	os.makedirs(archived_study_path)
	os.rename(os.path.join(studies_folder, study_id), os.path.join(archived_study_path, study_id))

	study_csv = csv_prefix + study_id + '.csv'
	study_csv_path = os.path.join(storage_folder, study_csv)
	if os.path.isfile(study_csv_path):
		os.rename(study_csv_path, os.path.join(archived_study_path, study_csv))
