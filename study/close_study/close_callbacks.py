@app.callback([Output('close-selected-study-output-state', 'children'),
               Output('close-study-list', 'options')],
              [Input('close-study-confirm-dialog', 'submit_n_clicks')],
              [State('close-study-list', 'value')])
def close_study_callback(confirm_click, study_id):
    """
    Closes chosen study on button click and moves it to archive directory

    :param confirm_click: check if confirm was clicked
    :param study_id: name of study to be closed
    :return: output state and cleans value of study list
    """
    if confirm_click and study_id:
        study_to_close = Study.from_study_id(study_id)
        study_to_close.close()
        remaining = get_study_list_as_dict()
        return html.Div('Study closed.'), remaining
    else:
        raise PreventUpdate


@app.callback(Output('close-study-confirm-dialog', 'displayed'),
              [Input('close-study-button', 'n_clicks')],
              [State('close-study-list', 'value')])
def display_confirm_close_study(n_clicks, study_id):
    if n_clicks and study_id:
        return True
    return False