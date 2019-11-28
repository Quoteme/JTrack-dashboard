import dash_core_components as dcc
import dash_html_components as html


def get_about_div():
    return html.Div(id='about1-div', children=html.P(id='about1-p', children=[
        html.A('Michael Stolz', href='https://www.fz-juelich.de/inm/inm-7/EN/UeberUns/Mitarbeiter/mitarbeiter_node.html?cms_notFirst=true&cms_docId=2552232'),
        html.Br(),
        html.A('m.stolz@fz-juelich.de', href='mailto:m.stolz@fz-juelich.de')
    ]))
