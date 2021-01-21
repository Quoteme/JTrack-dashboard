import getpass
import dash
import os

# Paths to storage directory and for the qrcodes + subject sheets
from security.DashboardUser import DashboardUser

dash_study_folder = 'Studies'
os.makedirs(dash_study_folder, exist_ok=True)
sheets_folder = 'Subject-Sheets'
qr_folder = 'QR-Codes'
zip_file = 'sheets.zip'

storage_folder = os.path.join('/', 'mnt', 'jutrack_data')
studies = 'studies'
archive = 'archive'
users = 'users'
csv_prefix = 'jutrack_dashboard_'

if getpass.getuser() == 'msfz' or getpass.getuser() == 'micst':
    home = os.path.expanduser('~')
    storage_folder = os.path.join(os.path.expanduser('~'), 'mnt', 'jutrack_data')
    os.makedirs(os.path.join(storage_folder, studies), exist_ok=True)
    os.makedirs(os.path.join(storage_folder, archive), exist_ok=True)

studies_folder = os.path.join(storage_folder, studies)
archive_folder = os.path.join(storage_folder, archive)
users_folder = os.path.join(storage_folder, users)

user = DashboardUser()
app = dash.Dash(__name__, suppress_callback_exceptions=True)
