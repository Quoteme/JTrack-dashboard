import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import os

cwd = os.getcwd()
working_dir= './workingdir'
study_dir = working_dir + '/studies'

external_stylsheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylsheets)
app.config.suppress_callback_exceptions = True


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    html.H1(children='JuTrack Dashboard', id='index-page-title'),
    html.P(children='Welcome to JuTrack'),
    html.A(children='Create Study', href='/create-study')
])

study_control_page = html.Div([
    html.H3(children='Create new study', id='create-study-title'),
    dcc.Input(id='study-name', placeholder='Your study', type='text'),
    html.Button(id='create-study-button', children='Create'),
    html.Br(),
    html.Br(),
    html.Div(id='output-state'),
    html.Br(),
    html.A(children='Home', href='/')
])


# Update the index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/create-study':
        return study_control_page
    else:
        return index_page


@app.callback(Output('output-state', 'children'),
              [Input('create-study-button', 'n_clicks')],
              [State('study-name', 'value')])
def create_new_study_folder(n_clicks, input1):
    if n_clicks and input1:
        print(n_clicks)
        os.system('mkdir ' + study_dir + '/' + input1)
        return "You created the study:\t", input1


if __name__ == '__main__':
    app.run_server(debug=True)