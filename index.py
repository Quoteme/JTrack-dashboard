import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from about.layout import get_about_div
from app import app, user
from layout import get_main_page
from study.close_study.layout import get_close_study_div
from study.create_study.layout import get_create_study_div
from study.display_study.layout import get_current_studies_div

from study.display_study import display_callbacks
from study.create_study import create_callbacks
from study.close_study import close_callbacks
from security import login_callbacks
from push_notification import push_notification_callbacks


@app.callback(Output('content-div', 'children'),
              [Input('create-button', 'n_clicks'),
               Input('current-studies-button', 'n_clicks'),
               Input('about-button', 'n_clicks'),
               Input('close-button', 'n_clicks')
               ])
def display_menu_tab_content_callback(create_btn, current_btn, about_btn, close_btn):
    """
    Callback reacting if a menu button is clicked. Returns clicked button content

    :param create_btn: not used due callback_context syntax
    :param current_btn: not used due callback_context syntax
    :param about_btn: not used due callback_context syntax
    :param close_btn: not used due callback_context syntax
    :return: Several possible divs depending which button was clicked. The div is displayed on the page right next
            to the menu. Returned by Output('page-content', 'children')
    """

    ctx = dash.callback_context
    if len(ctx.triggered) > 0:
        if ctx.triggered[0]['value']:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == 'create-button' and user.role == 'master':
                return get_create_study_div()
            if button_id == 'current-studies-button':
                return get_current_studies_div()
            if button_id == 'close-button' and user.role == 'master':
                return get_close_study_div()
            if button_id == 'about-button':
                return get_about_div()
    raise PreventUpdate


app.layout = get_main_page()


if __name__ == '__main__':
    app.run_server(debug=True)
