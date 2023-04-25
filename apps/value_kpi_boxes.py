# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 14:09:57 2022

@author: raghu
"""
import dash
import dash_admin_components as dac
from dash import Dash, html, dcc
from dplython import (DplyFrame, X, diamonds, select, sift, sample_n,
                      sample_frac, head, arrange, mutate, group_by,
                      summarize, DelayFunction)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dash import dash_table

plt.style.use('ggplot')

from data.MoonStoneData import MoonStoneData, table 

# =============================================================================
# Data
# =============================================================================


"""	

diamondsSmall = MoonStoneData >> select(X.Book, X.Product_Type, 
                                   X.Status_CC_MIS, X.Status, X.Disb_Amount_in_Lacs, 
                                   X.Branch  )
table = pd.pivot_table(data=diamondsSmall,
            index=['Book', 'Product_Type'], columns=['Status_CC_MIS'], 
            values=['Disb_Amount_in_Lacs'], aggfunc= ['count', 'sum'],
            margins = True, margins_name='Total')
 #   return dict(data=[table]) 
WIN = pd.pivot_table(data=diamondsSmall,
            index=['Book', 'Product_Type'], columns=['Status_CC_MIS'], 
            values=['Disb_Amount_in_Lacs'], aggfunc= ['count', 'sum'],
            margins = True, margins_name='Total')

gfg_csv_data = table.to_csv('GfG.csv', index = False)
# print('\nCSV String:\n', gfg_csv_data)

df = pd.read_csv(
   'https://gist.githubusercontent.com/chriddyp/'
   'c78bf172206ce24f77d6363a2d754b59/raw/'
   'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
   'usa-agricultural-exports-2011.csv')

def generate_table(dataframe, max_rows=20):
   return html.Table(
      # Header
      [html.Tr([html.Th(col) for col in dataframe.columns])] +
      # Body
      [html.Tr([
         html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
      ]) for i in range(min(len(dataframe), max_rows))]
   )
"""


kpi_value_boxes_tab = dac.TabItem(id='content_kpi_value_boxes',
    children=[
        
        html.Div([
            dcc.Tabs(id="tabs-styled-with-props", value='tab-1', children=[
                dcc.Tab(label='Mirror Board', value='tab-1'),
                dcc.Tab(label='Portfolio Overview', value='tab-2'),
                dcc.Tab(label='Product Overview', value='tab-3'),
                dcc.Tab(label='KPI Overview', value='tab-4'),
            ], colors={
                "border": "white",
                "primary": "gold",
                "background": "cornsilk"
            }),
            html.Div(id='tabs-content-props')
        ]),
    ]
)

"""
def sub_tab_table():
    return html.H4(children='Portfolio Analysis'), html.Div([
                generate_table(table),
                dash_table.DataTable(
                    data=df.to_dict("records"),
                    columns=[{"name": x, "id": x} for x in df],
                    style_as_list_view=True,
                    editable=False,
                    style_table={
                        "overflowY": "scroll",
                        "width": "100%",
                        "minWidth": "100%",
                    },
                    style_header={"backgroundColor": "#f8f5f0", "fontWeight": "bold"},
                    style_cell={"textAlign": "center", "padding": "8px"},
                ),
            ], className='row')

"""