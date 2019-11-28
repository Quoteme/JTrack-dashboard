import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import os
import menu_tabs.about as about
import menu_tabs.create_study as create_study
import menu_tabs.current_studies as current_studies


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
        html.Button(id='current-studies', children='Current studies'),
        html.Br(),
        html.Button(id='about-button', children='About')
    ])


# General dash app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='top-bar', className='row', style={'background-color': '#004176'}, children=[
        html.Div(id='image-container', className='column', children=html.Img(id='image', src=logo,
                                                                             style={'padding': '12px', 'width': '192px',
                                                                                    'height': '128px'})),
        html.H1(id='header', className='column-big', children='JuTrack Dashboard', style={'color': 'white', 'text-align': 'center',
                                                                  'line-height': '102px', 'vertical-align': 'middle'})
    ]),
    html.Div(id='menu-and-content', className='row', children=[
        html.Div(id='menu', className='column', children=[
            html.H3(id='menu-title', style={'padding': '12 px'}, children='Menu'),
            create_menu()]),
        html.Div(id='page-content',style={'margin': '12px'}, className='column-big')
    ]),
])


@app.callback(Output('page-content', 'children'),
              [Input('create-button', 'n_clicks'),
               Input('about-button', 'n_clicks'),
               Input('current-studies', 'n_clicks')
               ])
def display_menu_tab_content(btn1, btn2, btn3):
    ctx = dash.callback_context

    if ctx.triggered[0]['value']:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'create-button':
            return create_study.get_create_study_div(study_dir)
        if button_id == 'current-studies':
            return current_studies.get_current_studies_div(study_dir)
        if button_id == 'about-button':
            return about.get_about_div()
    else:
        return


@app.callback(Output('output-state', 'children'),
              [Input('create-study-button', 'n_clicks')],
              [State('study-name', 'value')])
def create_new_study_folder(n_clicks, input1):
    if n_clicks and input1:
        if os.path.isdir(study_dir + '/' + input1):
            return input1 + ' already exists'
        os.makedirs(study_dir + '/' + input1)
        os.system('python create_random_users.py ' + input1 + ' 15')
        return 'You created the study:\t' + input1
    else:
        raise PreventUpdate


@app.callback(Output('selected-study', 'children'),
              [Input('study-list', 'value')])
def display_study_info(study_name):
    if study_name:
        study_path = study_dir + '/' + study_name
        enrolled_subjects = os.listdir(study_path)
        n_subj = str(len(enrolled_subjects))
        return html.Div([
            html.H2(children=study_name),
            html.P(children='Number of enrolled subjects:\t' + n_subj),
        ])
    else:
        PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
