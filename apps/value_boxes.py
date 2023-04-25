# import dash_html_components as html
import dash_admin_components as dac
from dash import Dash, html, dcc
from dplython import (DplyFrame, X, diamonds, select, sift, sample_n,
                      sample_frac, head, arrange, mutate, group_by,
                      summarize, DelayFunction)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')


from example_plots import plot_pie, plot_surface, plot_scatter


def TableTry():
    p_file = "data/July22.xlsx"
    diamonds = DplyFrame(pd.read_excel(p_file))
    diamondsSmall = diamonds >> select(X.Book, X.Product_Type, X.Status_CC_MIS, X.Status, X.Disb_Amount_in_Lacs, X.Branch  , X.DPD_Bucket_Coll_Rep)
    table = pd.pivot_table(data=diamondsSmall,  
                       index=['Book', 'Product_Type'], columns=['Status_CC_MIS'], 
                       values=['Disb_Amount_in_Lacs'], aggfunc= ['count', 'sum'],
                       margins = True, margins_name='Total')
    return dict(data=[table]) 

dropdown_items = [
	dac.BoxDropdownItem(url="https://www.google.com", children="Link to google"),
	dac.BoxDropdownItem(url="#", children="item 2"),
	dac.BoxDropdownDivider(),
	dac.BoxDropdownItem(url="#", children="item 3")
]

value_boxes_tab = dac.TabItem(id='content_value_boxes',
  children=[
    html.Div(
            [
                    
                dac.Box(
                    [
                        dac.BoxHeader(
        					dac.BoxDropdown(dropdown_items),
                            collapsible = True,
                            closable = True,
                            title="Closable box with dropdown"
                        ),
                    	dac.BoxBody(
                            dcc.Graph(
                                figure=plot_pie(),
                                config=dict(displayModeBar=False),
                                style={'width': '38vw'}
                            )
                        )		
                    ],
                    color='warning',
                    width=6
                ),
                        
                dac.Box(
                    [
                        dac.BoxHeader(
                            collapsible = True,
                            closable = True,
                            title="Closable box with gradient"
                        ),
                    	dac.BoxBody(
                            dcc.Graph(
                                figure=plot_surface(),
                                config=dict(displayModeBar=False),
                                style={'width': '38vw'}
                            )
                        )		
                    ],
                    gradient_color="success",
                    width=6
                )
            ], 
            className='row'
        ),
                        
        html.Div(    
            dac.Box(
                [
                    dac.BoxHeader(
                        collapsible = True,
                        closable = True,
                        title="Card with solidHeader and elevation"
                    ),
                	dac.BoxBody(
                        dcc.Graph(
                            figure=plot_scatter(),
                            config=dict(displayModeBar=False),
                            style={'width': '38vw'}
                        )
                    )		
                ],
                color='primary',
                solid_header=True,
                elevation=4,
                width=6
            ),
            className='row'
        )
            
    ]
)