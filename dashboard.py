import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask import send_file

from security.DashboardUser import DashboardUser
from jutrack_dashboard_worker import zip_file, dash_study_folder, get_study_list_as_dict, sheets_folder
from Exceptions import StudyAlreadyExistsException, NoSuchUserException, WrongPasswordException, \
    EmptyStudyTableException
from jutrack_dashboard_worker.Study import Study
from menu_tabs import get_about_div, get_create_study_div, get_current_studies_div, get_close_study_div
from websites import general_page, login_page

# Generate dash app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
user = DashboardUser()
logo1 = app.get_asset_url('Logos.JPG')
logo2 = app.get_asset_url('Logo_BrainandBehaviour.png')


# General dash app layout starting with the login div
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='top-bar', className='row jutrack-background', children=[
        html.Div(id='image-container1', className='column-mid',
                 children=html.Img(id='logo1', src=logo1, className='juelich-icon-header')),
        html.H1(id='header', className='column-medium', children='JuTrack Dashboard',
                style={'color': 'white', 'text-align': 'center',
                       'line-height': '102px', 'vertical-align': 'middle'}),
        html.Div(id='image-container2', className='column-small',
                 children=html.Img(id='logo2', src=logo2, className='bb-icon-header')),
        html.Span(id='logged-in-as')
    ]),
    html.Div(id='menu-and-content', className='row', children=login_page())
])


@app.callback([Output('menu-and-content', 'children'),
               Output('login-output-state', 'children'),
               Output('username', 'value'),
               Output('passwd', 'value'),
               Output('logged-in-as', 'children')],
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
            return general_page(), 'Logged in successfully!', username, '', 'Logged in as: ' + username
        except NoSuchUserException:
            return login_page(), 'No such user!', username, '', ''
        except WrongPasswordException:
            return login_page(), 'Wrong Password!', username, '', ''
    else:
        raise PreventUpdate


@app.callback(Output('page-content', 'children'),
              [Input('create-button', 'n_clicks'),
               Input('current-studies', 'n_clicks'),
               Input('about-button', 'n_clicks'),
               Input('home-button', 'n_clicks'),
               Input('close-button', 'n_clicks')
               ])
def display_menu_tab_content_callback(btn1, btn2, btn3, btn4, btn5):
    """
    Callback reacting if a menu button is clicked. Returns clicked button content

    :param btn1: not used due callback_context syntax
    :param btn2: not used due callback_context syntax
    :param btn3: not used due callback_context syntax
    :param btn4: not used due callback_context syntax
    :param btn5: not used due callback_context syntax
    :return: Several possible divs depending which button was clicked. The div is displayed on the page right next
            to the menu. Returned by Output('page-content', 'children')
    """

    ctx = dash.callback_context
    if len(ctx.triggered) > 0:
        if ctx.triggered[0]['value']:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == 'create-button' and user.role == 'master':
                return get_create_study_div()
            if button_id == 'current-studies':
                return get_current_studies_div()
            if button_id == 'close-button' and user.role == 'master':
                return get_close_study_div()
            if button_id == 'about-button':
                return get_about_div()
            if button_id == 'home-button':
                return html.Div()
    return html.Div()


@app.callback([Output('create-study-output-state', 'children'),
               Output('create-study-name-input', 'value'),
               Output('create-study-duration-input', 'value'),
               Output('create-study-subject-number', 'value'),
               Output('create-study-description', 'value'),
               Output('create-study-sensors-checklist', 'value'),
               Output('frequency-list', 'value')],
              [Input('create-study-button', 'n_clicks')],
              [State('create-study-name-input', 'value'),
               State('create-study-duration-input', 'value'),
               State('create-study-subject-number', 'value'),
               State('create-study-description', 'value'),
               State('create-study-sensors-checklist', 'value'),
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
                return 'You created the study:\t' + study_name, '', '', '', '', [], ''
            except StudyAlreadyExistsException:
                return study_name + ' already exists. Please chose another name!', '', study_duration, number_subjects, description, sensors, freq
    else:
        raise PreventUpdate


@app.callback([Output('current-study-info', 'children'),
               Output('current-study-table', 'children'),
               Output('download-unused-sheets', 'children')],
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

        return study.get_study_info_div(), active_subjects_table, study.get_download_link_unused_sheets()
    else:
        raise PreventUpdate


@app.callback([Output('close-selected-study-output-state', 'children'),
               Output('close-study-list', 'options')],
              [Input('close-study-button', 'n_clicks')],
              [State('close-study-list', 'value')])
def close_study_callback(n_clicks, study_id):
    """
    Closes chosen study on button click and moves it to archive directory

    :param n_clicks: not used
    :param study_id: name of study to be closed
    :return: output state and cleans value of study list
    """
    if n_clicks and study_id:
        study_to_close = Study.from_study_id(study_id)
        study_to_close.close()
        remaining = get_study_list_as_dict()
        return html.Div('Study closed.'), remaining
    else:
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
        study_to_extend = Study.from_study_id(study_id)
        study_to_extend.create_additional_subjects(number_of_subjects)
        return "Total number of subject: " + study_to_extend.study_json["number-of-subjects"], ''
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

    selected_study = Study.from_study_id(study_id)
    selected_study.zip_unused_sheets()
    return send_file(dash_study_folder + '/' + study_id + '/' + zip_file,
                     mimetype='application/zip',
                     as_attachment=True)


if __name__ == '__main__':
    app.run_server(debug=True)
