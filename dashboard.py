import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask import send_file

from jutrack_dashboard_worker import create_study, get_study_information
from menu_tabs import get_about_div, get_create_study_div, get_current_studies_div, create_menu
import json

# Generate dash app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
logo = app.get_asset_url('jutrack.png')

# General dash app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='top-bar', className='row', style={'border-radius': '10px', 'background-color': '#004176'}, children=[
        html.Div(id='image-container', className='column', children=html.Img(id='image', src=logo,
                                                                             style={'padding': '12px', 'width': '192px',
                                                                                    'height': '128px'})),
        html.H1(id='header', className='column-big', children='JuTrack Dashboard',
                style={'color': 'white', 'text-align': 'center',
                       'line-height': '102px', 'vertical-align': 'middle'})
    ]),
    html.Div(id='menu-and-content', className='row', children=[
        html.Div(id='menu', className='column', style={'margin': '6px', 'border-radius': '3px', 'background-color': '#004176'}, children=[
            html.H2(id='menu-title', style={'color': 'white', 'margin': '6px'}, children='Menu'),
            create_menu()]),
        html.Div(id='page-content', style={'margin': '12px'}, className='column-big row')
    ]),
])


@app.callback(Output('page-content', 'children'),
              [Input('create-button', 'n_clicks'),
               Input('current-studies', 'n_clicks'),
               Input('about-button', 'n_clicks'),
               ])
def display_menu_tab_content_callback(btn1, btn2, btn3):
    """Callback reacting if a menu button is clicked. Returns clicked button content

               Parameters
               ----------
                btn1, btn2, btn3
                    Click counter of buttons. Not used due to dash.callback_context syntax. Given by
                    Inputs('button', 'n_clicks').

               Returns
               -------
                Several possible divs depending which button was clicked. The div is displayed on the page right next
                to the menu. Returned by Output('page-content', 'children').
       """

    ctx = dash.callback_context

    if ctx.triggered[0]['value']:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'create-button':
            return get_create_study_div()
        if button_id == 'current-studies':
            return get_current_studies_div()
        if button_id == 'about-button':
            return get_about_div()
    else:
        return


@app.callback([Output('create-study-output-state', 'children'),
               Output('create-study-name-input', 'value'),
               Output('create-study-duration-input', 'value'),
               Output('create-study-subject-number', 'value'),
               Output('create-study-sensors-checklist', 'value')],
              [Input('create-study-button', 'n_clicks')],
              [State('create-study-name-input', 'value'),
               State('create-study-duration-input', 'value'),
               State('create-study-subject-number', 'value'),
               State('create-study-sensors-checklist', 'value')])
def create_study_callback(n_clicks, study_name, study_duration, number_subjects, sensors):
    """
    TODO:   Give a certain pattern for study names
    Callback to create a new study on button click. Reacting if the create study button is clicked. Creates a new study
    if input field contains a valid input und the study does not exist yet.

               Parameters
               ----------
                n_clicks
                    Click counter of create-study-button. Used to determine if button has ever been clicked. Given by
                    Input('create-study-button', 'n_clicks').
                study_name
                    Name of the new study. Given by State('create-study-input', 'value').
                study_duration
                    Duration of study in days. Given by State('create-study-duration-input', 'value').
                number_subjects
                    Initial number of subjects enrolled. Subjects are stored with consecutive numbers in name. Given
                    by State('create-study-subject-number', 'value').
                sensors
                    List of selected sensors. Given by State('create-study-sensors-checklist', 'value').

               Raises
               ------
                PreventUpdate
                    Raise if button was not clicked yet or if the input field is empty when create button is clicked.

               Return
               -------
                    Output-state if creation was successful or if study already exists. Furthermore, clean input field of
                    create-study-input and other fields. Input remains if creation is not successful.
                    Returned by Output('create-study-output-state', 'children'), Output('create-study-input', 'value'),
                    Output('create-study-duration-input', 'value'), Output('create-study-subject-number', 'value') and
                    Output('create-study-sensors-checklist', 'value').
       """
    if n_clicks:
        output_state = ''
        if not study_name or not study_duration or not sensors:
            if not study_name:
                output_state = 'Please enter a study name!'
            elif not study_duration:
                output_state = 'Please enter a study duration!'
            elif not sensors:
                output_state = 'Please select sensors!'
            return output_state, study_name, study_duration, number_subjects, sensors

        else:
            new_study_json_str = json.dumps({"name": study_name,
                                         "duration": study_duration,
                                         "number-of-subjects": number_subjects,
                                         "sensor-list": sensors})
            new_study_json = json.loads(new_study_json_str)
            if create_study(new_study_json):
                return 'You created the study:\t' + study_name, '', '', '', []
            else:
                return study_name + ' already exists. Please chose another name!', '', study_duration, number_subjects, sensors

    else:
        raise PreventUpdate


@app.callback([Output('current-selected-study', 'children'),
              Output('download-sheet-zip', 'href')],
              [Input('current-study-list', 'value')])
def display_study_info_callback(study_name):
    """
    TODO:   Display subject information as a table below.
    Callback to display study info of chosen study on drop down selection. Provides information as well as the
    opportunity to create new users.

               Parameters
               ----------
                study_name
                    Name of the study which information should be displayed. The value is transferred by a drop down menu.
                    Given by Input('current-study-list', 'value').

               Raises
               ------
                PreventUpdate
                    Raise if the value of the drop down menu is empty

               Return
               -------
                    Html-Div containing the information of the study. Displayed beneath the drop down list. Returned
                    by Output('current-selected-study', 'children').
       """

    if study_name:
        return get_study_information(study_name), '/download-sheets-' + study_name
    else:
        PreventUpdate


@app.server.route('/download-sheets-<string:study_name>')
def download_sheets(study_name):
    return send_file('Subject-Sheets/' + study_name + '_subject_sheets.zip',
                     mimetype='application/zip',
                     as_attachment=True)


if __name__ == '__main__':
    app.run_server(debug=True)
