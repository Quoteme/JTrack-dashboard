import json
import requests

from app import users_folder

url = 'https://fcm.googleapis.com/fcm/send'
auth = 'key=AAAA_jwmwEU:APA91bFYuWaWejK255G8cGIlCTSumBSkUjrK_LzTNS-38D7dCOBRt4REFczSnSmsx-9tZKdJzjmR8sSU2bVBMWKADhK3TXRy6WBtOMVG9Jm77-PhtDEBowb5TwV3PxWa0PEjs4YU9bP6'
content_type = 'application/json'


def send_push_notification(title, text, receivers, study_id):
	tokens = get_receivers_tokens(receivers, study_id)
	body = {
		'data': {
			'title': title,
			'body': text
		},
		'registration_ids': tokens
	}
	requests.post(url, headers={'Authorization': auth, 'Content-Type': content_type}, json=body)


def get_receivers_tokens(receivers, study_id):
	tokens = []
	for receiver in receivers:
		receiver_json_path = users_folder + '/' + study_id + '_' + receiver + '.json'
		with open(receiver_json_path, 'r') as f:
			receiver_json = json.load(f)
		tokens.append(receiver_json["pushNotification_token"])
	return tokens
