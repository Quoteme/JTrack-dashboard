import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask import send_file

from jutrack_dashboard_worker.push_notifications import send_push_notification
from layout import get_main_page, get_log_in_div, get_logged_in_div, get_body
from security.DashboardUser import DashboardUser
from jutrack_dashboard_worker import zip_file, dash_study_folder, get_study_list_as_dict, sheets_folder
from Exceptions import StudyAlreadyExistsException, NoSuchUserException, WrongPasswordException, \
    EmptyStudyTableException, MissingCredentialsException
from jutrack_dashboard_worker.Study import Study
from menu_tabs import get_create_study_div, get_current_studies_div, get_close_study_div, get_about_div

# Generate dash app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
user = DashboardUser()

# General dash app layout starting with the login div
app.layout = get_main_page()


@app.callback([Output('login-wrapper', 'children'),
               Output('page-body', 'children'),
               Output('login-output-state', 'children'),
               Output('username', 'value'),
               Output('passwd', 'value')],
              [Input('login-button', 'n_clicks')],
              [State('username', 'value'),
               State('passwd', 'value')])
def display_page_callback(login_click, username, password):
    """
    TODO: Logout resulting in displaying the login page again

    :param login_click: login button click
    :param username: username of login
    :param password: password of login

    :return: content div (general content with menu or the login page if login was erroneous)
    """
    if login_click:
        try:
            user.login(username, password)
            return get_logged_in_div(username), get_body(), 'Logged in successfully!', username, ''
        except NoSuchUserException:
            return get_log_in_div(), '', 'This user does not exist!', username, ''
        except WrongPasswordException:
            return get_log_in_div(), '', 'Wrong Password!', username, ''
        except MissingCredentialsException:
            return get_log_in_div(), '', 'Please enter your credentials', username, ''
    else:
        raise PreventUpdate


@app.callback(Output('content-div', 'children'),
              [Input('create-button', 'n_clicks'),
               Input('current-studies-button', 'n_clicks'),
               Input('about-button', 'n_clicks'),
               Input('close-button', 'n_clicks')
               ])
def display_menu_tab_content_callback(btn1, btn2, btn3, btn4):
    """
    Callback reacting if a menu button is clicked. Returns clicked button content

    :param btn1: not used due callback_context syntax
    :param btn2: not used due callback_context syntax
    :param btn3: not used due callback_context syntax
    :param btn4: not used due callback_context syntax
    :return: Several possible divs depending which button was clicked. The div is displayed on the page right next
            to the menu. Returned by Output('page-content', 'children')
    """

    ctx = dash.callback_context
    if len(ctx.triggered) > 0:
        if ctx.triggered[0]['value']:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == 'create-button' and user.role == 'master':
                return get_create_study_div()
            if button_id == 'current-studies-button':
                return get_current_studies_div()
            if button_id == 'close-button' and user.role == 'master':
                return get_close_study_div()
            if button_id == 'about-button':
                return get_about_div()
    raise PreventUpdate


@app.callback([Output('create-study-output-state', 'children'),
               Output('create-study-name-input', 'value'),
               Output('create-study-duration-input', 'value'),
               Output('create-study-subject-number', 'value'),
               Output('create-study-description', 'value'),
               Output('create-study-sensors-list', 'value'),
               Output('frequency-list', 'value')],
              [Input('create-study-button', 'n_clicks')],
              [State('create-study-name-input', 'value'),
               State('create-study-duration-input', 'value'),
               State('create-study-subject-number', 'value'),
               State('create-study-description', 'value'),
               State('create-study-sensors-list', 'value'),
               State('frequency-list', 'value')])
def create_study_callback(n_clicks, study_name, study_duration, number_subjects, description, sensors, freq):
    """
     Callback to create a new study on button click. Reacting if the create study button is clicked. Creates a new study
    if input field contains a valid input und the study does not exist yet.

    :param n_clicks: Click counter of create-study-button. Used to determine if button has ever been clicked. Given by
                Input('create-study-button', 'n_clicks')
    :param study_name: Name of the new study. Given by State('create-study-input', 'value')
    :param study_duration: Duration of study in days. Given by State('create-study-duration-input', 'value')
    :param number_subjects: Initial number of subjects enrolled. Subjects are stored with consecutive numbers in name. Given
                by State('create-study-subject-number', 'value')
    :param description: Study description
    :param sensors: List of selected sensors. Given by State('create-study-sensors-checklist', 'value')
    :param freq: Recording frequency
    :return: Output-state if creation was successful or if study already exists. Furthermore, clean input field of
                create-study-input and other fields. Input remains if creation is not successful.
                Returned by Output('create-study-output-state', 'children'), Output('create-study-input', 'value'),
                Output('create-study-duration-input', 'value'), Output('create-study-subject-number', 'value') and
                Output('create-study-sensors-checklist', 'value')
    """

    if n_clicks:
        if not study_name or not study_duration or not sensors or not freq:
            error_output_state = ''
            if not study_name:
                error_output_state = 'Please enter a study name!'
            elif not study_duration:
                error_output_state = 'Please enter a study duration!'
            elif not sensors:
                error_output_state = 'Please select sensors!'
            elif not freq:
                error_output_state = 'Please enter a recording frequency!'
            return error_output_state, study_name, study_duration, number_subjects, description, sensors, freq

        else:
            json_dict = {"name": study_name,
                         "duration": str(study_duration),
                         "number-of-subjects": str(number_subjects),
                         "description": description,
                         "sensor-list": sensors,
                         "enrolled-subjects": [],
                         "frequency": str(freq)}
            new_study = Study.from_json_dict(json_dict)
            try:
                new_study.create()
                return 'You created the study: ' + study_name, '', '', '', '', [], ''
            except StudyAlreadyExistsException:
                return study_name + ' already exists. Please chose another name!', '', study_duration, number_subjects, description, sensors, freq
    else:
        raise PreventUpdate


@app.callback([Output('study-info-wrapper', 'children'),
               Output('study-data-wrapper', 'children'),
               Output('download-unused-sheets-link-wrapper', 'children'),
               Output('push-notification-wrapper', 'children')],
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
        study = Study.from_study_id(study_id)

        try:
            active_subjects_table = study.get_study_data_table()
        except FileNotFoundError:
            active_subjects_table = html.Div("Table file not found")
        except KeyError:
            active_subjects_table = html.Div("Data erroneous")
        except EmptyStudyTableException:
            active_subjects_table = html.Div("No data available")

        return study.get_study_info_div(), active_subjects_table, study.get_download_link_unused_sheets(), study.get_push_notification_div()
    else:
        raise PreventUpdate


@app.callback([Output('close-selected-study-output-state', 'children'),
               Output('close-study-list', 'options')],
              [Input('close-study-confirm-dialog', 'submit_n_clicks')],
              [State('close-study-list', 'value')])
def close_study_callback(confirm_click, study_id):
    """
    Closes chosen study on button click and moves it to archive directory

    :param confirm_click: check if confirm was clicked
    :param study_id: name of study to be closed
    :return: output state and cleans value of study list
    """
    if confirm_click and study_id:
        study_to_close = Study.from_study_id(study_id)
        study_to_close.close()
        remaining = get_study_list_as_dict()
        return html.Div('Study closed.'), remaining
    else:
        raise PreventUpdate


@app.callback(Output('close-study-confirm-dialog', 'displayed'),
              [Input('close-study-button', 'n_clicks')],
              [State('close-study-list', 'value')])
def display_confirm_close_study(n_clicks, study_id):
    if n_clicks and study_id:
        return True
    return False


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
        study_to_extend = Study.from_study_id(study_id)
        study_to_extend.create_additional_subjects(number_of_subjects)
        return "Total number of subject: " + study_to_extend.study_json["number-of-subjects"], ''
    else:
        raise PreventUpdate


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

    selected_study = Study.from_study_id(study_id)
    selected_study.zip_unused_sheets()
    return send_file(dash_study_folder + '/' + study_id + '/' + zip_file,
                     mimetype='application/zip',
                     as_attachment=True)


if __name__ == '__main__':
    app.run_server(debug=True)
