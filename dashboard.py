import dash
import  dash_core_components as dcc
import dash_html_components as html

print(dcc.__version__)
external_stylsheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylsheets)
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    html.H1(children='JuTrack Dashboard', id='index-page-title'),
    html.A('Create Study', href='/create-study')
])

create_study_page = html.Div([
    html.H3(children='Create new study', id='create-study-title'),
    dcc.Input(id='study-name', placeholder='Your study', type='text'),
    html.Button(children='Create', id='create-study-button')
])



# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/create-study':
        return create_study_page
    else:
        return index_page
    # You could also return a 404 "URL not found" page here

if __name__ == '__main__':
    app.run_server(debug=True)