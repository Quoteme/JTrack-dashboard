import dash_html_components as html
import dash_core_components as dcc


def get_log_in_div():
    return html.Div(id='login-div', children=[
        dcc.Input(id='username', placeholder='Username', type='text'),
        dcc.Input(id='passwd', placeholder='Password', type='password'),
        html.Button(id='login-button', children='Login'),
        html.Span(id='login-output-state', children=''),
    ])


def get_logged_in_div(user):
    return html.Div(id='logged-in-message', children='You are logged in as: ' + user)