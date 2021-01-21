import dash_html_components as html


def get_about_div():
    """
    Returns the about div

    :return: About Div
    """

    return html.Div(id='about-div', children=[
        html.H2(children='About'),
        html.P('This application serves as a interface between Jutrack Service and researchers or study leaders. '
               'It provides different methods like creating new studies or displaying currently available information to studies.'),
        html.P(children=['Responsible: ', html.A('Michael Stolz', href='https://www.fz-juelich.de/inm/inm-7/EN/UeberUns/Mitarbeiter/mitarbeiter_node.html?cms_notFirst=true&cms_docId=2552232')]),
        html.P(children=['Mail to: ', html.A('m.stolz@fz-juelich.de', href='mailto:m.stolz@fz-juelich.de')])])

