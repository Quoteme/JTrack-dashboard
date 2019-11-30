import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import os
import shutil
from menu_tabs.about import get_about_div
from menu_tabs.create_study import get_create_study_div
from menu_tabs.current_studies import get_current_studies_div, get_study_info_div, get_number_enrolled_subjects
from menu_tabs.delete_study import get_delete_study_div, refresh_drop_down
from create_users import create_users


# Generate dash app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
logo = app.get_asset_url('jutrack.png')
study_dir = './studies'
os.makedirs(study_dir, exist_ok=True)


# Create menu bar
def create_menu():
    return html.Div(id='menu-items', style={'padding': '12px'}, children=[
        html.Button(id='create-button', children='Create Study'),
        html.Br(),
        html.Button(id='delete-button', children='Delete Study'),
        html.Br(),
        html.Button(id='current-studies', children='Current Studies'),
        html.Br(),
        html.Button(id='about-button', children='About')
    ])


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
        html.Div(id='menu', className='column', style={'margin': '6px', 'border-style': 'solid', 'border-color': '#004176'}, children=[
            html.H2(id='menu-title', style={'margin': '6px'}, children='Menu'),
            create_menu()]),
        html.Div(id='page-content', style={'margin': '12px'}, className='column-big')
    ]),
])


@app.callback(Output('page-content', 'children'),
              [Input('create-button', 'n_clicks'),
               Input('delete-button', 'n_clicks'),
               Input('current-studies', 'n_clicks'),
               Input('about-button', 'n_clicks'),
               ])
def display_menu_tab_content_callback(btn1, btn2, btn3, btn4):
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
               Output('create-study-input', 'value')],
              [Input('create-study-button', 'n_clicks')],
              [State('create-study-input', 'value')])
def create_new_study_callback(n_clicks, study_name):
    if n_clicks and study_name:
        if os.path.isdir(study_dir + '/' + study_name):
            return study_name + ' already exists', ''
        else:
            os.makedirs(study_dir + '/' + study_name)
            os.makedirs(study_dir + '/' + study_name + '/QR-Codes')
            return 'You created the study:\t' + study_name, ''
    else:
        raise PreventUpdate


@app.callback([Output('delete-study-output-state', 'children'),
               Output('to-delete-study-list', 'options')],
              [Input('delete-study-button', 'n_clicks')],
              [State('to-delete-study-list', 'value')])
def delete_study_callback(btn1, study_name):
    if btn1 and study_name:
        study_path = study_dir + '/' + study_name
        shutil.rmtree(study_path)
        return 'You removed:\t' + study_name, refresh_drop_down(study_dir)
    else:
        PreventUpdate


@app.callback(Output('current-selected-study', 'children'),
              [Input('current-study-list', 'value')])
def display_study_info_callback(study_name):
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
def create_users_callback(n_clicks, number_users, study_name):
    selected_study_dir = study_dir + '/' + study_name
    if n_clicks and number_users:
        if number_users < 1 or number_users > 500:
            output_state = 'You did not enter a valid number'
        else:
            create_users(selected_study_dir, number_users)
            output_state = 'You created ' + str(number_users) + ' new users and QR-Codes'
        n_subj = get_number_enrolled_subjects(selected_study_dir)
        return output_state, '', 'Number of enrolled subjects:\t' + n_subj
    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
