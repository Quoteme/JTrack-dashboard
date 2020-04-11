import dash_html_components as html

from menu_tabs import create_menu


def page_not_found():
	return html.Div(children=[html.H1("404 Error"), html.H3("Page not found")])


def general_page():
	return [html.Div(id='menu', className='column-small jutrack-background', style={'margin': '6px'},
					 children=[html.H2(id='menu-title', style={'color': 'white', 'margin': '6px'}, children='Menu'),
							   create_menu()]),
			html.Div(id='page-content', style={'margin': '12px'}, className='column-big row')]


def login_page():
	return [html.Div(id='login', className='center', children=[html.H3("Username:"), html.H3("Password:")])]
