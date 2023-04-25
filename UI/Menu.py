
from dash import Dash, html, dcc, dash_table
#from dash.dependencies import Input, Output
from dash import Input, Output, State, html
import dash_admin_components as dac
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc



# Sidebar
subitems = [dac.SidebarMenuSubItem(id='tab_gallery_1', 
                            label='Gallery 1', 
                            icon='arrow-circle-right', 
                            badge_label='Soon',
                            badge_color='success'), 
			dac.SidebarMenuSubItem(id='tab_gallery_2', 
                            label='Gallery 2', 
                            icon='arrow-circle-right', 
                            badge_label='Soon', 
                            badge_color='success')
            ]
# Font awesome for icons
sidebar = dac.Sidebar(
	dac.SidebarMenu(
		[
			dac.SidebarHeader(children="Cards"),
			dac.SidebarMenuItem(id='tab_cards', label='Basic cards', icon='box'),
            dac.SidebarMenuItem(id='tab_social_cards', label='Data cards', icon='id-card'),
            dac.SidebarMenuItem(id='tab_tab_cards', label='Tab cards', icon='image'),
			dac.SidebarHeader(children="Boxes"),
			dac.SidebarMenuItem(id='tab_basic_boxes', label='Basic boxes', icon='desktop'),
			dac.SidebarMenuItem(id='tab_value_boxes', label='Value/Info boxes', icon='suitcase'),
            dac.SidebarHeader(children="Portfolio"),
			dac.SidebarMenuItem(id='tab_kpi_basic_boxes', label='Basic KPI', icon='anchor'),
			dac.SidebarMenuItem(id='tab_kpi_value_boxes', label='Info KPI', icon='snowflake'),
            dac.SidebarHeader(children="Product"),
            dac.SidebarMenuItem(id='tab_kpi_product_boxes', label='Product KPI', icon='eye'),
			dac.SidebarHeader(children="Gallery"),
			dac.SidebarMenuItem(label='Galleries', icon='cubes', children=subitems),
		]
	),
    title='Moon Stone',
	skin="light",
    color="primary",
	brand_color="primary",
    url="https://kamble.ai",
    src="assets/Kamblelogo.png",
    elevation=3,
    opacity=0.8
)
