
from dash import Dash, html, dcc, dash_table
#from dash.dependencies import Input, Output
from dash import Input, Output, State, html
import dash_admin_components as dac
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from UI.About import AboutMe as About, Avatar
from UI.Notify import Notify
# Navbar




navbar = dac.Navbar(color = "white", 
                    text="Moon Stone Analytics Tool!",
                    children=[#Notify,
                              Avatar,
                              #html.A("k", href=""),
                              About,
                              #dropdown,
                              #right_ui1,
                              #right_ui2,
                              ]
                    )

"""

dropdown = html.Div(
    [
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem(
                    "A button", id="dropdown-button", n_clicks=0
                ),
                dbc.DropdownMenuItem(
                    "Internal link", href="/docs/components/dropdown_menu"
                ),
                dbc.DropdownMenuItem(
                    "External Link", href="https://kamble.ai"
                ),
                dbc.DropdownMenuItem(
                    "External relative",
                    href="/docs/components/dropdown_menu",
                    external_link=True,
                ),
            ],
            label="About",
        ),
        #html.P(id="item-clicks", className="mt-3"),
    ]
)




right_ui1 = dac.SidebarButton(
                                icon='ghost',
                                n_clicks=0,
                                color='white',
                                id="about"
                              )

right_ui2 = dac.NavbarDropdown(
                                 header_text="About",
                                 menu_icon='ghost',
                                 badge_color="success",
                                 id="about"
                               )

"""