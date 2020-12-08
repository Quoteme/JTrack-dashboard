import dash
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate


from app import app, user
from push_notification.push_notifications import send_push_notification


@app.callback([Output('push-notification-title', 'value'),
               Output('push-notification-text', 'value'),
               Output('receiver-list', 'value'),
               Output('push-notification-output-state', 'children')],
              [Input('user-with-missing-data-button', 'n_clicks'),
               Input('every-user-button', 'n_clicks'),
               Input('send-push-notification-button', 'n_clicks')],
              [State('push-notification-title', 'value'),
               State('push-notification-text', 'value'),
               State('receiver-list', 'value'),
               State('user-with-missing-data-button', 'data-user-list'),
               State('every-user-button', 'data-user-list'),
               State('current-study-list', 'value')])
def push_notifications(autofillbtn1, autofillbtn2, send_button, title, text, receivers, missing_data_users_list, every_user_list , study_id):
    ctx = dash.callback_context

    if len(ctx.triggered) > 0:
        if ctx.triggered[0]['value']:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == 'user-with-missing-data-button':
                return title, text, missing_data_users_list, ''
            if button_id == 'every-user-button':
                return title, text, every_user_list, ''
            if button_id == 'send-push-notification-button' and (user.role == 'master' or user.role == 'invest'):
                if not title or not text or not receivers:
                    error_output_state = ''
                    if not title:
                        error_output_state = 'Please enter a message title!'
                    elif not text:
                        error_output_state = 'Please enter a message!'
                    elif not receivers:
                        error_output_state = 'Please select receivers!'
                    return title, text, receivers, error_output_state
                else:
                    send_push_notification(title, text, receivers, study_id)
                    return '', '', [], 'Push notification sent!'
    raise PreventUpdate
