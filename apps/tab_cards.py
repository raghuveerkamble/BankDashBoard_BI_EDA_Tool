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

from data.MoonStoneData import MoonStoneData, table 


# =============================================================================
# Data
# =============================================================================


diamondsSmall = MoonStoneData >> select(X.Portfolio, X.Vertical, X.Segment, X.Status,  X.Disb_Amount_in_Lacs, X.Branch )

"""
print(diamondsSmall >> head(4))
print(diamondsSmall >> sample_n(5))
table = pd.pivot_table(data=diamondsSmall,  index=['Book', 'Product_Type'], columns=['Status_CC_MIS'], values=['Disb_Amount_in_Lacs'], aggfunc= np.sum)
table = pd.pivot_table(diamondsSmall, index=['Book', 'Product_Type'], aggfunc={'Status_CC_MIS':np.count_nonzero,'Disb_Amount_in_Lacs':np.sum})
"""
table = pd.pivot_table(data=diamondsSmall,  
                       index=['Portfolio', 'Segment'], columns=['Status'], 
                       values=['Disb_Amount_in_Lacs'], aggfunc= ['count', 'sum'],
                       margins = True, margins_name='Total')


text_1 =  ["A wonderful serenity has taken possession of my entire soul",
           "like these sweet mornings of spring which I enjoy with my",
           "whole heart. I am alone, and feel the charm of existence in",
           "this spot, which was created for the bliss of souls like mine.",
           "I am so happy, my dear friend, so absorbed in the exquisite sense",
           "of mere tranquil existence, that I neglect my talents. I should be",
           "incapable of drawing a single stroke at the present moment; and yet",
           "I feel that I never was a greater artist than now"]

text_2 =  ["The European languages are members of the same family.",
           "Their separate existence is a myth. For science, music,",
           "sport, etc, Europe uses the same vocabulary. The languages",
           "only differ in their grammar, their pronunciation and their",
           "most common words. Everyone realizes why a new common",
           "language would be desirable: one could refuse to pay expensive",
           "translators. To achieve this, it would be necessary to have",
           "uniform grammar, pronunciation and more common words. If several",
           "languages coalesce, the grammar of the resulting language is",
           "more simple and regular than that of the individual languages."]

text_3 =  ["Lorem Ipsum is simply dummy text of the printing and",
           "typesetting industry. Lorem Ipsum has been the industry's",
           "standard dummy text ever since the 1500s, when an unknown",
           "printer took a galley of type and scrambled it to make a",
           "type specimen book. It has survived not only five centuries,",
           "but also the leap into electronic typesetting, remaining",
           "essentially unchanged. It was popularised in the 1960s with",
           "the release of Letraset sheets containing Lorem Ipsum passages,",
           "and more recently with desktop publishing software like Aldus",
           "PageMaker including versions of Lorem Ipsum."]

tab_cards_tab = dac.TabItem(id='content_tab_cards', 
                              
    children=[
     
        html.Div(
            [
                    
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
                            collapsible = False,
                            closable = True,
                            title="A card with tabs"
                        ),
                    	dac.TabBoxBody(
                            id='tab_box_1'
                        )		
                    ],
                    width=6,
                    elevation=2
                ),
                        
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
                                    dac.TabBoxMenuItem(tab_id='tab_box_2_tab3',
                                                       label='Tab 3', 
                                                       color='primary') 
                                ],
                                id='tab_box_2_menu'
                            ),
                            closable=True,
                            title="A card with colorful tabs"
                        ),
                    	dac.TabBoxBody(
                            id='tab_box_2'
                        )		
                    ],
                    color='warning',
                    width=6,
                    elevation=2
                )
            ], 
            className='row'
        )
            
    ]
)
