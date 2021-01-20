import json
import requests

import dash_html_components as html
import dash_core_components as dcc

from app import users_folder, firebase_url, firebase_auth, firebase_content_type
from study import get_enrolled_qr_codes_from_json, get_ids_with_missing_data


def get_push_notification_div(study_json, user_list):
    # TODO: EMA and passive monitoring Checklist and output if successful sent
    all_ids = [{'label': enrolled_qr_code, 'value': enrolled_qr_code} for enrolled_qr_code in
               get_enrolled_qr_codes_from_json(study_json)]

    return html.Div(id='push-notification', children=[
        html.H3('Push notifications'),
        html.Div(id='push-notification-information-div', children=[
            html.Div(id='push-notification-title-div',
                     children=dcc.Input(id='push-notification-title', placeholder='Message title', type='text')),
            html.Div(id='push-notification-text-div',
                     children=dcc.Textarea(id='push-notification-text', placeholder='Message text')),
            html.Div(id='push-notification-receiver-list-div', children=[
                dcc.Dropdown(id='receiver-list', options=all_ids, multi=True, placeholder='Receiver...')])]),
        html.Div(id='autofill-button-div', children=[
            html.Button(id='every-user-button', children='All IDs',
                        **{'data-user-list': get_enrolled_qr_codes_from_json(study_json)}),
            html.Button(id='user-with-missing-data-button', children='Missing data IDs',
                        **{'data-user-list': get_ids_with_missing_data(user_list)})]),
        html.Button(id='send-push-notification-button', children='Send notification'),
        html.Div(id='push-notification-output-state')
    ])


def send_push_notification(title, text, receivers, study_id):
    tokens = get_receivers_tokens(receivers, study_id)
    body = {
        'data': {
            'title': title,
            'body': text
        },
        'registration_ids': tokens
    }
    requests.post(firebase_url, headers={'Authorization': firebase_auth, 'Content-Type': firebase_content_type}, json=body)


def get_receivers_tokens(receivers, study_id):
    tokens = []
    for receiver in receivers:
        receiver_json_path = users_folder + '/' + study_id + '_' + receiver + '.json'
        with open(receiver_json_path, 'r') as f:
            receiver_json = json.load(f)
        tokens.append(receiver_json["pushNotification_token"])
    return tokens
