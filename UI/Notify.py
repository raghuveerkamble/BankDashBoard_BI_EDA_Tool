
# from dash import Dash, html, dcc, dash_table
from dash import Input, Output, State
import dash_admin_components as dac
# from dash.exceptions import PreventUpdate
# import dash_bootstrap_components as dbc



Notify = dac.NavbarDropdown(
    badge_label="!",
    badge_color="danger",
    src="https://kamble.ai",
    header_text="2 Items",
    children=[
        dac.NavbarDropdownItem(
            children="Random message 1",
            date = "today"
            ),
        dac.NavbarDropdownItem(
            children = "Example message 2",
            date = "yesterday"
            ),
        ]
)
