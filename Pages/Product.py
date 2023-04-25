# Raghuveer Kamble
# www.kamble.ai
# www.linkedin.com/raghuveerkamble

# =============================================================================
# KPI Tab data
# =============================================================================

import pandas as pd
import numpy as np
import dash

from dash import Dash, html, dcc, dash_table
import dash_admin_components as dac
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash.dash_table.Format import Group
import dash_pivottable
import dash_tabulator
from dash import Dash, Input, Output, dcc, html
from data.MoonStoneData import MoonStoneData, table
from dash_iconify import DashIconify

from dplython import (DplyFrame, X, diamonds, select, sift, sample_n,
                      sample_frac, head, arrange, mutate, group_by,
                      summarize, DelayFunction)

# =============================================================================
# Query Data
# =============================================================================
"""
csv_file = "data/Dec22a.csv"
csv_data = pd.read_csv(csv_file)
table = pd.DataFrame(csv_data)

MoonStoneData = DplyFrame(table)
"""

diamondsSmall = MoonStoneData >> select(X.Portfolio, X.Vertical, X.Segment, 
                                        X.Product, X.Borrower, X.Status,
                                        X.Nature_of_Business, X.Constitution, X.Disbursement_Amount,
                                        X.Disb_Amount_in_Lacs, X.Amt, X.Ticket_Size_Bucket,	
                                        X.Disbursement_Date, X.Disb_Month, X.Disb_Year,
                                        X.FY, X.POS_Dec_22, X.POS_Dec_22_in_Crs, X.Branch,	
                                        X.Branch_Risk_Colour, X.State, X.Branch_Type,
                                        X.Zone, X.Ashv_Risk_Score, X.SME_Score,	
                                        X.Loan_Tenure_Months, X.CM, X.RM, X.DP_Holder_As_per_policy,
                                        X.DEC_22_CL_BKT)


Query1 = pd.pivot_table(data=diamondsSmall,
                       index=['Vertical','Product'], columns=['Status'],
                       values=['Amt'], aggfunc=['count'], #{diamondsSmall['Status']:np.count_nonzero,'Amt':np.sum},
                       margins = True, margins_name='Total')
Query1.columns = Query1.columns.droplevel(0)
Query1.columns = Query1.columns.droplevel(0)

Query2 = pd.pivot_table(data=diamondsSmall,
                       index=['Product'], columns=['DEC_22_CL_BKT'],
                       values=['Amt'], aggfunc=['count'],  
                       margins = True, margins_name='Total')
Query2.columns = Query2.columns.droplevel(0)
Query2.columns = Query2.columns.droplevel(0)

Query3 = pd.pivot_table(data=diamondsSmall,
                       index=['Product'], #columns=['Status'],
                       values=['Amt'], aggfunc=['count'], #{diamondsSmall['Status']:np.count_nonzero,'Amt':np.sum},
                       margins = True, margins_name='Total')
Query3.columns = Query3.columns.droplevel(0)

Query4 = pd.pivot_table(data=diamondsSmall,
                       index=['Product'], columns=['Status'],
                       values=['Amt'], aggfunc=['count'], #{diamondsSmall['Status']:np.count_nonzero,'Amt':np.sum},
                       margins = True, margins_name='Total')


Query6 = round((diamondsSmall >> 
         #mutate(carat_bin=X.carat.round()) >> 
         group_by( X.Status) >>
         sift(X.Portfolio == 'New Book') >>
         summarize(count=X.Amt.count(), amt=np.sum(X.Amt)) 
         
         
         #arrange(X.Portfolio) 
         #crosstab(X.Portfolio, X.Status)   
),2)
# Query6.drop('Status')
# Query6.columns = Query3.columns.droplevel(0)
#Query6b = Query6.columns.tolist()
#Query6b = Query6.columns.values

# Query6.append(Query6.sum(numeric_only=True), ignore_index=True)
# df.loc['Column_Total']= df.sum(numeric_only=True, axis=0)
# df.loc[:,'Row_Total'] = df.sum(numeric_only=True, axis=1)
# df.reset_index(drop=True, inplace=True)
# Query6.set_index('Status')
Query6 = Query6.set_index('Status')
Query6['% Count'] = round((Query6['count']/Query6['count'].sum())*100,2)
Query6['% Amt'] = round((Query6['amt']/Query6['amt'].sum())*100,2)
Query6.loc['Total']= round(Query6.sum(numeric_only=True, axis=0),2)
# Query6.loc[:,'Row_Total']= round(Query6.sum(numeric_only=True, axis=1),2)

Query8 = table[["Portfolio", "Vertical", "Segment", "Product", "Borrower", "Status", "Amt", "POS_Dec_22_in_Crs"]]
#Total_rows = Query8.shape[0]






# =============================================================================
# Card Data
# =============================================================================


CardHeader = "Portfolio Insights"
CardTitle = "Raghuveer Kamble"
#CardTable = [1, ",", 2]
CardHeader1 = "Total Portfolio"
CardTitle1 = ""
BoxCardTitle1 = "Total Portfolio"
CardHeader2 = "ATS - Live Acs"
CardTitle2 = ""
CardHeader3 = "Book Performance : No wise"
CardTitle3 = ""
CardHeader4 = "Book Performance : Amt wise "
CardTitle4 = ""
CardHeader5 = "Vertical Performance : No wise "
CardTitle5 = ""
CardHeader6 = "Segment Performance : No wise "
CardTitle6 = ""
CardHeader7 = "Book Performance : DPD wise "
CardTitle7 = ""
CardHeader8 = "Slicer"
CardTitle8 = ""

def CardTable(df):
    CardTable = [
        dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, index=True, responsive=True, id="customers")
    ]
    return CardTable
     
def CardTableNoIndex(df):
    CardTable = [
        dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, index=False, responsive=True, id="customers")
    ]
    return CardTable

CardTable1 = CardTable(Query1)
CardTable2 = CardTable(Query2)
CardTable3 = CardTable(Query1)
CardTable4 = CardTable(Query1)
CardTable5 = CardTable(Query6)
CardTable6 = CardTableNoIndex(Query6)
CardTable7 = CardTableNoIndex(Query1)


CardTable8 = dash_pivottable.PivotTable(
            id="Query8",
            data=Query8.to_dict(orient='records'),
            cols=["Status"],
            #colOrder="key_a_to_z",
            rows=["Product"],
            #rowOrder="key_a_to_z",
            #rendererName= "Table",  #"Grouped Column Chart",
            aggregatorName="Sum as Fraction of Rows",
            #hiddenFromAggregators = False,
            #hiddenFromDragDrop = True,
            #hiddenAttributes = False,
            vals=["Amt"],
            #valueFilter={"Status": {"Live": False}}
            
)


# =============================================================================
# Tab Body
# =============================================================================

ProductVertical = "Hi" #VerticalTabData
# =============================================================================
# Tab Body
# =============================================================================

def card_content(CardHeader, CardTitle, CardTable):
    card_content = [
        dbc.CardHeader(CardHeader, style={"background-color": "#FF0000", "color": "white"}),
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



VerticalCards = html.Div(
    [
        html.Br(),
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content(CardHeader1, CardTitle1, CardTable1), color="primary", outline=True)),
                dbc.Col(dbc.Card(card_content(CardHeader2, CardTitle2, CardTable2), )),
                dbc.Col(dbc.Card(card_content(CardHeader3, CardTitle3, CardTable3), )),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content(CardHeader4, CardTitle4, CardTable4), )),
                dbc.Col(dbc.Card(card_content(CardHeader5, CardTitle5, CardTable5), )),
                dbc.Col(dbc.Card(card_content(CardHeader6, CardTitle6, CardTable6), )),
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

WholesaleVertical = VerticalCards
PartnershipVertical = VerticalCards




def create_graph():
    return "Hi"

RetailVertical = html.Div([
    html.Br(),
    dmc.Tabs(
    [
        dmc.TabsList(
            [
                dmc.Tab("Status wise", value="1", icon=DashIconify(icon="tabler:alarm-filled")),
                dmc.Tab("DPD Wise", value="2", icon=DashIconify(icon="tabler:alarm")),
                dmc.Tab("Bounce wise", value="3", icon=DashIconify(icon="tabler:alarm-minus")),
            ]
        ),
        dmc.TabsPanel(VerticalCards, value="1"),
        dmc.TabsPanel(ProductVertical, value="2"),
        dmc.TabsPanel(create_graph(), value="3"),
    ],
    value="1",
    color="red",
    variant="pills",
)
])


# Red: #FF0000, Pink : #FB79B3, light salmon: #ffa07a
Product_KPI = dac.TabItem(id='product_content_cards', 
    children=html.Div([
        dbc.Card([
        dcc.Store(id="product_store1"),
        dbc.CardHeader([
        dbc.Tabs(
            [
                dbc.Tab(ProductVertical, label="Vertical", tab_id="ProductVertical", active_label_style={"color": "#FF0000"}, activeTabClassName="fw-bold fst-italic"),
                dbc.Tab(RetailVertical, label="Retail", tab_id="RetailVertical", active_label_style={"color": "#FF0000"}, activeTabClassName="fw-bold fst-italic"),
                dbc.Tab(WholesaleVertical, label="Wholesale", tab_id="WholesaleVertical", active_label_style={"color": "#FF0000"}, activeTabClassName="fw-bold fst-italic"),
                dbc.Tab(PartnershipVertical, label="Partnership", tab_id="PartnershipVertical", active_label_style={"color": "#FF0000"}, activeTabClassName="fw-bold fst-italic"),
            ],
            id="Product_tabs1",
            active_tab="ProductVertical",  
            ),#style='color:#ffa07a',
        ]),    
    ]),
        html.Div(id="product-box-tab-content", className="p-4"),
    ])
    )

