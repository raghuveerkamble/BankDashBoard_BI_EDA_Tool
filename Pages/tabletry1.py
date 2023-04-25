
# =============================================================================
# KPI Tab data
# =============================================================================


import pandas as pd
import numpy as np
import dash
import dash_tabulator
import plotly_express as px
import dash_admin_components as dac
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash.dash_table.Format import Group
import dash_pivottable
from dash import Dash, Input, Output, dcc, html, dash_table
from dash_iconify import DashIconify
from dplython import (DplyFrame, X, diamonds, select, sift, sample_n,
                      sample_frac, head, arrange, mutate, group_by,
                      summarize, DelayFunction)

#from data.MoonStoneData import MoonStoneData, table

external_scripts = ["https://oss.sheetjs.com/sheetjs/xlsx.full.min.js"]
external_stylesheets = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"
]
app = dash.Dash(
    __name__,
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets,
)

styles = {"pre": {"border": "thin lightgrey solid", "overflowX": "scroll"}}

"""
df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
)

# This adds an "id" column
df = df.reset_index().rename(columns={"index": "id"})
"""




# =============================================================================
# Query Data
# =============================================================================
csv_file = "data/Dec22a.csv"
csv_data = pd.read_csv(csv_file)
table = pd.DataFrame(csv_data)

MoonStoneData = DplyFrame(table)

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

Query6 = (diamondsSmall >> 
         
#        mutate(carat_bin=X.carat.round()) >> 
         group_by( X.Status) >>
         sift(X.Portfolio == 'New Book') >>
         summarize(count=X.Status.count(), amt=np.sum(X.Amt)) 
         
         
         #arrange(X.Portfolio) 
         #crosstab(X.Portfolio, X.Status)   
)

#Query6.append(Query6.sum(numeric_only=True), ignore_index=True)
#df.loc['Column_Total']= df.sum(numeric_only=True, axis=0)
#df.loc[:,'Row_Total'] = df.sum(numeric_only=True, axis=1)

#Query6.loc['Column_Total']= Query6.sum(numeric_only=True, axis=0)

print(Query6)

datasam = diamondsSmall.head(500)
Query1 = pd.pivot_table(data=diamondsSmall, 
                    index=['Product'],
                    columns=['Status'],
                    values=['Amt'], aggfunc=['count'], #{diamondsSmall['Status']:np.count_nonzero,'Amt':np.sum},
                    margins = True, margins_name='Total')

Query1.columns = Query1.columns.droplevel(0)
Query1.columns = Query1.columns.droplevel(0)
data = datasam.to_dict("records")
print(Query1)
print(data)
columns = [
    {"title": "Vertical", "field": "Status", "hozAlign": "left", "headerFilter": True},
    {"title": "Product", "field": "count", "hozAlign": "left", "headerFilter": True,},
    {"title": "Closed", "field": "amt", "hozAlign": "left", "headerFilter": True},

"""
    {
        "title": "POS_Dec_22_in_Crs",
        "field": "Disb_Amount_in_Lacs",
        "formatter": "money",
        "formatterParams": {"precision": 0},
        "topCalc": "avg",
        "topCalcParams": {"precision": 0},
        "topCalcFormatter": "money",
        "topCalcFormatterParams": {"precision": 0},
        "hozAlign": "right",
    },

    {
        "title": "Life Expectancy",
        "field": "Status",
        "hozAlign": "right",
        "formatter": "money",
        "formatterParams": {"precision": 1},
        "topCalc": "avg",
        "topCalcParams": {"precision": 1},
    },
    {
        "title": "GDP Per Capita",
        "field": "Disb_Amount_in_Lacs",
        "hozAlign": "right",
        "formatter": "money",
        "formatterParams": {"precision": 2},
        "topCalc": "avg",
        "topCalcParams": {"precision": 2},
        "topCalcFormatter": "money",
        "topCalcFormatterParams": {"precision": 2},
    },
"""
]

# Note:  With  large datasets, it's necessary to set the maxHeight for the table otherwise the app will be slow.
#        See more info here:  http://tabulator.info/docs/4.8/virtual-dom
options = {"groupBy": "Vertical", "selectable": 1, "maxHeight": "500px"}
downloadButtonType = {"css": "btn btn-primary", "text": "Export", "type": "xlsx"}
clearFilterButtonType = {"css": "btn btn-outline-dark", "text": "Clear Filters"}

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

CardHeader = "Raghuveer Kamble"
CardTitle = "Raavan"
CardTable = Query6

VerticalCards = html.Div(
    [
        html.Br(),
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content(CardHeader, CardTitle, CardTable), color="primary", outline=True)),
            ],
            className="mb-4",
        ),
])


VerticalCardsTab = html.Div(
    [
        dash_tabulator.DashTabulator(
            
            id="table",
            columns=columns,
            data=Query6,
            options=options,
            #downloadButtonType=downloadButtonType,
            #clearFilterButtonType=clearFilterButtonType,
        ),
        # dcc.Graph(id="graph"),
    ], 
)

app.layout = VerticalCards



"""

@app.callback(
    Output("graph", "figure"), Input("table", "dataFiltering"),
)


def display_output(filters):
    dff = df.copy()
    dff["year"] = dff["year"].astype(str)
    for filter_col in filters:
        dff = dff[
            dff[filter_col["field"]].str.contains(filter_col["value"], case=False)
        ]
"""
"""
    fig = (
        px.scatter(
            dff,
            x="gdpPercap",
            y="lifeExp",
            size="pop",
            color="continent",
            hover_name="country",
            log_x=True,
            size_max=55,
        )
        if not dff.empty
        else {}
    )
    return fig
"""

if __name__ == "__main__":
    app.run_server(debug=False)