
from dash import Dash, html, dcc, dash_table
#from dash.dependencies import Input, Output
from dash import Input, Output, State, html
import dash_admin_components as dac
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc



# Footer
footer = dac.Footer(
    html.A(html.Div([" Raghuveer Kamble, Moon Stone",
            html.Img(src="assets/ravan.ico", className="rounded float-left", alt="Kamble...", height=30)]),
           href="https://www.linkedin.com/in/raghuveerkamble/",
           target="_blank",),
    
    right_text="Copyright 2018"
)