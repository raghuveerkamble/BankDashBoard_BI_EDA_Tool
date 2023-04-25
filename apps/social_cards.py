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
from dash import Input, Output, dcc, html
from dplython import (DplyFrame, X, diamonds, select, sift, sample_n,
                      sample_frac, head, arrange, mutate, group_by,
                      summarize, DelayFunction)
from data.MoonStoneData import MoonStoneData, table

# =============================================================================
# Data
# =============================================================================
"""
csv_file = "data/Dec22.csv"
csv_data = pd.read_csv(csv_file)
table = pd.DataFrame(csv_data)
"""

Query1 = table[["Portfolio", "Vertical", "Segment", "Product", "Borrower", "Status", "Amt", "POS_Dec_22_in_Crs"]]
Total_rows = Query1.shape[0]

Query3 = Query1.apply(lambda x : True
                      if x['Status'] == "Live" else False, axis = 1)

# Count number of True in the series
Live_rows = len(Query3[Query3 == True].index)
NewPortfolio_rows = Total_rows - Live_rows
Portfolio_Sum_rows = np.sum(Query1['Amt'] > 0)

Total_Portfolio = Query1.loc[Query1['Amt'] > 0, 'Amt'].sum()
AUM = Query1.loc[(Query1['Status'] == 'Live') & (Query1['Amt'] > 0), 'Amt'].sum()
POS = Query1.loc[(Query1['Status'] == 'Live') & (Query1['Amt'] > 0), 'POS_Dec_22_in_Crs'].sum()

ATSRetailS = Query1.loc[(Query1['Status'] == 'Live') & (Query1['Vertical'] == 'Retail'), 'Amt'].sum()
ATSRetailC = Query1.loc[(Query1['Status'] == 'Live') & (Query1['Vertical'] == 'Retail'), 'Amt'].count()
ATSRetail = round((ATSRetailS / ATSRetailC)*100, 2)
ATSWholeS = Query1.loc[(Query1['Status'] == 'Live') & (Query1['Vertical'] == 'Wholesale'), 'Amt'].sum()
ATSWholeC = Query1.loc[(Query1['Status'] == 'Live') & (Query1['Vertical'] == 'Wholesale'), 'Amt'].count()
ATSWhole = round((ATSWholeS / ATSWholeC)*100, 2)
ATSPartS = Query1.loc[(Query1['Status'] == 'Live') & (Query1['Vertical'] == 'Partnership'), 'Amt'].sum()
ATSPartC = Query1.loc[(Query1['Status'] == 'Live') & (Query1['Vertical'] == 'Partnership'), 'Amt'].count()
ATSPart = round((ATSPartS / ATSPartC)*100, 2)
Total_Portfolio = float (str (Total_Portfolio)[:-2])
AUM = float (str (AUM)[:-2])
POS = float (str (POS)[:-2])
ATSC  = ATSRetailC + ATSWholeC + ATSPartC
ATSS  = ATSRetailS + ATSWholeS + ATSPartS

ATSTotal = round((Total_Portfolio / Total_rows)*100,2)
ATSLive = round((AUM / Live_rows)*100,2)
WOS =  Query1.loc[Query1['Status'] == 'Write-off', 'Amt'].sum()
WOC =  Query1.loc[Query1['Status'] == 'Write-off', 'Amt'].count()

diamonds = DplyFrame(table)
diamondsSmall = diamonds >> select(X.Portfolio, X.Vertical, X.Segment, X.Status, X.Amt, X.Branch, X.DEC_22_CL_BKT)
#df >> sift((X.carat > 4) | (X.cut == "Ideal")) >> head(2)
#(diamonds >> 
#        mutate(carat_bin=X.carat.round()) >> 
#        group_by(X.cut, X.carat_bin) >> 
#        summarize(avg_price=X.price.mean()))

Query4 = pd.pivot_table(data=diamondsSmall,
                       index=['Portfolio'], columns=['Status'],
                       values=['Amt'], aggfunc= ['count', 'sum'],
                       margins = True, margins_name='Total')

#Query5 = diamondsSmall >>
            



# =============================================================================
# Body
# =============================================================================

social_cards_tab = dac.TabItem(id='content_social_cards',
    children=html.Div([
       dbc.Container([
        dcc.Store(id="store"),
        html.H1("Portfolio Insights..."),
        html.Hr(),
        dbc.Button(
            "Regenerate graphs",
            color="primary",
            id="button",
            className="mb-3",
        ),
        dbc.Tabs(
            [
                dbc.Tab(label="KPI", tab_id="kpi"),
                dbc.Tab(label="Scatter", tab_id="scatter"),
                dbc.Tab(label="Histograms", tab_id="histogram"),
            ],
            id="tabs",
            active_tab="kpi",
        ),
        html.Div(id="tab-content", className="p-4"),
    ])
]))









#---------------------


CardHeader = "Portfolio Insights"
CardTitle = "Raghuveer Kamble"
CardTable = [WOC, ",", WOS]
CardHeader1 = "Total Portfolio"
CardTitle1 = ""
CardHeader2 = "ATS - Live Acs"
CardTitle2 = ""
CardHeader3 = "Testing"
CardTitle3 = "Test"




KPI_Disb = pd.DataFrame(
    {
        ("Portfolio", "No."): {
            "Total Disbursed": Total_rows,
            "Live Acs ": Live_rows,
        },
        ("Portfolio", "Amt in Crs"): {
            "Total Disbursed": Total_Portfolio,
            "Live Acs ": AUM,
            "POS": POS,
        },
    }
)
KPI_Disb.index.set_names("KPI", inplace=True)
CardTable1 = dbc.Table.from_dataframe(
    KPI_Disb, striped=False, bordered=True, hover=True, index=True, responsive=True
)


KPI_Portfolio = pd.DataFrame(
    {
        ("Portfolio", "No."): {
            "Retail": ATSRetailC,
            "Wholesale": ATSWholeC,
            "Partnership": ATSPartC,
            "Total Live": ATSC,
        },
        ("Portfolio", "No. %"): {
            "Retail": round((ATSRetailC/ATSC)*100, 2),
            "Wholesale": round((ATSWholeC/ATSC)*100, 2),
            "Partnership": round((ATSPartC/ATSC)*100, 2),
            "Total Live": round((ATSC/ATSC)*100, 2)
        },
        ("Portfolio", "Amt"): {
            "Retail": round(ATSRetailS, 2),
            "Wholesale": round(ATSWholeS, 2),
            "Partnership": round(ATSPartS, 2),
            "Total Live": round(ATSS, 2)
        },
        ("Portfolio", "Amt %"): {
            "Retail": round((ATSRetailS/ATSS)*100, 2),
            "Wholesale": round((ATSWholeS/ATSS)*100, 2),
            "Partnership": round((ATSPartS/ATSS)*100, 2),
            "Total Live": round((ATSS/ATSS)*100, 2)
        },
        ("Portfolio", "ATS"): {
            "Retail": ATSRetail,
            "Wholesale": ATSWhole,
            "Partnership": ATSPart,
            "Total Live": round(ATSTotal, 2)
        },
    }
)
KPI_Portfolio.index.set_names("ATS", inplace=True)
CardTable2 = dbc.Table.from_dataframe(
    KPI_Portfolio, striped=False, bordered=True, hover=True, index=True, responsive=True
)

CardTable3 = dbc.Table.from_dataframe(
    Query4, striped=False, bordered=True, hover=True, index=True, responsive=True
)

CardTable4 = dash_pivottable.PivotTable(
            id="Query1",
            data=Query1.to_dict(orient='records'),
            #cols=["Status"],
            #colOrder="key_a_to_z",
            rows=["Portfolio"],
            #rowOrder="key_a_to_z",
            #rendererName= "Table",  #"Grouped Column Chart",
            #aggregatorName="Sum",
            #hiddenFromAggregators = False,
            #hiddenFromDragDrop = True,
            #hiddenAttributes = False,
            vals=["Amt"],
            #valueFilter={"Status": {"Live": False}}
            
            )
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

cards = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content(CardHeader1, CardTitle1, CardTable1), color="primary", inverse=True)),
                dbc.Col(
                    dbc.Card(card_content(CardHeader2, CardTitle2, CardTable2), color="secondary", inverse=True)
                ),
                dbc.Col(dbc.Card(card_content(CardHeader3, CardTitle, CardTable3), color="info", inverse=True)),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content(CardHeader, CardTitle, CardTable4), color="success", inverse=True)),
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




