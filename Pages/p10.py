# =============================================================================
# Nature of Business
# =============================================================================
import pandas as pd 
import numpy as np
import datetime as dt

from dplython import (DplyFrame, X, diamonds, select, sift, sample_n,
                      sample_frac, head, arrange, mutate, group_by,
                      summarize, DelayFunction)

import dash
from dash import Dash, html, dcc, dash_table
import dash_admin_components as dac
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Group
from dash.dependencies import Input, Output, State

import plotly.offline as pyo 
import plotly.graph_objs as go 
import plotly.express as px
import plotly.io as pio

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



def make_dash_table(df):
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table


def table_from_df(df) -> str:
    """Generate a html table from a pandas DataFrame"""

    header_row = "\n".join([f'      <th scope="col">{col}</th>' for col in df.columns])
    body_rows = ""
    for i, row in df.iterrows():
        body_rows += (
            "    <tr>\n"
            + "\n".join(["      <td>" + str(val) + "</td>" for val in row.values])
            + "\n    </tr>\n"
        )

    table = f"""
<table class="table">
  <thead>
    <tr>
{header_row}
    </tr>
  </thead>
  <tbody>
{body_rows}
  </tbody>
</table>
    """
    return table



Query8 = (pd.pivot_table(data=diamondsSmall,
                       index=['Portfolio'], columns=['DEC_22_CL_BKT'],
                       values=['Amt'], aggfunc=['count'], 
                       margins = True, margins_name='Total') #.reset_index() #, as_index=False
         )
Query8.columns = Query8.columns.droplevel(0)
Query8.columns = Query8.columns.droplevel(0) 


CardTable2 = dbc.Table.from_dataframe(
    Query8, striped=False, bordered=True, hover=True, index=True, responsive=True
)

product_cards_sub_tab2 = dash_table.DataTable(
                    data=Query3.to_dict("records"),
                    columns=[{"name": x, "id": x} for x in Query3],
                    style_as_list_view=True,
                    editable=False,
                    style_table={
                        "overflowY": "scroll",
                        "width": "100%",
                        "minWidth": "100%",
                    },
                    style_header={"backgroundColor": "#f8f5f0", "fontWeight": "bold"},
                    style_cell={"textAlign": "center", "padding": "8px"}
                )



"""
datasam1 = diamondsSmall >> group_by( X.Status)
datasam = datasam1.head(500)
"""

Query9 = round((diamondsSmall >> 
         #mutate(carat_bin=X.carat.round()) >> 
         group_by( X.Status) >>
         sift(X.Portfolio == 'New Book') >>
         summarize(count=X.Amt.count(), amt=np.sum(X.Amt)) 
         #arrange(X.Portfolio) 
         #crosstab(X.Portfolio, X.Status)   
),2)
Query9['PCount'] = round((Query9['count']/Query9['count'].sum())*100,2)
Query9['PAmt'] = round((Query9['amt']/Query9['amt'].sum())*100,2)
#Query9.loc['Total']= round(Query9.sum(numeric_only=True, axis=0),2)
data = Query9.to_dict("records")


#data = datasam.to_dict("records")
columns = [
    {"title": "Status", "field": "Status", "hozAlign": "left", "headerFilter": True},
    {"title": "count", "field": "count", "hozAlign": "left", "headerFilter": True,},
    {"title": "amt", "field": "amt", "hozAlign": "left", "headerFilter": True},
#    {"title":"Progress", "field":"PCount", "formatter":"progress", "formatterParams":"{"color":"["#00dd00", "orange", "rgb(255,0,0)"]"}", "sorter":"number", "width":"100"},
    {"title":"Line Chart", "field":"line", "width":"160", "formatter":"chartFormatter", "formatterParams":{"type":"line"}},
    {
        "title": "amt",
        "field": "PAmt",
        "formatter": "progress",
        "formatterParams": {"precision": 0},
        "topCalc": "sum",
        "topCalcParams": {"precision": 0},
        "topCalcFormatter": "money",
        "topCalcFormatterParams": {"precision": 0},
        "hozAlign": "right",
    },
"""
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
#options = {"groupBy": "Vertical", "selectable": 1, "maxHeight": "500px"}
downloadButtonType = {"css": "btn btn-primary", "text": "Export", "type": "xlsx"}
clearFilterButtonType = {"css": "btn btn-outline-dark", "text": "Clear Filters"}

VerticalTabData = html.Div(
    [
        dash_tabulator.DashTabulator(
            
            id="table",
            columns=columns,
            data=data,
            #options=options,
            #downloadButtonType=downloadButtonType,
            #clearFilterButtonType=clearFilterButtonType,
        ),
 #       dcc.Graph(id="graph"),
    ], 
)


# =============================================================================
# MAke Table Card Data
# =============================================================================



def make_dash_table(df):
    table = []
    
    #header_row = "\n".join([{col} for col in df.columns])
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table

def create_table(df):
    columns, values = df.columns, df.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    table = [html.Thead(header), html.Tbody(rows)]
    return table

def table_from_df(df) -> str:
    """Generate a html table from a pandas DataFrame"""

    header_row = "\n".join([f'      <th scope="col">{col}</th>' for col in df.columns])
    body_rows = ""
    for i, row in df.iterrows():
        body_rows += (
            "    <tr>\n"
            + "\n".join(["      <td>" + str(val) + "</td>" for val in row.values])
            + "\n    </tr>\n"
        )

    table = f"""
<table class="table">
  <thead>
    <tr>
{header_row}
    </tr>
  </thead>
  <tbody>
{body_rows}
  </tbody>
</table>
    """
    return table




CardHeader = "Portfolio Insights"
CardTitle = "Raghuveer Kamble"
CardTable = make_dash_table(table1)
CardTable1 = make_dash_table(table1)
#CardTable2 = make_dash_table(table1)
CardTable3 = make_dash_table(table3)
CardTable4 = make_dash_table(table4)
CardTable5 = make_dash_table(table5)

labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
values = [4500, 2500, 1053, 500]


fig1 = dbc.Card([
    dbc.CardBody([
               dcc.Graph(id='tips-bar-chart', figure=dict(
                   data=[go.Pie(labels=labels,values=values)]
               ))
    ])
 ],className='cardDesign')

fig2 = dbc.Card([
    dbc.CardBody([
               dcc.Graph(figure=dict(
                   data=[go.Pie(labels=labels,values=values)]
               ))
    ])
 ],className='cardDesign')

fig3 = dbc.Card([
    dbc.CardBody([
               dcc.Graph(figure=dict(
                   data=[go.Bar(x=labels,y=values)]
               ))
    ])        
],className='cardDesign')




#

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


def box_card_content(CardTitle, CardTable):
    box_card_content = ([
        dac.Box(
                [
                    dac.BoxHeader(
                        collapsible = True,
                        closable = True,
                        title=CardTitle
                    ),
                	dac.BoxBody(CardTable)		
                ],
                color='primary',
                #solid_header=True,
                #elevation=4,
                width='auto'
            )])
    return box_card_content


tab1_NOB_content = html.Div(
    [
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content(CardHeader1, CardTitle1, CardTable1), color="primary", inverse=True)),
                dbc.Col(
                    dbc.Card(card_content(CardHeader2, CardTitle2, CardTable2), color="secondary", inverse=True)
                ),
                dbc.Col(dbc.Card(card_content(CardHeader3, CardTitle3, CardTable), color="info", inverse=True)),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(fig1, color="success", inverse=True)),
                dbc.Col(dbc.Card(fig2, color="warning", inverse=True)),
                dbc.Col(dbc.Card(fig3, color="danger", inverse=True)),
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

text_1 = "Raavan"
text_2 = "Kamble"
text_3 = "Lankini"

product_tab_cards_tab = dac.TabItem(id='content_tab_cards', 
                              
    children=[
        html.Div(
            [
                html.Hr(),    
                dac.TabBox(
                    [
                        dac.TabBoxHeader(
        					dac.TabBoxMenu(
                                [
                                    dac.TabBoxMenuItem(tab_id='tab_box_1_tab1',
                                                       label='Tab 1'),
                                    dac.TabBoxMenuItem(tab_id='tab_box_1_tab2',
                                                       label='Tab 2'),
                                    dac.TabBoxMenuItem(tab_id='tab_box_1_tab3',
                                                       label='Tab 3') 
                                ],
                                id='tab_box_1_menu'
                            ),
                            collapsible = True,
                            closable = True,
                            title="A card with tabs"
                        ),
                    	dac.TabBoxBody(
                            id='tab_box_1'
                        )		
                    ],
                    color='success',
                    width=6,
                    elevation=2
                ),
                dac.TabBox(
                    [
                        dac.TabBoxHeader(
        					dac.TabBoxMenu(
                                [
                                    dac.TabBoxMenuItem(tab_id='tab_box_2_tab1',
                                                       label='Chart', 
                                                       color='dark'), #dark
                                    dac.TabBoxMenuItem(tab_id='tab_box_2_tab2',
                                                       label='Tab 2', 
                                                       color='dark'),
                                    dac.TabBoxMenuItem(tab_id='tab_box_2_tab3',
                                                       label='Tab 3', 
                                                       color='dark') 
                                ],
                                id='tab_box_2_menu'
                            ),
                            collapsible = True,
                            closable=True,
                            title="A card with colorful tabs"
                        ),
                    	dac.TabBoxBody(
                            id='tab_box_2'
                        )		
                    ],
                    color='warning', #'warning',
                    width=6,
                    elevation=2
                )
            ], 
            className='row'
        )
            
    ]
)

product_cards_sub_tab = html.Div([
    html.Hr(),
    dac.TabBox(
    [
        dac.TabBoxHeader(
            dac.TabBoxMenu(
                [
                    
                dac.TabBoxMenuItem(tab_id='tab_box_2_tab1',
                                        label='Tab 1', 
                                        color='dark'),
                    dac.TabBoxMenuItem(tab_id='tab_box_2_tab2',
                                        label='Tab 2', 
                                        color='danger'),
                    dac.TabBoxMenuItem(
                                        tab_id='tab_box_2_tab3',
                                        label='Tab 3', 
                                        color='primary') 
                ],
                id='tab_box_2_menu'
            ),
            collapsible = True,
            closable=True,
            title="..."
        ),
        dac.TabBoxBody(id='tab_box_2', children=product_cards_sub_tab2)		
    ],
    color='warning',
    width=12,
    elevation=2
)
])


# =============================================================================
# App Layout
# =============================================================================
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server
app.title = 'Moon Stone'

app.layout = dac.Page([tab1_NOB_content])

# =============================================================================
# Call Back
# =============================================================================

@app.callback(Output('tab_box_1', 'children'),
              [Input('tab_box_1_menu', 'active_tab')]
              )

def display_tabbox1(active_tab):
    # Depending on tab which triggered a callback, show/hide contents of app
    if active_tab == 'tab_box_1_tab1':
        return RetailVertical
    elif active_tab == 'tab_box_1_tab2':
        return product_cards_sub_tab2
    elif active_tab == 'tab_box_1_tab3':
        return text_3

@app.callback(Output('tab_box_2', 'children'),
              [Input('tab_box_2_menu', 'active_tab')]
)

def display_tabbox2(active_tab):
    # Depending on tab which triggered a callback, show/hide contents of app
    if active_tab == 'tab_box_2_tab1':
        return text_1
    elif active_tab == 'tab_box_2_tab2':
        return text_2
    elif active_tab == 'tab_box_2_tab3':
        return text_3



# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
