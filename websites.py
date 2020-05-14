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
	return [html.Div(id='menu', className='column-small jutrack-background', style={'margin': '6px'},
					 children=[html.H2(id='menu-title', style={'color': 'white', 'margin': '6px'}, children='Menu'),
							   create_menu()]),
			html.Div(id='page-content', style={'margin': '12px'}, className='column-big row')]


def login_page():
	"""
	Login page

	:return: Div for logging in
	"""
	return [html.Div(id='login', className='center', children=[
		html.Div(children=[html.Span("Username:"), dcc.Input(id='username', placeholder='Username', type='text', style={'margin-left': '9px'})], style={'padding': '12px'}),
		html.Div(children=[html.Span("Password:"), dcc.Input(id='passwd', placeholder='Password', type='password', style={'margin-left': '12px'})], style={'padding': '12px'}),
		html.Button(id='login-button', children='Login', style={'margin': '16px'}),
		html.Br(),
		html.Span(id='login-output-state', children='')
	])]
