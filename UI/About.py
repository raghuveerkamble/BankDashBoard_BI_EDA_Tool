
from dash import Dash, dcc, dash_table, Input, Output, State, html
import dash_admin_components as dac
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

Avatar = html.A(
    dmc.Tooltip(
        dmc.Avatar(
            src="assets/Kamblelogo.png",
            size="sm",
            radius="xl",
        ),
        label="Raghuveer Kamble",
        position="bottom",
    ),
    href="https://www.linkedin.com/in/raghuveerkamble/",
    target="_blank",
)

"""
        dbc.Button( id="open", n_clicks=0, className = "ghost",
        children = html.Div(["About ",
            html.Img(src="assets/command.svg", height=18),
            #html.Button('About', id='open', n_clicks=0),
        ])
        ),
"""

AboutIcon = dmc.ActionIcon(
    DashIconify(icon="icomoon-free:sun", width=20), #clarity:settings-line, game-icons:alien-stare
    size="lg",
    radius="lg",
    variant="light", #"filled",
    id="open",
    color="red",
    #pos="center",
    n_clicks=0,
    mb=10,
)

AboutButton = dmc.Button(
    "About",
    variant="subtle",
    rightIcon=DashIconify(icon="fluent:settings-32-regular"),
    color="blue",
    id="open", n_clicks=0,
)
        

AboutMe = html.Div(
    [
        
        AboutIcon,
        dbc.Modal(
            [
                dbc.ModalHeader([
                    html.Img(src="assets/Kamblelogo.png", className="rounded float-left", alt="Kamble...", height=50),
                    dbc.ModalTitle("Moon Stone..."),
                ]),
                dbc.ModalBody([
                    dbc.Row([
                    dbc.Col(dac.UserCard(
                        src = "assets/ravan.jpg",
                        color = "success",
                        title = "Kamble Data Solutions",
                        subtitle = "www.kamble.ai",
                        elevation = 4,
                        children= ([#"Unlock the power of AI", 
                                  "Accelerate and operationalize data science projects and",
                                  "enable your business to make AI driven decisions at scale.",
                                  #"Automated AI - Increase data science productivity",
                                  #"Democratized AI - Enable citizen data scientists",
                                  #"Extend your AI - Leverage data science best practices",
                                  #"Operationalize AI – Deploy AI models 40 times faster",
                                  #"Drive ROI with AI - Realise the value of data science projects"
                                  ])
                    ), width=100),
                    dbc.Col(dac.UserCard(
                        #src = "https://adminlte.io/themes/AdminLTE/dist/img/user1-128x128.jpg",
                        type = 2,
                        src = "assets/Raavan.jpg",
                        color = "info",
                        title = "Raghuveer Kamble",
                        subtitle = "...",
                        elevation = 4,
                        children="Moon Stone Analytical Tool - created for Easier & Effective Data Modeling"
                    ), width=100),
                    ])
            ]),
                dbc.ModalFooter([
                    #html.Img(src="assets/ravan.ico", className="rounded float-left", alt="Kamble...", height=50),
                    dbc.Button(
                        "Close", id="close", className="ms-auto", n_clicks=0
                    )]
                ),
            ],
            id="modal",
            size="lg", #sl - small, lg-large, xl-extra
            is_open=False,
        ),
        
    ]
)