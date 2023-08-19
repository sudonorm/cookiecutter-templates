import dash
from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

import dash
from dash import dcc, html, no_update

import json
import os
import shutil
from pathlib import Path
import builtins

import sys
home_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(home_dir)
from utils import folderPaths

LINUX_MNT = folderPaths.LINUX_MNT
USER_DRIVE = folderPaths.USER_DRIVE
USER = folderPaths.USER

NETWORK_ROOT_FOLDER = folderPaths.NETWORK_ROOT_FOLDER
WIN_FOLDER =  folderPaths.WIN_FOLDER
ROOT_FOLDER = folderPaths.ROOT_FOLDER
SLSH = folderPaths.SLSH
BKSLH = folderPaths.BKSLH 

BASEPATH_NETWORK = folderPaths.BASEPATH_NETWORK

BASEPATH_USER = folderPaths.BASEPATH_USER

BASEPATH = BASEPATH_NETWORK


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# layout
layout = html.Div([
    html.Div(children='My First App with Data and a Graph'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure=px.histogram(df, x='continent', y='lifeExp', histfunc='avg'))
])

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
