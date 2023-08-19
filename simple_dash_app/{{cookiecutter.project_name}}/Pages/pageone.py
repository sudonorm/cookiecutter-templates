import os
import time
import logging
import sys
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback, State, dash_table, no_update
import dash

try:
    from glob import glob
except Exception as e:
    from glob2 import glob

home_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(home_dir)
import utils
from utils import folderPaths


layout = html.Div([
            html.Div(children=[
                dcc.ConfirmDialog(
                        id='confirm-danger',
                        message='some message.',
                    ),

                dbc.Row([

                    dbc.Col(
                            [
                                dbc.Card([
                                    html.Label('Hello world'),
                                    
                                 ],  style={"marginBottom": 30, 'padding': 20}),
                            ], 
                            xs=12, sm=12, md=12, lg=6, xl=6, class_name="d-grid"),

                    dbc.Col(
                            [
                                dbc.Card([
                                    html.Label('Still here'),
                                    
                                 ],  style={"marginBottom": 30, 'padding': 20}),
                            ], 
                            xs=12, sm=12, md=12, lg=6, xl=6, class_name="d-grid"),

            ],  style={"margin": 30}, justify='center'),
], style={'padding': 20, 'flex': 1}),
    ]
)

## ************************  callback example *****************************
# @callback(
#     Output("some-id", "options"), 
#     [Input("some-other-id", "value")],
#     prevent_initial_call=True,
# )
# def some_function(id):

#     trigger_id = dash.ctx.triggered_id if not None else 'No clicks yet'
#     if trigger_id == "some-other-id":
#         print("some logic here")    

#         return [{'label':x, 'value':x} for x in ["tmp"]]

#     return [{'label':x, 'value':x} for x in ["tmp"]]