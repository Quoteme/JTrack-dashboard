from dash import dash
import os

# Paths to storage directory and for the qrcodes + subject sheets
dash_study_folder = 'Studies'
os.makedirs(dash_study_folder, exist_ok=True)
sheets_folder = 'Subject-Sheets'
qr_folder = 'QR-Codes'
zip_file = 'sheets.zip'

storage_folder = '/mnt/jutrack_data'
csv_prefix = 'jutrack_dashboard_'

studies_folder = storage_folder + '/studies'
archive_folder = storage_folder + '/archive'
users_folder = storage_folder + '/users'

timestamp_format = "%Y-%m-%d %H:%M:%S"

app = dash.Dash(__name__, suppress_callback_exceptions=True)
