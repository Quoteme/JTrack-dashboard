import os

from exceptions.Exceptions import StudyAlreadyExistsException


def create(self):
	"""
	Create study using underlying json data which contains study_name, initial number of subjects, study duration and a list
	of sensors to be used. The new study is created in the storage folder. Further,
	folders for qr codes and subjects sheets will be create within the dashboard project and filled with corresponding qr codes
	and pdfs. Lastly, a json file containing meta data of the study is stored.

	:return: True or False depending if creation succeeded. False if and only if study already exists.
	"""
	if os.path.isdir(self.study_path):
		raise StudyAlreadyExistsException

	# creates study folder in storage folder
	os.makedirs(self.study_path)

	# generate folders for qr codes and subject sheets in dashboard folder of study
	os.makedirs(self.qr_path)
	os.makedirs(self.sheets_path)

	# store json file with meta data
	self.save_study_json()

	# create subjects depending on initial subject number
	self.create_sheets_wrt_total_subject_number()


def create_additional_subjects(self, number_of_subjects):
	"""
	create additional subjects for the study

	:param number_of_subjects: number of subjects to create
	:return:
	"""
	self.study_json["number-of-subjects"] = str(int(self.study_json["number-of-subjects"]) + number_of_subjects)
	self.save_study_json()
	self.create_sheets_wrt_total_subject_number()


def create_sheets_wrt_total_subject_number(self):
	"""
	adjust the number of existing subject sheets according to the number of all subjects (creates for each subject a sheet)

	:return:
	"""
	n_subjects = int(self.study_json["number-of-subjects"])
	for subject_number in range(1, n_subjects + 1):
		self.create_subject(subject_number)


