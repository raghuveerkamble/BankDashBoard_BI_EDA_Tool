# Raghuveer Kamble : Moon Stone Project...

import dash
import dash_pivottable
import pandas as pd
import numpy as np
import time

from dash import Dash, html, dcc, dash_table
from dash import Input, Output, State, html
import dash_admin_components as dac
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from apps.cards import cards_tab
from apps.social_cards import social_cards_tab, cards
from apps.tab_cards import tab_cards_tab, text_1, text_2, text_3
from apps.basic_boxes import basic_boxes_tab
from apps.value_boxes import value_boxes_tab
from apps.basic_kpi_boxes import kpi_basic_boxes_tab # boxkpicards, boxcards
from apps.value_kpi_boxes import kpi_value_boxes_tab
from apps.Product_KPIcards import kpi_product_boxes_tab
from example_plots import plot_scatter


from UI.Header import navbar
from UI.Footer import footer
from UI.Menu import sidebar

from dplython import (DplyFrame, X, diamonds, select, sift, sample_n,
                      sample_frac, head, arrange, mutate, group_by,
                      summarize, DelayFunction)
import matplotlib.pyplot as plt
import plotly.graph_objs as go
plt.style.use('ggplot')

import dash_mantine_components as dmc
from dash_iconify import DashIconify
#from example_plots import plot_scatter

csv_file = "data/Dec22.csv"
csv_data = pd.read_csv(csv_file)
table = pd.DataFrame(csv_data)

Query1 = table[["Portfolio", "Vertical", "Segment", "Product", "Borrower", "Status", "Amt"]]
					

#dict = {'Book': 'Portfolio', 'Vertical': 'Product',
#        'Status': 'Status', 'Disb_Amount_in_Lacs': 'Amt'}
#Query1.rename(columns=dict, inplace=True)

Total_rows = Query1.shape[0]
Query2 = table[["Portfolio", "Vertical", "Status", "Amt", "POS_Dec_22_in_Crs"]]


# FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"
# =============================================================================
# Dash App and Flask Server
# =============================================================================
#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_AWESOME])
#app = Dash(__name__)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server
app.title = 'Moon Stone'

# =============================================================================
# Dash Admin Components
# =============================================================================


# Body

body = dac.Body(
    dac.TabItems([
        cards_tab,
        social_cards_tab,
        tab_cards_tab,
        basic_boxes_tab,
        value_boxes_tab,
        kpi_basic_boxes_tab,
        kpi_value_boxes_tab,
        kpi_product_boxes_tab,
   
        dac.TabItem(html.P('Gallery 1'), 
                    id='content_gallery_1'),
        dac.TabItem(html.P('Gallery 2'), 
                    id='content_gallery_2'),
    ])
)

# Controlbar
controlbar = dac.Controlbar(
    [
        html.Br(),
        html.P("Slice & Dice"),
        dcc.Slider(
            id='controlbar-slider',
            min=10,
            max=50,
            step=1,
            value=20
        )
    ],
    title="Filters",
    skin="light"
)




# =============================================================================
# App Layout
# =============================================================================
app.layout = dac.Page([navbar, sidebar, body, controlbar, footer])

# =============================================================================
# Callbacks
# =============================================================================


def activate(input_id,
             n_cards, n_social_cards, n_tab_cards, n_basic_boxes,
             n_value_boxes, n_kpi_basic_boxes, n_kpi_value_boxes,
             n_kpi_product_boxes, n_gallery_1, n_gallery_2):

    # Depending on tab which triggered a callback, show/hide contents of app
    if input_id == 'tab_cards' and n_cards:
        return True, False, False, False, False, False, False, False, False, False
    elif input_id == 'tab_social_cards' and n_social_cards:
        return False, True, False, False, False, False, False, False, False, False
    elif input_id == 'tab_tab_cards' and n_tab_cards:
        return False, False, True, False, False, False, False, False, False, False
    elif input_id == 'tab_basic_boxes' and n_basic_boxes:
        return False, False, False, True, False, False, False, False, False, False
    elif input_id == 'tab_value_boxes' and n_value_boxes:
        return False, False, False, False, True, False, False, False, False, False
    elif input_id == 'tab_kpi_basic_boxes' and n_kpi_basic_boxes:
        return False, False, False, False, False, True, False, False, False, False
    elif input_id == 'tab_kpi_value_boxes' and n_kpi_value_boxes:
        return False, False, False, False, False, False, True, False, False, False
    elif input_id == 'tab_kpi_product_boxes' and n_kpi_product_boxes:
        return False, False, False, False, False, False, False, True, False, False
    elif input_id == 'tab_gallery_1' and n_gallery_1:
        return False, False, False, False, False, False, False, False, True, False
    elif input_id == 'tab_gallery_2' and n_gallery_2:
        return False, False, False, False, False, False, False, False, False, True
    else:
        return True, False, False, False, False, False, False, False, False, False # App init
    
@app.callback([Output('content_cards', 'active'),
               Output('content_social_cards', 'active'),
               Output('content_tab_cards', 'active'),
               Output('content_basic_boxes', 'active'),
               Output('content_value_boxes', 'active'),
               Output('content_kpi_basic_boxes', 'active'),
               Output('content_kpi_value_boxes', 'active'),
               Output('content_kpi_product_boxes', 'active'),
               Output('content_gallery_1', 'active'),
               Output('content_gallery_2', 'active')],
               [Input('tab_cards', 'n_clicks'),
                Input('tab_social_cards', 'n_clicks'),
                Input('tab_tab_cards', 'n_clicks'),
                Input('tab_basic_boxes', 'n_clicks'),
                Input('tab_value_boxes', 'n_clicks'),
                Input('tab_kpi_basic_boxes', 'n_clicks'),
                Input('tab_kpi_value_boxes', 'n_clicks'),
                Input('tab_kpi_product_boxes', 'n_clicks'),
                Input('tab_gallery_1', 'n_clicks'),
                Input('tab_gallery_2', 'n_clicks')]
)
def display_tab(n_cards, n_social_cards, n_tab_cards, n_basic_boxes,
                n_value_boxes, n_kpi_basic_boxes, n_kpi_value_boxes,
                n_kpi_product_boxes, n_gallery_1, n_gallery_2):
    
    ctx = dash.callback_context # Callback context to recognize which input has been triggered

    # Get id of input which triggered callback  
    if not ctx.triggered:
        raise PreventUpdate
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]   

    return activate(input_id, 
                    n_cards, n_social_cards, n_tab_cards, n_basic_boxes,
                    n_value_boxes, n_kpi_basic_boxes, n_kpi_value_boxes,
                    n_kpi_product_boxes, n_gallery_1, n_gallery_2)
#
@app.callback([Output('tab_cards', 'active'),
               Output('tab_social_cards', 'active'),
               Output('tab_tab_cards', 'active'),
               Output('tab_basic_boxes', 'active'),
               Output('tab_value_boxes', 'active'),
               Output('tab_kpi_basic_boxes', 'active'),
               Output('tab_kpi_value_boxes', 'active'),
               Output('tab_kpi_product_boxes', 'active'),
               Output('tab_gallery_1', 'active'),
               Output('tab_gallery_2', 'active')],
               [Input('tab_cards', 'n_clicks'),
                Input('tab_social_cards', 'n_clicks'),
                Input('tab_tab_cards', 'n_clicks'),
                Input('tab_basic_boxes', 'n_clicks'),
                Input('tab_value_boxes', 'n_clicks'),
                Input('tab_kpi_basic_boxes', 'n_clicks'),
                Input('tab_kpi_value_boxes', 'n_clicks'),
                Input('tab_kpi_product_boxes', 'n_clicks'),
                Input('tab_gallery_1', 'n_clicks'),
                Input('tab_gallery_2', 'n_clicks')])
#
def activate_tab(n_cards, n_social_cards, n_tab_cards, n_basic_boxes,
                 n_value_boxes, n_kpi_basic_boxes, n_kpi_value_boxes,
                 n_kpi_product_boxes, n_gallery_1, n_gallery_2):

    ctx = dash.callback_context
    # Callback context to recognize which input has been triggered

    # Get id of input which triggered callback
    if not ctx.triggered:
        raise PreventUpdate
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    return activate(input_id,
                    n_cards, n_social_cards, n_tab_cards, n_basic_boxes,
                    n_value_boxes, n_kpi_basic_boxes, n_kpi_value_boxes,
                    n_kpi_product_boxes, n_gallery_1, n_gallery_2)


@app.callback(Output('tab_box_1', 'children'),
              [Input('tab_box_1_menu', 'active_tab')]
              )

def display_tabbox1(active_tab):
    # Depending on tab which triggered a callback, show/hide contents of app
    if active_tab == 'tab_box_1_tab1':
        return text_1
    elif active_tab == 'tab_box_1_tab2':
        return text_2
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







def sub_tab4():
    return html.Div([
        html.H3('Slice & Dice Overview'),
        dash_pivottable.PivotTable(
            id="table",
            data=table.to_dict(orient='records'),
            cols=["Status"],
            colOrder="key_a_to_z",
            rows=["Book", "Vertical"],
            rowOrder="key_a_to_z",
            rendererName="Grouped Column Chart",
            aggregatorName="Average",
            vals=["Disb_Amount_in_Lacs"],
            valueFilter={"Status": {"Live": False}}
            )
    ])

def sub_tab1():
    return html.Div([
        html.H3('Raavan'),
        dash_pivottable.PivotTable(
            id="table",
            data=table.to_dict(orient='records'),
            cols=["Status"],
            colOrder="key_a_to_z",
            rows=["Book", "Vertical"],
            rowOrder="key_a_to_z",
            rendererName="Grouped Column Chart",
            aggregatorName="Average",
            vals=["Disb_Amount_in_Lacs"],
            valueFilter={"Status": {"Live": False}}
            )
    ])

def sub_tab2():
    return html.Div([
        html.H3('Slice & Dice Overview'),
        dash_pivottable.PivotTable(
            id="table",
            data=table.to_dict(orient='records'),
            cols=["Status"],
            colOrder="key_a_to_z",
            rows=["Book", "Vertical"],
            rowOrder="key_a_to_z",
            rendererName="Grouped Column Chart",
            aggregatorName="Average",
            vals=["Disb_Amount_in_Lacs"],
            valueFilter={"Status": {"Live": False}}
            )
    ])

def sub_tab3():
    return html.Div([
        html.H3('Book Performance'),
        dash_pivottable.PivotTable(
            id="Query3",
            data=Query1.to_dict(orient='records'),
            cols=["Status"],
            colOrder="key_a_to_z",
            rows=["Portfolio", "Product"],
            rowOrder="key_a_to_z",
            rendererName= "Table",  #"Grouped Column Chart",
            aggregatorName="Sum",
            vals=["Amt"],
            valueFilter={"Status": {"Live1": False}}
            )
    ])


@app.callback(Output('tabs-content-props', 'children'),
              Input('tabs-styled-with-props', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return sub_tab1()
    elif tab == 'tab-2':
        return sub_tab2()
    elif tab == 'tab-3':
        return sub_tab3()
    elif tab == 'tab-4':
        return sub_tab4()

# Update figure on slider change

@app.callback(
    Output('box-graph', 'figure'),
    [Input('controlbar-slider', 'value')])
def update_box_graph(value):
    return plot_scatter(value)

@app.callback(
    Output("item-clicks", "children"), [Input("dropdown-button", "n_clicks")]
)
def count_clicks(n):
    if n:
        return f"Button clicked {n} times."
    return "Button not clicked yet."



@app.callback(
    Output("example-output", "children"), [Input("about", "n_clicks")]
)
def on_button_click(n):
    if n is None:
        return "Not clicked."
    else:
        return f"Clicked {n} times."

 
# =============================================================================
# AboutMe callback
# =============================================================================

@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# =============================================================================
# Social Cards Callback
# =============================================================================

@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")],
)
def render_tab_content(active_tab, data):

    if active_tab and data is not None:
        if active_tab == "scatter":
            return dcc.Graph(figure=data["scatter"])
        elif active_tab == "histogram":
            return dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=data["hist_1"]), width=6),
                    dbc.Col(dcc.Graph(figure=data["hist_2"]), width=6),
                ]
            )
        elif active_tab == "kpi":
            return cards
    return "No tab selected"


@app.callback(Output("store", "data"), [Input("button", "n_clicks")])
def generate_graphs(n):
    """
    This callback generates three simple graphs from random data.
    """
    if not n:
        # generate empty graphs when app loads
        return {k: go.Figure(data=[]) for k in ["scatter", "hist_1", "hist_2"]}

    # simulate expensive graph generation process
    time.sleep(2)

    # generate 100 multivariate normal samples
    data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], 100)

    scatter = go.Figure(
        data=[go.Scatter(x=data[:, 0], y=data[:, 1], mode="markers")]
    )
    hist_1 = go.Figure(data=[go.Histogram(x=data[:, 0])])
    hist_2 = go.Figure(data=[go.Histogram(x=data[:, 1])])

    # save figures in a dictionary for sending to the dcc.Store
    return {"scatter": scatter, "hist_1": hist_1, "hist_2": hist_2}


# =============================================================================
# Basix KPI Boxes Cards Callback
# =============================================================================

#--- No call back - Direct Tab content





# =============================================================================
# Run app
# =============================================================================

#if __name__ == '__main__':
#    app.run_server(debug=True)

if __name__ == "__main__":
    app.run_server(debug=False, port=8050)
