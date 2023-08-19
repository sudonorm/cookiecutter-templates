import dash
from dash import Dash, html
import dash_bootstrap_components as dbc
import os
from sys import platform as pltfrm_type
import sys
home_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(home_dir)
from Pages import index, pageone

PROD = True
DEBUG_MODE = False ### this should only be set to true when developing and not in production

if pltfrm_type in ['win32', 'cygwin']:
    PROD = False
    DEBUG_MODE = True

app = Dash(__name__, use_pages=True, pages_folder="", external_stylesheets=[dbc.themes.FLATLY],
            meta_tags=[{'name': 'viewport',
                                        'content': 'width=device-width, initial-scale=1.0'}], url_base_pathname="/{{ cookiecutter.url_endpoint_of_app }}/")

dash.register_page("index", path='/', layout=index.layout, name='Home')
dash.register_page("pageone", layout=pageone.layout, name='Page One')

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/{{ cookiecutter.url_endpoint_of_app }}")),
        dbc.NavItem(dbc.NavLink("Page One", href="/{{ cookiecutter.url_endpoint_of_app }}/pageone")),
        
    ],
    #brand="NavbarSimple",
    #brand_href="#",
    links_left=True,
    color="primary",
    dark=True,
)

app.layout = html.Div([

    dbc.Row([
       dbc.Col([
           navbar
       ])
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Container(dash.page_container, fluid=True),
        ])
    ])
])

if not PROD:
    if __name__ == "__main__":
        app.run(debug=DEBUG_MODE, port= {{ cookiecutter.app_port }})
