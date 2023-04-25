
# =============================================================================
# KPI Tab data
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
#from dash_table import DataTable
from dash import dash_table

from data.MoonStoneData import MoonStoneData, table

# =============================================================================
# Data
# =============================================================================

Query1 = table[["Portfolio", "Vertical", "Segment", "Product", "Borrower", "Status", "Amt", "POS_Dec_22_in_Crs"]]
Total_rows = Query1.shape[0]

Query3 = Query1.apply(lambda x : True
                      if x['Status'] == "Live" else False, axis = 1)
"""
diamondsSmall = (MoonStoneData >> 
                select(X.Portfolio, X.Vertical, X.Segment, X.Status, X.Amt, X.Branch, X.DEC_22_CL_BKT, X.Nature_of_Business, X.Constitution) >>
                sift(X.DEC_22_CL_BKT != 'closed', X.Vertical == 'Retail', X.Nature_of_Business != '')
)
"""
diamondsSmall = (MoonStoneData >> 
                select(X.Portfolio, X.Vertical, X.Segment, X.Status, X.Amt, 
                       X.Branch, X.DEC_22_CL_BKT, X.Nature_of_Business, X.Constitution, 
                       X.Disb_Year, X.Ticket_Size_Bucket ) #>>
                #sift( X.Vertical == 'Retail', X.Nature_of_Business != '')
)

Query2 = pd.pivot_table(data=diamondsSmall, values=['Status'],
                       index=['Disb_Year'], columns=['Vertical'], 
                       aggfunc=len, margins=True, 
                       dropna=True, fill_value=0)
Query2.columns = Query2.columns.droplevel(0) 

Query4 = pd.pivot_table(data=diamondsSmall, values=['Vertical'],
                       index=['Disb_Year'], columns=['Status'], 
                       aggfunc=len, margins=True, 
                       dropna=True, fill_value=0)
Query4.columns = Query4.columns.droplevel(0) 

Query5 = pd.pivot_table(data=diamondsSmall, values=['Status'],
                       index=['Disb_Year'], columns=['DEC_22_CL_BKT'], 
                       aggfunc=len, margins=True, 
                       dropna=False, fill_value=0)
Query5.columns = Query5.columns.droplevel(0) 


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


CardTable1 = dbc.Table.from_dataframe(
    Query2, striped=False, bordered=True, hover=True, index=True, responsive=True
)

CardTable2 = dbc.Table.from_dataframe(
    Query4, striped=False, bordered=True, hover=True, index=True, responsive=True
)

CardTable3 = dbc.Table.from_dataframe(
    Query5, striped=False, bordered=True, hover=True, index=True, responsive=True
)
# =============================================================================
# Card Body
# =============================================================================
CardHeader1 = "Portfolio - Yearwise"
CardTitle1 = ""
CardHeader2 = "Status - Yearwise"
CardTitle2 = ""
CardHeader3 = "Constitution vs Status"
CardTitle3 = ""

def card_content(CardHeader, CardTitle, CardTable):
    card_content = [
        dbc.CardHeader(CardHeader),
        dbc.CardBody(
            [
            html.H5(CardTitle, className="card-title"),
            html.P(CardTable,
                #"This is some card content that we'll reuse",
                className="card-text",),
            ]
            ),
        ]
    return card_content

# =============================================================================
# Tab Body
# =============================================================================

KPI = html.Div([
  html.Hr(),
# html.H4('Basic KPI'),
    html.Div([
      dac.ValueBox(
        	value= "Total Disbursed : {}".format(Total_rows),
            subtitle="Live Accounts : {}".format(Live_rows),
            color = "primary",
            icon = "shopping-cart",
            #href = "#"
        ),
        dac.ValueBox(
          elevation = 4,
          subtitle =  "Total Portfolio : {} Cr".format(Total_Portfolio),    #"POS : {} Cr".format(POS),
          value = "AUM : {} Cr".format(AUM),
          color = "success",
          icon = "cogs"
        ),
        dac.ValueBox(
          value = "POS : ", #ATS in Lacs: Retail :{} ".format(ATSRetail),  #[ATSRetail ",", ATSWhole, ",", ATSPart],
          subtitle = "{} ".format(POS),  #"ATS in Lacs, Wholesale: {}, Partnership: {}".format(ATSWhole, ATSPart),
          color = "warning",
          icon = "suitcase"
        ),
        dac.ValueBox(
          value = "Write off No :{} ".format(WOC), 
          subtitle = "Write off Amt in Crs : {}".format(round(WOS,2)),
          color = "danger",
          icon = "database"
        )
    ], className='row'),
  html.Hr(),
# html.H4('Basic Info'),
    html.Div([
      dac.InfoBox(
        title = "ATS in Lacs, Retail : ",
        value = "{} ".format(ATSRetail), 
        icon = "envelope"
        ),
      dac.InfoBox(
        title = "ATS in Lacs, Wholesale : ",
        color = "info",
        value = "{}".format(ATSPart),
        icon = "bookmark"
        ),
      dac.InfoBox(
        title = "ATS in Lacs, Partnership : ",
        gradient_color = "danger",
        value = " {} ".format(ATSWhole), 
        icon = "comments"
        )
    ], className='row'),
  html.Hr(),
# html.H4('Basic KPI'),
    html.Div([
      dbc.Row(
            [
                dbc.Col(dbc.Card(card_content(CardHeader1, CardTitle1, CardTable1), color="primary", inverse=True)),
                dbc.Col(dbc.Card(card_content(CardHeader2, CardTitle2, CardTable2), color="secondary", inverse=True)),
                dbc.Col(dbc.Card(card_content(CardHeader3, CardTitle3, CardTable3), color="info", inverse=True)),
            ],
            className="mb-4",
      ),
    ])  
])

