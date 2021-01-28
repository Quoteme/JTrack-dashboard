import dash_core_components as dcc
import dash_html_components as html

from security.layout import get_log_in_div
#TODO remove unnecessary divs
#TODO cleanup
hhu_icon = 'assets/icons/hhu-icon.png'
fz_icon = 'assets/icons/fz-icon.png'
bb_icon = 'assets/icons/bb-icon.png'


def get_main_page():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        html.Header(id='page-header', children=get_header()),
        get_log_in_div(),
        html.Div(id='page-body'),
        html.Footer(id='page-footer', children=get_footer())
    ])


def get_header():
    return html.Div(id='header-div', className='row', children=[
        html.Div(id='title-div', children=[
            html.H1(id='title', children='JuTrack Dashboard'),
            html.H6(id='subtitle', children=[
                html.Span('by '),
                html.A('Biomarker Development Group, INM-7',
                       href='https://www.fz-juelich.de/inm/inm-7/EN/Forschung/Biomarker%20Development/artikel.html?nn=654270',
                       target='_blank', rel='noreferrer')])
        ]),
        html.Div(id='icons-div', children=[
            html.A(html.Img(style={'border-left': '0'}, src=hhu_icon), href='https://www.medizin.hhu.de/',
                   target='_blank', rel='noreferrer'),
            html.A(html.Img(style={'border-left': '0'}, src=fz_icon),
                   href='https://www.fz-juelich.de/portal/EN/Home/home_node.html', target='_blank',
                   rel='noreferrer'),
            html.A(html.Img(style={'border-left': '0', 'border-right': '0'}, src=bb_icon),
                   href='https://www.fz-juelich.de/inm/inm-7/EN/Home/home_node.html', target='_blank',
                   rel='noreferrer')
        ]),
    ])


def get_body():
    return html.Div(id='body-div', className='row', children=[
        get_menu(),
        html.Div(id='content-div')
    ])


def get_footer():
    return html.Div(id='footer-div', children=[
        html.Div(id='info-text', children=[
            html.P(children=
                   "You are visiting the JuTrack website which provides access to the dashboard for managing research studies "
                   "running on the JuTrack mobile platform."),
            html.P(children=
                   "JuTrack is developed by the Group Biomarker Development of the Institute "
                   "for Neuroscience and Medicine 7 (Brain and Behaviour) at the Forschungszentrum Jülich. It is a multifunctional "
                   "Android-based digital biomarker platform for collection of sensor, mobile usage and ecological momentary assessment "
                   "information from mobile and wearable devices."),
            html.P(children=
                   "JuTrack is developed as an open source solution (release in preparation, "
                   "Sahandi-Far et al.). It is currently deployed in several clinical and mobile health studies. If you are interested "
                   "in collaboration with us or would like to learn more about JuTrack or our studies please reach out to "
                   "Dr. Juergen Dukart (j.dukart@fz-juelich.de)."),
            html.P(children=["You can find more information about our group on: ", html.A(
                children="https://www.fz-juelich.de/inm/inm-7/EN/Forschung/Biomarker%20Development/_node.html",
                href="https://www.fz-juelich.de/inm/inm-7/EN/Forschung/Biomarker%20Development/_node.html")]),
        ])
    ])


def get_menu():
    return html.Div(id='menu-div', children=[
        html.Button(id='create-button', children='Create Study'),
        html.Button(id='current-studies-button', children='Current Studies', className='top-border'),
        html.Button(id='close-button', children='Close Study', className='top-border'),
        html.Button(id='about-button', children='About', className='top-border'),
    ])
