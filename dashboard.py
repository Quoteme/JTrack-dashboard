import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask import send_file

from jutrack_dashboard_worker import zip_file, dash_study_folder
from jutrack_dashboard_worker.Exceptions import StudyAlreadyExistsException
from jutrack_dashboard_worker.Study import Study
from menu_tabs import get_about_div, get_create_study_div, get_current_studies_div, create_menu, get_close_study_div

# Generate dash app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': 'ju7r4K!'
}
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

logo = app.get_asset_url('jutrack.png')

# General dash app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='top-bar', className='row jutrack-background', children=[
        html.Div(id='image-container', className='column-small',
                 children=html.Img(id='image', src=logo, className='jutrack-icon-header')),
        html.H1(id='header', className='column-big', children='JuTrack Dashboard',
                style={'color': 'white', 'text-align': 'center',
                       'line-height': '102px', 'vertical-align': 'middle'})
    ]),
    html.Div(id='menu-and-content', className='row', children=[
        html.Div(id='menu', className='column-small jutrack-background', style={'margin': '6px'}, children=
        [html.H2(id='menu-title', style={'color': 'white', 'margin': '6px'}, children='Menu'), create_menu()]),
        html.Div(id='page-content', style={'margin': '12px'}, className='column-big row')
    ]),
])


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

    if ctx.triggered[0]['value']:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'create-button':
            return get_create_study_div()
        if button_id == 'current-studies':
            return get_current_studies_div()
        if button_id == 'close-button':
            return get_close_study_div()
        if button_id == 'about-button':
            return get_about_div()
        if button_id == 'home-button':
            return html.Div()
    else:
        return


@app.callback([Output('create-study-output-state', 'children'),
               Output('create-study-name-input', 'value'),
               Output('create-study-duration-input', 'value'),
               Output('create-study-subject-number', 'value'),
               Output('create-study-description', 'value'),
               Output('create-study-sensors-checklist', 'value')],
              [Input('create-study-button', 'n_clicks')],
              [State('create-study-name-input', 'value'),
               State('create-study-duration-input', 'value'),
               State('create-study-subject-number', 'value'),
               State('create-study-description', 'value'),
               State('create-study-sensors-checklist', 'value')])
def create_study_callback(n_clicks, study_name, study_duration, number_subjects, description, sensors):
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
    :return: Output-state if creation was successful or if study already exists. Furthermore, clean input field of
                create-study-input and other fields. Input remains if creation is not successful.
                Returned by Output('create-study-output-state', 'children'), Output('create-study-input', 'value'),
                Output('create-study-duration-input', 'value'), Output('create-study-subject-number', 'value') and
                Output('create-study-sensors-checklist', 'value')
    """

    if n_clicks:
        if not study_name or not study_duration or not sensors:
            if not study_name:
                output_state = 'Please enter a study name!'
            elif not study_duration:
                output_state = 'Please enter a study duration!'
            elif not sensors:
                output_state = 'Please select sensors!'
            return output_state, study_name, study_duration, number_subjects, description, sensors

        else:
            json_dict = {"name": study_name,
                         "duration": str(study_duration),
                         "number-of-subjects": str(number_subjects),
                         "description": description,
                         "sensor-list": sensors,
                         "enrolled-subjects": []}
            new_study = Study.from_json_dict(json_dict)
            try:
                new_study.create()
                return 'You created the study:\t' + study_name, '', '', '', '', []
            except StudyAlreadyExistsException:
                return study_name + ' already exists. Please chose another name!', '', study_duration, number_subjects, description, sensors
    else:
        raise PreventUpdate


@app.callback([Output('current-selected-study', 'children'),
               Output('download-unused-sheets-zip', 'href')],
              [Input('current-study-list', 'value')])
def display_study_info_callback(study_id):
    """
    Callback to display study info of chosen study on drop down selection. Provides information as well as the
    opportunity to create new subjects.

    :param study_id:  Name of the study which information should be displayed. The value is transferred by a drop down menu.
                Given by Input('current-study-list', 'value')
    :return: Html-Div containing the information of the study. Displayed beneath the drop down list. Returned
                by Output('current-selected-study', 'children'). Also returning a href containing the link to
                download subject sheets in Output('download-sheet-zip', 'href')
    """

    if study_id:
        study = Study.from_study_id(study_id)
        return study.get_study_info_div(), '/download-unused-sheets-zip-' + study_id
    else:
        PreventUpdate
    return html.Div(''), ''


@app.callback(Output('close-selected-study-output-state', 'children'),
              [Input('close-study-button', 'n_clicks')],
              [State('close-study-list', 'value')])
def close_study_callback(btn, study_id):
    """
    Closes chosen study on button click and moves it to archive directory

    :param btn: not used
    :param study_id: name of study to be closed
    :return: cleans value of study list
    """
    try:
        if study_id:
            study_to_close = Study.from_study_id(study_id)
            study_to_close.close()
            return html.Div('Study closed.')
    except FileNotFoundError:
        return html.Div('Study already closed!')
    return html.Div('')


@app.callback([Output('total-subjects', 'children'),
               Output('create-additional-subjects-input', 'value')],
              [Input('create-additional-subjects-button', 'n_clicks')],
              [State('current-study-list', 'value'),
               State('create-additional-subjects-input', 'value')])
def create_additional_subjects_callback(btn, study_id, number_of_subjects):
    """
    Creates additional subjects on button click. QR-Codes and study sheets are added to the existing directories

    :param btn: not used
    :param study_id: study receiving new subjects
    :param number_of_subjects: number of new subjects
    :return: refreshes current number of subjects state and clears input field
    """
    study_to_extend = Study.from_study_id(study_id)
    if number_of_subjects:
        study_to_extend.create_additional_subjects(number_of_subjects)
    return "Total number of subject: " + study_to_extend.study_json["number-of-subjects"], ''


@app.callback(Output('download-marked-sheets-zip', 'href'),
              [Input('table', 'selected_row_ids')],
              [State('current-study-list', 'value')])
def update_marked_sheets_download_link_callback(selected_rows, study_id):
    """
    On marking sheets in the information table, the download link will be updated containing the IDs of every marked subject

    :param selected_rows: list of selected subjects
    :param study_id: selected study
    :return:
    """
    if len(selected_rows) and study_id:
        return '/download-marked-sheets-zip-' + (study_id + '-' + '-'.join(selected_rows))
    else:
        PreventUpdate


@app.server.route('/download-marked-sheets-zip-<string:study_id_and_row_ids>')
def download_marked_sheets(study_id_and_row_ids):
    """
    Routing option to access and download subjects sheets. Just selected sheets from enrolled subjects are downloaded.

    :param study_id_and_row_ids: link containing the study name and the list of selected sheets ("-" - separated)
    :return: Flask send_file delivering zip folder containing selected sheets
    """
    study_id = str(study_id_and_row_ids).split('-')[0]
    marked_sheets = str(study_id_and_row_ids).split('-')[1:]

    selected_study = Study.from_study_id(study_id)
    selected_study.zip_marked_sheets(marked_sheets)
    return send_file(dash_study_folder + '/' + study_id + '/' + zip_file,
                     mimetype='application/zip',
                     as_attachment=True)


@app.server.route('/download-unused-sheets-zip-<string:study_id>')
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
