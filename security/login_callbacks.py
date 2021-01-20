from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

from app import app, user
from exceptions.Exceptions import MissingCredentialsException, NoSuchUserException, WrongPasswordException
from layout import get_body
from security.layout import get_logged_in_div, get_log_in_div


@app.callback([Output('login-div', 'children'),
               Output('page-body', 'children'),
               Output('login-output-state', 'children'),
               Output('username', 'value'),
               Output('passwd', 'value')],
              [Input('login-button', 'n_clicks')],
              [State('username', 'value'),
               State('passwd', 'value')])
def display_page_callback(login_click, username, password):
    """

    :param login_click: login button click
    :param username: username of login
    :param password: password of login

    :return: content div (general content with menu or the login page if login was erroneous)
    """
    if login_click:
        try:
            user.login(username, password)
            return get_logged_in_div(username), get_body(), 'Logged in successfully!', username, ''
        except NoSuchUserException:
            return get_log_in_div(), '', 'This user does not exist!', username, ''
        except WrongPasswordException:
            return get_log_in_div(), '', 'Wrong Password!', username, ''
        except MissingCredentialsException:
            return get_log_in_div(), '', 'Please enter your credentials', username, ''
    else:
        raise PreventUpdate