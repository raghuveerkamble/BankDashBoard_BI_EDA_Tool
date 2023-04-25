# -*- coding: utf-8 -*-
# =============================================================================
# Raghuveer Kamble
# =============================================================================

# =============================================================================
# Cards Tab
# =============================================================================

import time
import pandas as pd
import numpy as np
import dash
import dash_bootstrap_components as dbc
import dash_admin_components as dac
import dash_pivottable
import plotly.graph_objs as go
from dash import Dash, Input, Output, dcc, html
from dplython import (DplyFrame, X, diamonds, select, sift, sample_n,
                      sample_frac, head, arrange, mutate, group_by,
                      summarize, DelayFunction)
import dash
from dash.dependencies import Input, Output

from dash import dash_table

from Pages.NOB import tab1_NOB_content
from Pages.KPI import KPI
from Pages.Portfolio import Portfolio_KPI
from Pages.Product import Product_KPI
from data.MoonStoneData import MoonStoneData, table 

import matplotlib.pyplot as plt
plt.style.use('ggplot')



# =============================================================================
# Body
# =============================================================================
cards_tab = dac.TabItem(id='content_cards', 
    children=html.Div([
        dbc.Card([
        dcc.Store(id="store1"),
        dbc.CardHeader(
        dbc.Tabs(
            [
                dbc.Tab(KPI, label="KPI", tab_id="Veer_KPI", active_label_style={"color": "#FF0000"}, activeTabClassName="fw-bold fst-italic"),
                dbc.Tab(Portfolio_KPI, label="Portfolio", tab_id="Portfolio_KPI", active_label_style={"color": "#FF0000"}, activeTabClassName="fw-bold fst-italic"),
                dbc.Tab(Product_KPI, label="Product", tab_id="Product_KPI", active_label_style={"color": "#FF0000"}, activeTabClassName="fw-bold fst-italic"),
            ],
            id="tabs1",
            active_tab="Veer_KPI",  
            ),
        ),    
    ]),
        html.Div(id="box-tab-content", className="p-4"),
    ])
    )

