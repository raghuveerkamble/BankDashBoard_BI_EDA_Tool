# =============================================================================
# Nature of Business
# =============================================================================

import pandas as pd
import numpy as np
from dplython import (DplyFrame, X, diamonds, select, sift, sample_n,
                      sample_frac, head, arrange, mutate, group_by,
                      summarize, DelayFunction)

import dash_admin_components as dac
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Group
from dash import Dash, html, dcc, dash_table
from dash import dash_table

from data.MoonStoneData import MoonStoneData
# =============================================================================
# Data
# =============================================================================


diamondsSmall = (MoonStoneData >> 
                select(X.Portfolio, X.Vertical, X.Segment, X.Status, X.Amt, X.Branch, X.DEC_22_CL_BKT, X.Nature_of_Business, X.Constitution) >>
                sift(X.DEC_22_CL_BKT != 'closed', X.Vertical == 'Retail', X.Nature_of_Business != '')
)

table1 = pd.pivot_table(data=diamondsSmall, values=['Amt'],
                       index=['Nature_of_Business'], columns=['DEC_22_CL_BKT'], 
                       aggfunc=len, margins=True, 
                       dropna=True, fill_value=0)


table2 = round (table1.div( table1.iloc[:,-1], axis=0 ) * 100, 2)
table3 = table1
table2.columns = table2.columns.droplevel(0)
table4 = table2
df = table2

df['Rating'] = df['Current'].apply(lambda x:
    '⭐⭐⭐' if x > 30 else (
    '⭐⭐' if x > 20 else (
    '⭐' if x > 10 else ''
)))
df['Growth'] = df['Par 90'].apply(lambda x: '↗️' if x > 0 else '↘️')
df['Status'] = df['Par 90'].apply(lambda x: '🔥' if x > 0 else '🚒')
table5 = df

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

def make_dash_table(df):
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table



CardHeader = "Portfolio Insights"
CardTitle = "Raghuveer Kamble"
CardTable = make_dash_table(table1)
CardTable1 = make_dash_table(table1)
CardTable2 = table2
CardTable3 = table3
CardTable4 = table4
CardTable5 = table5




CardHeader1 = "Total Portfolio"
CardTitle1 = ""
CardHeader2 = "ATS - Live Acs"
CardTitle2 = ""
CardHeader3 = "Testing"
CardTitle3 = "Test"

def card_content(CardHeader, CardTitle, CardTable):
    card_content = [
        dbc.CardHeader(CardHeader),
        dbc.CardBody(
            [
            html.H5(CardTitle, className="card-title"),
            html.P(CardTable,
                "This is some card content that we'll reuse",
                className="card-text",),
            ]
            ),
        ]
    return card_content

tab1_NOB_content = html.Div(
    [
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content(CardHeader1, CardTitle1, CardTable1), color="primary", inverse=True)),
                dbc.Col(
                    dbc.Card(card_content(CardHeader2, CardTitle2, CardTable1), color="secondary", inverse=True)
                ),
                dbc.Col(dbc.Card(card_content(CardHeader3, CardTitle, CardTable1), color="info", inverse=True)),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content(CardHeader, CardTitle, CardTable1), color="success", inverse=True)),
                dbc.Col(dbc.Card(card_content(CardHeader, CardTitle, CardTable), color="warning", inverse=True)),
                dbc.Col(dbc.Card(card_content(CardHeader, CardTitle, CardTable), color="danger", inverse=True)),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content(CardHeader, CardTitle, CardTable), color="light")),
                dbc.Col(dbc.Card(card_content(CardHeader, CardTitle, CardTable), color="dark", inverse=True)),
            ]
        ),
    ]
)

