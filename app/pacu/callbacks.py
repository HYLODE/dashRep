"""
Functions (callbacks) that provide the functionality
"""
import json

import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from config.config import ConfigFactory, footer, header, nav
from dash import Dash, Input, Output, State
from dash import dash_table as dt
from dash import dcc, html

from app import app
from utils import utils

conf = ConfigFactory.factory()


