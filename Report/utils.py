from dash import html, dcc

def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.A(
                        html.Img(
                            src=app.get_asset_url("assets/Kamblelogo.png"),
                            className="logo",
                        ),
                        href="https://kamble.ai",
                    ),
                    html.A(
                        html.Button(
                            "About",
                            id="learn-more-button",
                            style={"margin-left": "-10px"},
                        ),
                        href="https://kamble.ai/about/",
                    ),
                    html.A(
                        html.Button("Source Code", id="learn-more-button"),
                        href="https://github.com/kamble/MoonStone",
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("Moon Stone - Data Playground")],
                        className="seven columns main-title",
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                "Full View",
                                href="/Report/full-view",
                                className="full-view-link",
                            )
                        ],
                        className="five columns",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Overview",
                href="/Report/overview",
                className="tab first",
            ),
            dcc.Link(
                "Price Performance",
                href="/Report/price-performance",
                className="tab",
            ),
            dcc.Link(
                "Portfolio & Management",
                href="/Report/portfolio-management",
                className="tab",
            ),
            dcc.Link(
                "Fees & Minimums", href="/Report/fees", className="tab"
            ),
            dcc.Link(
                "Distributions",
                href="/Report/distributions",
                className="tab",
            ),
            dcc.Link(
                "News & Reviews",
                href="/Report/news-and-reviews",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table
