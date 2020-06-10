import dash_html_components as html
import dash_core_components as dcc

from menu_tabs import create_menu


def page_not_found():
	"""
	Page not found (404) site

	:return: Div for page not found
	"""
	return html.Div(children=[html.H1("404 Error"), html.H3("Page not found")])


def general_page():
	"""
	General page with menu and div for content

	:return: Div for general layout
	"""
	return [html.Div(id='menu', className='column-small jutrack-background', style={'margin': '6px'}, children=[
		html.H2(id='menu-title', style={'color': 'white', 'margin': '6px'}, children='Menu'), create_menu()]),
			html.Div(id='page-content', style={'margin': '12px'}, className='column-big row')]


def login_page():
	"""
	Login page

	:return: Div for logging in
	"""
	return html.Div(className='row', children=[
		html.Div(id='login', className='center column-small ', children=[
			html.Div(style={'padding': '12px'}, children=[
				html.Span("Username:"),
				dcc.Input(id='username', placeholder='Username', type='text', style={'margin-left': '9px'})]),
			html.Div(style={'padding': '12px'}, children=[
				html.Span("Password:"),
				dcc.Input(id='passwd', placeholder='Password', type='password', style={'margin-left': '12px'})]),
			html.Button(id='login-button', children='Login', style={'margin': '16px'}),
			html.Br(),
			html.Span(id='login-output-state', children='')]),
		html.Div(className='column-big welcome', children=[
			html.Span(
				"You are visiting the JuTrack website which provides access to the dashboard for managing research studies "
				"running on the JuTrack mobile platform."),
			html.Br(),
			html.Span(
				"JuTrack is developed by the Group Biomarker Development of the Institute "
				"for Neuroscience and Medicine 7 (Brain and Behaviour) at the Forschungszentrum Jülich. It is a multifunctional "
				"Android-based digital biomarker platform for collection of sensor, mobile usage and ecological momentary assessment "
				"information from mobile and wearable devices."),
			html.Br(),
			html.Span(
				"JuTrack is developed as an open source solution (release in preparation, "
				"Sahandi-Far et al.). It is currently deployed in several clinical and mobile health studies. If you are interested "
				"in collaboration with us or would like to learn more about JuTrack or our studies please reach out to "
				"Dr. Juergen Dukart (j.dukart@fz-juelich.de)."),
			html.Br(),
			html.Span(
				"You can find more information about our group on: "),
			html.A(children="https://www.fz-juelich.de/inm/inm-7/EN/Forschung/Biomarker%20Development/_node.html",
				   href="https://www.fz-juelich.de/inm/inm-7/EN/Forschung/Biomarker%20Development/_node.html")])
	])
