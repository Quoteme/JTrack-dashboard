import dash
from dash.exceptions import PreventUpdate
from flask import send_file
import dash_html_components as html
from app import dash_study_folder, zip_file, sheets_folder, app, user
from exceptions.Exceptions import EmptyStudyTableException
from dash.dependencies import Output, Input, State

from study.display_study.push_notification import send_push_notification


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
       # study = Study.from_study_id(study_id)

        try:
            PreventUpdate
           # active_subjects_table = study.get_study_data_table()
        except FileNotFoundError:
            active_subjects_table = html.Div("Table file not found")
        except KeyError:
            active_subjects_table = html.Div("Data erroneous")
        except EmptyStudyTableException:
            active_subjects_table = html.Div("No data available")
        raise PreventUpdate
        #return study.get_study_info_div(), active_subjects_table, study.get_download_link_unused_sheets(), study.get_push_notification_div()
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

    return send_file(dash_study_folder + '/' + study_id + '/' + sheets_folder + '/' + user + '.pdf',
                     mimetype='application/pdf',
                     as_attachment=True)


@app.server.route('/download-<string:study_id>')
def download_sheets(study_id):
    """
    Execute download of subject-sheet-zip which contains all of the subject sheets for every subject of one specified study
    :param study_id: specified study of which the sheets should be downloaded

    :return: Flask send_file which delivers the zip belonging to the study
    """

    #selected_study = Study.from_study_id(study_id)
    #selected_study.zip_unused_sheets()
    return send_file(dash_study_folder + '/' + study_id + '/' + zip_file,
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
