import os

from app import archive_folder, csv_prefix, studies_folder


def close(self):
	"""
	close a study (moves it to archive folder)

	:return:
	"""
	archived_study_path = archive_folder + '/' + self.study_id
	os.makedirs(archived_study_path)
	os.rename(studies_folder + '/' + self.study_id, archived_study_path + '/' + self.study_id)
	if os.path.isfile(self.study_csv):
		os.rename(self.study_csv, archived_study_path + '/' + csv_prefix + self.study_id + '.csv')