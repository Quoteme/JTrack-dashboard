import json

from app import users_folder
from study import timestamp_format, sep, suffix_per_modality_dict, remove_status_code
from study.display_study.study_data import get_ids_and_app_list
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime
import os


def get_remove_users_div(not_left_users_dict):

    not_left_user_list = get_ids_and_app_list(not_left_users_dict)

    return html.Div(id='remove-user', children=[
        html.H3('Remove user'),
        html.Div(id='remove-user-div', children=[
            html.Div(id='remove-user-list-div', children=[
                dcc.Dropdown(id='remove-user-list', options=[{'label': qr_and_app, 'value': qr_and_app} for qr_and_app in not_left_user_list], multi=False, placeholder='User to be removed...')])]),

        html.Button(id='remove-user-button', children='Remove user from study'),
        html.P(id='remove-user-output-state'),
        dcc.ConfirmDialog(id='remove-user-confirm-dialog')
    ])


def remove_user(study_id, user_to_remove):
    user, app = str(user_to_remove).split(sep)
    user_json_path = os.path.join(users_folder, study_id + '_' + user + '.json')

    time_left_string = datetime.now().strftime(timestamp_format)
    time_left_key = 'time_left' + suffix_per_modality_dict[app]
    status_key = 'status' + suffix_per_modality_dict[app]

    with open(user_json_path) as f:
        user_data = json.load(f)

    user_data[time_left_key] = time_left_string
    user_data[status_key] = remove_status_code

    with open(user_json_path, 'w') as f:
        json.dump(user_data, f, ensure_ascii=False, indent=4)
