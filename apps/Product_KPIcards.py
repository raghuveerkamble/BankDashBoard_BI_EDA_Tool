# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:41:36 2022

@author: raghu
"""

import dash
from dash.dependencies import Input, Output
import dash_pivottable
import dash_admin_components as dac
from dash import Dash, html, dcc
#from example_plots import plot_scatter
import pandas as pd
import numpy as np

from data.MoonStoneData import MoonStoneData, table 

# =============================================================================
# Data
# =============================================================================


kpi_product_boxes_tab = dac.TabItem(id='content_kpi_product_boxes',
    children=html.Div([
     dash_pivottable.PivotTable(
         id="table",
         data=table.to_dict(orient='records'),
         cols=["Status"],
         colOrder="key_a_to_z",
         rows=["Portfolio", "Vertical"],
         rowOrder="key_a_to_z",
         rendererName="Grouped Column Chart",
         aggregatorName="Average",
         vals=["Disb_Amount_in_Lacs"],
         valueFilter={"Status": {"Live": False}},
     ),
     ], 
        className='row'
    ),
    )