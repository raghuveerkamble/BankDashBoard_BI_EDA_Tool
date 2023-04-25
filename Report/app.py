# -*- coding: utf-8 -*-
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from pages import (
    overview,
    pricePerformance,
    portfolioManagement,
    feesMins,
    distributions,
    newsReviews,
)

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Financial Report"
server = app.server

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/Report/price-performance":
        return pricePerformance.create_layout(app)
    elif pathname == "/Report/portfolio-management":
        return portfolioManagement.create_layout(app)
    elif pathname == "/Report/fees":
        return feesMins.create_layout(app)
    elif pathname == "/Report/distributions":
        return distributions.create_layout(app)
    elif pathname == "/Report/news-and-reviews":
        return newsReviews.create_layout(app)
    elif pathname == "/Report/full-view":
        return (
            overview.create_layout(app),
            pricePerformance.create_layout(app),
            portfolioManagement.create_layout(app),
            feesMins.create_layout(app),
            distributions.create_layout(app),
            newsReviews.create_layout(app),
        )
    else:
        return overview.create_layout(app)


if __name__ == "__main__":
    app.run_server(debug=False)
