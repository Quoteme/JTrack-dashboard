import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import os

# Declare paths
cwd = os.getcwd()
working_dir = './working'
study_dir = working_dir + '/studies'

# Basic css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True


# General page layout, changes page when URL is modified (c. display_page function below)
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# Start page
def make_index_page():
    return html.Div([
        html.H1(children='JuTrack Dashboard', id='index-page-title'),
        html.P(children='Welcome to JuTrack'),
        dcc.Link(children='Create Study', href='/create-study')
    ])


# Page for creating new studies
def make_study_control_page():
    return html.Div([
        html.H2(children='Create new study', id='create-study-title'),
        dcc.Input(id='study-name', placeholder='Your study', type='text'),
        html.A(children=html.Button(id='create-study-button', children='Create'), href='/create-study'),
        html.Br(),
        html.Div(id='output-state'),
        html.Br(),
        html.P(children='Current studies:'),
        html.Div(get_current_studies()),
        dcc.Link(children='Home', href='/')
    ])


# Display study info
def make_study_info_page(study):
    study_path = study_dir + '/' + study
    n_subj = str(len(os.listdir(study_path)))

    return html.Div([
        html.H2(children=study),
        html.P(children='Number of enrolled subjects:\t' + n_subj),
        dcc.Link(children='Back', href='/create-study'),
        html.Br(),
        dcc.Link(children='Home', href='/')
    ])


def get_current_studies():
    html_study_list = []
    current_studies = os.listdir(study_dir)
    print(current_studies)
    for study in current_studies:
        html_study_list.append(dcc.Link(children=study, href='/create-study/' + study))
        html_study_list.append(html.Br())
    html_study_list.append(html.Br())
    return html_study_list


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    pathname = str(pathname)
    if pathname.endswith('/'):
        return make_index_page()
    elif pathname.endswith('/create-study'):
        return make_study_control_page()
    elif pathname.find('create-study/') != -1:
        return make_study_info_page(pathname.split('/')[-1])
    else:
        return make_index_page()


@app.callback(Output('output-state', 'children'),
              [Input('create-study-button', 'n_clicks')],
              [State('study-name', 'value')])
def create_new_study_folder(n_clicks, input1):
    if n_clicks and input1:
        os.system('mkdir ' + study_dir + '/' + input1)
        os.system('python create_random_users.py ' + input1 + ' 15')
        return "You created the study:\t" + input1
    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
