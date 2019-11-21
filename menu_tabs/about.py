import dash_core_components as dcc
import dash_html_components as html


def get_about_div():
    return html.Div(id='about1-div', children=html.P(id='about1-p', children=[
        html.Span('Michael Stolz'),
        html.Br(),
        html.Span('m.stolz@fz-juelich.de')])
    )
