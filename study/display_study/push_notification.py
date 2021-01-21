import json
import os

import requests

import dash_html_components as html
import dash_core_components as dcc

from app import users_folder
from study import sep, main, ema, modalities
from study.display_study.study_data import get_qr_and_app_with_missing_data


firebase_url = 'https://fcm.googleapis.com/fcm/send'
firebase_auth = {
    main: 'key=AAAA_jwmwEU:APA91bFYuWaWejK255G8cGIlCTSumBSkUjrK_LzTNS-38D7dCOBRt4REFczSnSmsx-9tZKdJzjmR8sSU2bVBMWKADhK3TXRy6WBtOMVG9Jm77-PhtDEBowb5TwV3PxWa0PEjs4YU9bP6',
    ema: 'key=AAAAqONfb68:APA91bGUjq7VcWizetjZ9BGU3WWwtRHhVHVVMtn1F_5XKFm1yZSWiYw4nC0kl5guyUbwHLEQ7V1rpLqMDi_xXjd5q3UUKBCjnHTJIymAM0UBhfwS4g7mdL9aAtqSb8SyckaJtA5XT1my'
}
firebase_content_type = 'application/json'


def get_push_notification_div(study_df, user_list):
    # TODO: EMA and passive monitoring Checklist and output if successful sent
    qr_and_app_list = [row['id'] + sep + row['app'] for index, row in study_df.iterrows()]

    return html.Div(id='push-notification', children=[
        html.H3('Push notifications'),
        html.Div(id='push-notification-information-div', children=[
            html.Div(id='push-notification-title-div',
                     children=dcc.Input(id='push-notification-title', placeholder='Message title', type='text')),
            html.Div(id='push-notification-text-div',
                     children=dcc.Textarea(id='push-notification-text', placeholder='Message text')),
            html.Div(id='push-notification-receiver-list-div', children=[
                dcc.Dropdown(id='receiver-list', options=[{'label': qr_and_app, 'value': qr_and_app} for qr_and_app in qr_and_app_list], multi=True, placeholder='Receiver...')])]),
        html.Div(id='autofill-button-div', children=[
            html.Button(id='every-user-button', children='All IDs',
                        **{'data-user-list': qr_and_app_list}),
            html.Button(id='user-with-missing-data-button', children='Missing data IDs',
                        **{'data-user-list': get_qr_and_app_with_missing_data(user_list)})]),
        html.Button(id='send-push-notification-button', children='Send notification'),
        html.Div(id='push-notification-output-state')
    ])


def send_push_notification(title, text, receivers, study_id):
    sending_errors = []
    for modality in modalities:
        receivers_per_modality = [str(receiver).split(sep)[0] for receiver in receivers if str(receiver).split(sep)[1] == modality]

        if len(receivers_per_modality) > 0:
            tokens, errors = get_receivers_tokens(receivers_per_modality, study_id, modality)
            body = {
                'data': {
                    'title': title,
                    'body': text
                },
                'registration_ids': tokens
            }

            requests.post(firebase_url, headers={'Authorization': firebase_auth[modality], 'Content-Type': firebase_content_type}, json=body)
            sending_errors.extend(errors)
    return sending_errors


def get_receivers_tokens(receivers, study_id, modality):
    tokens = []
    errors = []

    for receiver in receivers:
        receiver_json_path = os.path.join(users_folder, study_id + '_' + receiver + '.json')
        with open(receiver_json_path, 'r') as f:
            receiver_json = json.load(f)
        if modality == main and 'pushNotification_token' in receiver_json:
            tokens.append(receiver_json["pushNotification_token"])
        elif modality == ema and 'pushNotification_token_ema' in receiver_json:
            tokens.append(receiver_json["pushNotification_token_ema"])
        else:
            errors.append("Sending to: " + receiver + sep + modality + " was not successful!")
    return tokens, errors
