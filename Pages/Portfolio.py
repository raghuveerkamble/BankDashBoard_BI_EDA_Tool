

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
import dash_pivottable
from data.MoonStoneData import MoonStoneData, table

# =============================================================================
# Data
# =============================================================================

Query1 = table[["Portfolio", "Vertical", "Segment", "Product", "Borrower", "Status", "Amt", "POS_Dec_22_in_Crs"]]
Total_rows = Query1.shape[0]

Query3 = Query1.apply(lambda x : True
                      if x['Status'] == "Live" else False, axis = 1)

diamondsSmall = MoonStoneData >> select(X.Portfolio, X.Vertical, X.Segment, X.Status, X.Amt, X.Branch, X.DEC_22_CL_BKT)

Query4 = pd.pivot_table(data=diamondsSmall,
                       index=['Portfolio'], columns=['Status'],
                       values=['Amt'], aggfunc=['count'], #{diamondsSmall['Status']:np.count_nonzero,'Amt':np.sum},
                       margins = True, margins_name='Total')
Query4.columns = Query4.columns.droplevel(0)
Query4.columns = Query4.columns.droplevel(0)

Query5 = np.round(pd.pivot_table(data=diamondsSmall,
                       index=['Portfolio'], columns=['Status'],
                       values=['Amt'], aggfunc=np.sum, #aggfunc=['sum'], 
                       margins = True, margins_name='Total'),2)
Query5.columns = Query5.columns.droplevel(0)
#Query5.columns = Query5.columns.droplevel(0)   

Query6 = (pd.pivot_table(data=diamondsSmall,
                       index=['Vertical'], columns=['Status'],
                       values=['Amt'], aggfunc=['count'], 
                       margins = True, margins_name='Total') #.reset_index() , as_index=False
         )
Query6.columns = Query6.columns.droplevel(0)
Query6.columns = Query6.columns.droplevel(0)   

Query7 = (pd.pivot_table(data=diamondsSmall,
                       index=['Segment'], columns=['Status'],
                       values=['Amt'], aggfunc=['count'], 
                       margins = True, margins_name='Total') #.reset_index() #, as_index=False
         )
Query7.columns = Query7.columns.droplevel(0)
Query7.columns = Query7.columns.droplevel(0)  

Query8 = (pd.pivot_table(data=diamondsSmall,
                       index=['Portfolio'], columns=['DEC_22_CL_BKT'],
                       values=['Amt'], aggfunc=['count'], 
                       margins = True, margins_name='Total') #.reset_index() #, as_index=False
         )
Query8.columns = Query8.columns.droplevel(0)
Query8.columns = Query8.columns.droplevel(0) 


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


# =============================================================================
# Card Data
# =============================================================================


CardHeader = "Portfolio Insights"
CardTitle = " "
CardTable = [WOC, ",", WOS]
CardHeader1 = "Total Portfolio"
CardTitle1 = ""
CardHeader2 = "ATS - Live Acs"
CardTitle2 = ""
CardHeader3 = "Book Performance : No wise"
CardTitle3 = ""
CardHeader4 = "Book Performance : Amt in Cr wise "
CardTitle4 = ""
CardHeader5 = "Vertical Performance : No wise "
CardTitle5 = ""
CardHeader6 = "Segment Performance : No wise "
CardTitle6 = ""
CardHeader7 = "Book Performance : DPD wise "
CardTitle7 = ""
CardHeader8 = "Slicer"
CardTitle8 = ""


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

CardTable4 = dbc.Table.from_dataframe(
    Query5, striped=False, bordered=True, hover=True, index=True, responsive=True
)

CardTable5 = dbc.Table.from_dataframe(
    Query6, striped=False, bordered=True, hover=True, index=True, responsive=True
)

CardTable6 = dbc.Table.from_dataframe(
    Query7, striped=False, bordered=True, hover=True, index=True, responsive=True
)

CardTable7 = dbc.Table.from_dataframe(
    Query8, striped=False, bordered=True, hover=True, index=True, responsive=True
)

CardTable8 = dash_pivottable.PivotTable(
            id="Query1",
            data=Query1.to_dict(orient='records'),
            cols=["Status"],
            #colOrder="key_a_to_z",
            rows=["Portfolio"],
            #rowOrder="key_a_to_z",
            #rendererName= "Table",  #"Grouped Column Chart",
            aggregatorName="Sum as Fraction of Rows",
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
                #"This is some card content that we'll reuse",
                className="card-text",),
            ]
            ),
        ]
    return card_content

# =============================================================================
# Tab Body
# =============================================================================


Portfolio_KPI = html.Div(
    [
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content(CardHeader1, CardTitle1, CardTable1), color="primary", inverse=True)),
                dbc.Col(dbc.Card(card_content(CardHeader2, CardTitle2, CardTable2), color="secondary", inverse=True)),
                dbc.Col(dbc.Card(card_content(CardHeader3, CardTitle3, CardTable3), color="info", inverse=True)),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content(CardHeader4, CardTitle4, CardTable4), color="success", inverse=True)),
                dbc.Col(dbc.Card(card_content(CardHeader5, CardTitle5, CardTable5), color="warning", inverse=True)),
                dbc.Col(dbc.Card(card_content(CardHeader6, CardTitle6, CardTable6), color="danger", inverse=True)),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content(CardHeader7, CardTitle7, CardTable7), color="light")),
                dbc.Col(dbc.Card(card_content(CardHeader8, CardTitle8, CardTable8), color="dark", inverse=True)),
            ]
        ),
    ]
)
