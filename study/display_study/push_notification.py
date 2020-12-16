import json
import requests

from app import users_folder, fire_url, fire_auth, fire_content_type


def send_push_notification(title, text, receivers, study_id):
	tokens = get_receivers_tokens(receivers, study_id)
	body = {
		'data': {
			'title': title,
			'body': text
		},
		'registration_ids': tokens
	}
	requests.post(fire_url, headers={'Authorization': fire_auth, 'Content-Type': fire_content_type}, json=body)


def get_receivers_tokens(receivers, study_id):
	tokens = []
	for receiver in receivers:
		receiver_json_path = users_folder + '/' + study_id + '_' + receiver + '.json'
		with open(receiver_json_path, 'r') as f:
			receiver_json = json.load(f)
		tokens.append(receiver_json["pushNotification_token"])
	return tokens
