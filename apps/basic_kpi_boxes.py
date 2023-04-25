# -*- coding: utf-8 -*-
# =============================================================================
# Raghuveer Kamble
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
# Demographic Tabs
# =============================================================================


Demographic_Tabs = html.Div([
    html.Hr(),
    dbc.Card(
    [
        #html.Hr(),
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(tab1_NOB_content, label="NOB", active_label_style={"color": "#FB79B3"}, activeTabClassName="fw-bold fst-italic"),
                    dbc.Tab(tab1_NOB_content, label="Constitution", active_label_style={"color": "#FB79B3"}, activeTabClassName="fw-bold fst-italic"),
                    dbc.Tab("This tab's content is never seen", label="Tab 3", disabled=True),
                ],
                id="card-tabs",
                active_tab="tab-1",
            )
        ),
        dbc.CardBody(html.P(id="card-content", className="card-text")),
    ]
    )   
])

# =============================================================================
# Body
# =============================================================================

kpi_basic_boxes_tab = dac.TabItem(id='content_kpi_basic_boxes', 
    children=html.Div([
       #dbc.Container([
        dbc.Card([
        dcc.Store(id="store1"),
        #html.H1("Product Insights..."),
        #html.Hr(),
        dbc.CardHeader(
        dbc.Tabs(
            [
                dbc.Tab(KPI, label="KPI", tab_id="Veer_KPI", active_label_style={"color": "#FB79B3"}, activeTabClassName="fw-bold fst-italic"),
                dbc.Tab(Portfolio_KPI, label="Portfolio", tab_id="Portfolio_KPI1", active_label_style={"color": "#FB79B3"}, activeTabClassName="fw-bold fst-italic"),
                dbc.Tab(Demographic_Tabs, label="Demographic", tab_id="Demographic_KPI2", active_label_style={"color": "#FB79B3"}, activeTabClassName="fw-bold fst-italic"),
                dbc.Tab(KPI, label="Bureau", tab_id="Bureau_KPI3", active_label_style={"color": "#FB79B3"}, activeTabClassName="fw-bold fst-italic"),
                dbc.Tab(KPI, label="Banking", tab_id="Banking_KPI4", active_label_style={"color": "#FB79B3"}, activeTabClassName="fw-bold fst-italic"),
            ],
            id="tabs1",
            active_tab="Veer_KPI",  
            ),
        ),    
        #html.Hr(),
            
    ]),
        html.Div(id="box-tab-content", className="p-4"),
        #html.Hr(),
    ])
    )

