# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:18:52 2022

@author: raghu
"""

import dash_admin_components as dac
from dash import Dash, html, dcc

from example_plots import plot_pie, plot_surface, plot_scatter

dropdown_items = [
	dac.BoxDropdownItem(url="https://www.google.com", children="Link to google"),
	dac.BoxDropdownItem(url="#", children="item 2"),
	dac.BoxDropdownDivider(),
	dac.BoxDropdownItem(url="#", children="item 3")
]

KPIcards_tab = dac.TabItem(id='content_Portfolio_KPI1', 
                              
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