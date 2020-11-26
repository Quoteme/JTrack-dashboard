
@app.callback([Output('study-info-wrapper', 'children'),
               Output('study-data-wrapper', 'children'),
               Output('download-unused-sheets-link-wrapper', 'children'),
               Output('push-notification-wrapper', 'children')],
              [Input('current-study-list', 'value')])
def display_study_info_callback(study_id):
    """
    Callback to display study info of chosen study on drop down selection. Provides information as well as the
    opportunity to create new subjects.

    :param study_id:  Name of the study which information should be displayed. The value is transferred by a drop down menu.
                Given by Input('current-study-list', 'value')
    :return: Html-Div containing the information of the study and a button for downloading unused sheets.
                Displayed beneath the drop down list. Returned by Output('current-selected-study', 'children').
    """
    if study_id:
        study = Study.from_study_id(study_id)

        try:
            active_subjects_table = study.get_study_data_table()
        except FileNotFoundError:
            active_subjects_table = html.Div("Table file not found")
        except KeyError:
            active_subjects_table = html.Div("Data erroneous")
        except EmptyStudyTableException:
            active_subjects_table = html.Div("No data available")

        return study.get_study_info_div(), active_subjects_table, study.get_download_link_unused_sheets(), study.get_push_notification_div()
    else:
        raise PreventUpdate

@app.server.route('/download-<string:study_id>-<string:user>')
def download_marked_sheets(study_id, user):
    """
    Routing option to access and download subjects sheets. Just selected sheets from enrolled subjects are downloaded.

    :param study_id: study name
    :param user: user name
    :return: Flask send_file delivering zip folder containing selected sheets
    """

    return send_file(dash_study_folder + '/' + study_id + '/' + sheets_folder + '/' + user + '.pdf',
                     mimetype='application/pdf',
                     as_attachment=True)


@app.server.route('/download-<string:study_id>')
def download_sheets(study_id):
    """
    Execute download of subject-sheet-zip which contains all of the subject sheets for every subject of one specified study
    :param study_id: specified study of which the sheets should be downloaded

    :return: Flask send_file which delivers the zip belonging to the study
    """

    selected_study = Study.from_study_id(study_id)
    selected_study.zip_unused_sheets()
    return send_file(dash_study_folder + '/' + study_id + '/' + zip_file,
                     mimetype='application/zip',
                     as_attachment=True)