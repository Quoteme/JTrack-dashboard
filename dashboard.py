import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import os
import shutil
from menu_tabs.about import get_about_div
from menu_tabs.create_study import get_create_study_div, create_study
from menu_tabs.current_studies import get_current_studies_div, get_study_info_div, get_number_enrolled_subjects
from menu_tabs.delete_study import get_delete_study_div, refresh_drop_down
from subject_configuration.create_subjects import create_subjects


# Generate dash app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
logo = app.get_asset_url('jutrack.png')
study_dir = './studies'
os.makedirs(study_dir, exist_ok=True)


def create_menu():
    """Create the menu list on the left site of the page

            Returns
            -------
            Div containing buttons for navigation
    """

    return html.Div(id='menu-items', style={'padding': '12px'}, children=[
        html.Button(id='create-button', children='Create Study'),
        html.Br(),
        html.Button(id='delete-button', children='Delete Study'),
        html.Br(),
        html.Button(id='current-studies', children='Current Studies'),
        html.Br(),
        html.Button(id='about-button', children='About')
    ])


@app.callback(Output('page-content', 'children'),
              [Input('create-button', 'n_clicks'),
               Input('delete-button', 'n_clicks'),
               Input('current-studies', 'n_clicks'),
               Input('about-button', 'n_clicks'),
               ])
def display_menu_tab_content_callback(btn1, btn2, btn3, btn4):
    """Callback reacting if a menu button is clicked. Returns clicked button content

               Parameters
               ----------
                btn1, btn2, btn3, btn4
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
        if button_id == 'delete-button':
            return get_delete_study_div(study_dir)
        if button_id == 'current-studies':
            return get_current_studies_div(study_dir)
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
def update_output(n_clicks, study_name, study_duration, number_subjects, sensors):
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

               Raises
               ------
                PreventUpdate
                    Raise if button was not clicked yet or if the input field is empty when create button is clicked.

               Return
               -------
                    Output-state if creation was successful or if study already exists. Furthermore, clean input field of
                    create-study-input. Returned by Output('create-study-output-state', 'children') and
                    Output('create-study-input', 'value')
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
            if os.path.isdir(study_dir + '/' + study_name):
                return study_name + ' already exists. Please chose another name!', '', study_duration, number_subjects, sensors
            else:
                create_study(study_dir + '/' + study_name, number_subjects)
                return 'You created the study:\t' + study_name, '', '', '', []
    else:
        raise PreventUpdate


@app.callback([Output('delete-study-output-state', 'children'),
               Output('delete-study-list', 'options')],
              [Input('delete-study-button', 'n_clicks')],
              [State('delete-study-list', 'value')])
def delete_study_callback(n_clicks, study_name):
    """
    TODO:   Confirmation dialog
    Callback to delete a chosen study on button click. Input is a value of a drop down menu specifying the study which
    will be deleted on button click. Refreshes the drop down list after deletion.

               Parameters
               ----------
                n_clicks
                    Click counter of delete-study-button. Used to determine if button has ever been clicked. Given by
                    Input('delete-study-button', 'n_clicks').
                study_name
                    Name of the study to delete provided by a drop down menu. Given by State('delete-study-list', 'value').

               Raises
               ------
                PreventUpdate
                    Raise if button was not clicked yet or if the value of the drop down menu is empty when button
                    is clicked.

               Return
               -------
                    Message that deletion was successful. Furthermore, refresh options in drop down menu. Returned by
                     Output('delete-study-output-state', 'children') and Output('delete-study-list', 'options')
       """

    if n_clicks and study_name:
        study_path = study_dir + '/' + study_name
        shutil.rmtree(study_path)
        return 'You removed:\t' + study_name, refresh_drop_down(study_dir)
    else:
        PreventUpdate


@app.callback(Output('current-selected-study', 'children'),
              [Input('current-study-list', 'value')])
def display_study_info_callback(study_name):
    """
    TODO:   Display all enrolled subjects on the right site of the div
            Display more information (total amount of data sent)
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
        selected_study_dir = study_dir + '/' + study_name
        return get_study_info_div(selected_study_dir)
    else:
        PreventUpdate


@app.callback([Output('create-users-output-state', 'children'),
               Output('create_users_input', 'value'),
               Output('number-enrolled-subjects', 'children')],
              [Input('create-users-button', 'n_clicks')],
              [State('create_users_input', 'value'),
               State('current-study-list', 'value')])
def create_subjects_callback(n_clicks, number_users, study_name):
    """Callback to create new subjects on click. Depends on input number and the current study displayed.

               Parameters
               ----------
                n_clicks
                    Click counter of create-users-button. Used to determine if button has ever been clicked. Given by
                    Input('create-users-button', 'n_clicks').
                number_users
                    Number of new subjects to create. Given by State('create_users_input', 'value').
                study_name
                    Name of current study selected. Specifies where to drop the new subjects. Given by
                    State('current-study-list', 'value').

               Raises
               ------
                PreventUpdate
                    Raise if the value of the input field is empty or if the button was not clicked yet.

               Return
               -------
                    Output-state of the procedure. Furthermore, the input field is cleaned and the displayed number of
                    enrolled subjects is refreshed. Returned by Output('create-users-output-state', 'children') and
                    Output('create_users_input', 'value') and Output('number-enrolled-subjects', 'children')
       """

    selected_study_dir = study_dir + '/' + study_name
    if n_clicks and number_users:
        if number_users < 1 or number_users > 500:
            output_state = 'You did not enter a valid number'
        else:
            create_subjects(selected_study_dir, number_users)
            output_state = 'You created ' + str(number_users) + ' new users and QR-Codes'
        n_subj = get_number_enrolled_subjects(selected_study_dir)
        return output_state, '', 'Number of enrolled subjects:\t' + n_subj
    else:
        raise PreventUpdate


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


if __name__ == '__main__':
    app.run_server(debug=True)
