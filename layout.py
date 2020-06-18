import dash_core_components as dcc
import dash_html_components as html


def get_main_page():
    hhu_icon = 'assets/hhu-icon.png'
    fz_icon = 'assets/fz-icon.png'
    bb_icon = 'assets/bb-icon.png'

    return html.Div([
        dcc.Location(id='url', refresh=False),
        html.Header(id='page-header', className='row', children=[
            html.Div(id='title-wrapper', style={'float': 'left'}, children=[
                html.H1(id='title', children='JuTrack Dashboard'),
                html.H6(id='subtitle', children=[
                    html.Span('by '),
                    html.A('Biomarker Development Group, INM-7',
                           href='https://www.fz-juelich.de/inm/inm-7/EN/Forschung/Biomarker%20Development/artikel.html?nn=654270',
                           target='_blank', rel='noreferrer')])
            ]),
            html.Div(id='icons-wrapper', style={'float': 'right'}, children=[
                html.A(html.Img(style={'border-left': '0'}, src=hhu_icon), href='https://www.medizin.hhu.de/',
                       target='_blank', rel='noreferrer'),
                html.A(html.Img(style={'border-left': '0'}, src=fz_icon),
                       href='https://www.fz-juelich.de/portal/EN/Home/home_node.html', target='_blank',
                       rel='noreferrer'),
                html.A(html.Img(style={'border-left': '0', 'border-right': '0'}, src=bb_icon),
                       href='https://www.fz-juelich.de/inm/inm-7/EN/Home/home_node.html', target='_blank',
                       rel='noreferrer')
            ]),
        ]),
        html.Div(id='login-wrapper', children=get_log_in_div()),
        html.Div(id='menu-and-content', className='row'),
        html.Span(id='logged-in-as')
    ])


def get_log_in_div():
    return html.Div(id='login-div', children=[
                dcc.Input(id='username', placeholder='Username', type='text'),
                dcc.Input(id='passwd', placeholder='Password', type='password'),
                html.Button(id='login-button', children='Login'),
                html.Span(id='login-output-state', children=''),
    ])


def get_logged_in_div(user):
    return html.Div(id='logged-in-message', children='You are logged in as: ' + user)
