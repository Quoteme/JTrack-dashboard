import json
import os

import dash
from dash.exceptions import PreventUpdate
from flask import send_file
import dash_html_components as html
from app import dash_study_folder, zip_file, sheets_folder, app, user
from exceptions.Exceptions import EmptyStudyTableException
from dash.dependencies import Output, Input, State

from study import get_app_user_objects_from_study_df, read_study_df, open_study_json, save_study_json
from study.create_subjects.create_subjects import create_subjects
from study.display_study.download_sheets import get_download_link_unused_sheets, zip_unused_sheets
from study.display_study.layout import get_study_info_div
from study.display_study.push_notification import send_push_notification, get_push_notification_div
from study.display_study.study_table import get_study_data_table


@app.callback([Output('study-info-div', 'children'),
               Output('study-data-div', 'children'),
               Output('download-unused-sheets-link-div', 'children'),
               Output('push-notification-div', 'children')],
              [Input('current-study-list', 'value')])
def display_study_info_callback(study_id):
    """
    Callback to display study info of chosen study on drop down selection. Provides information as well as the
    opportunity to create new subjects.

    :param study_id:  Name of the study which information should be displayed. The value is transferred by a drop down menu.
                Given by Input('current-study-list', 'value')
    :return: Html-Div containing the information of the study and a button for downloading unused sheets.
                Displayed beneath the drop down list. Returned by Output('current-selected-study', 'children').
    """
    if study_id:

        try:
            study_json = open_study_json(study_id)
            study_info_div = get_study_info_div(study_json)
            study_download_link = get_download_link_unused_sheets(study_json)
        except FileNotFoundError:
            return 'No valid study (Study json missing).', '', '', ''

        try:
            study_df = read_study_df(study_json)
            user_list = get_app_user_objects_from_study_df(study_json, study_df)

            study_table = get_study_data_table(study_df, user_list)
            push_notification_div = get_push_notification_div(study_json, user_list)
           # remove_users_div = get_remove_users_div(study_json, user_list)
        except FileNotFoundError:
            study_table = html.Div("Table file not found.")
            push_notification_div = ''
        except KeyError:
            study_table = html.Div("Data is erroneous.")
            push_notification_div = ''
        except EmptyStudyTableException:
            study_table = html.Div("No data available.")
            push_notification_div = ''

        return study_info_div, study_table, study_download_link, push_notification_div
    else:
        raise PreventUpdate


@app.server.route('/download-<string:study_id>-<string:user>')
def download_marked_sheets(study_id, user):
    """
    Routing option to access and download subjects sheets. Just selected sheets from enrolled subjects are downloaded.

    :param study_id: study name
    :param user: user name
    :return: Flask send_file delivering zip folder containing selected sheets
    """

    return send_file(os.path.join(dash_study_folder, study_id, sheets_folder, user + '.pdf'),
                     mimetype='application/pdf',
                     as_attachment=True)


@app.server.route('/download-<string:study_id>')
def download_sheets(study_id):
    """
    Execute download of subject-sheet-zip which contains all of the subject sheets for every subject of one specified study
    :param study_id: specified study of which the sheets should be downloaded

    :return: Flask send_file which delivers the zip belonging to the study
    """

    zip_unused_sheets(study_id)
    return send_file(os.path.join(dash_study_folder, study_id, zip_file),
                     mimetype='application/zip',
                     as_attachment=True)


@app.callback([Output('push-notification-title', 'value'),
               Output('push-notification-text', 'value'),
               Output('receiver-list', 'value'),
               Output('push-notification-output-state', 'children')],
              [Input('user-with-missing-data-button', 'n_clicks'),
               Input('every-user-button', 'n_clicks'),
               Input('send-push-notification-button', 'n_clicks')],
              [State('push-notification-title', 'value'),
               State('push-notification-text', 'value'),
               State('receiver-list', 'value'),
               State('user-with-missing-data-button', 'data-user-list'),
               State('every-user-button', 'data-user-list'),
               State('current-study-list', 'value')])
def push_notifications(autofillbtn1, autofillbtn2, send_button, title, text, receivers, missing_data_users_list, every_user_list , study_id):
    ctx = dash.callback_context

    if len(ctx.triggered) > 0:
        if ctx.triggered[0]['value']:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == 'user-with-missing-data-button':
                return title, text, missing_data_users_list, ''
            if button_id == 'every-user-button':
                return title, text, every_user_list, ''
            if button_id == 'send-push-notification-button' and (user.role == 'master' or user.role == 'invest'):
                if not title or not text or not receivers:
                    error_output_state = ''
                    if not title:
                        error_output_state = 'Please enter a message title!'
                    elif not text:
                        error_output_state = 'Please enter a message!'
                    elif not receivers:
                        error_output_state = 'Please select receivers!'
                    return title, text, receivers, error_output_state
                else:
                    send_push_notification(title, text, receivers, study_id)
                    return '', '', [], 'Push notification sent!'
    raise PreventUpdate


@app.callback([Output('total-subjects', 'children'),
               Output('create-additional-subjects-input', 'value')],
              [Input('create-additional-subjects-button', 'n_clicks')],
              [State('current-study-list', 'value'),
               State('create-additional-subjects-input', 'value')])
def create_additional_subjects_callback(n_clicks, study_id, number_of_subjects):
    """
    Creates additional subjects on button click. QR-Codes and study sheets are added to the existing directories

    :param n_clicks: not used
    :param study_id: study receiving new subjects
    :param number_of_subjects: number of new subjects
    :return: refreshes current number of subjects state and clears input field
    """
    if n_clicks and number_of_subjects and (user.role == 'master' or user.role == 'invest'):
        study_json = open_study_json(study_id)
        study_json["number-of-subjects"] = int(study_json["number-of-subjects"]) + number_of_subjects
        save_study_json(study_id, study_json)

        create_subjects(study_json["name"], study_json["number-of-subjects"])

        return "Total number of subject: " + str(study_json["number-of-subjects"]), ''
    else:
        raise PreventUpdate
