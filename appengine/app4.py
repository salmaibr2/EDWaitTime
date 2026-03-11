from dash import Dash, html, dcc, page_container, page_registry

app = Dash(__name__, use_pages=True, pages_folder="pages")
server = app.server


def build_nav_links():
    ordered_pages = sorted(
        page_registry.values(),
        key=lambda page: (0 if page.get("path") == "/" else 1, page.get("name", "")),
    )

    links = []
    for page in ordered_pages:
        links.append(
            dcc.Link(
                page["name"],
                href=page["relative_path"],
                style={
                    "textDecoration": "none",
                    "fontWeight": 600,
                    "color": "#1f2937",
                    "padding": "0.35rem 0.6rem",
                    "border": "1px solid #e5e7eb",
                    "borderRadius": "8px",
                    "backgroundColor": "#ffffff",
                },
            )
        )

    return links


app.layout = html.Div(
    [
        html.Div(
            [
                html.H2("ED Wait Time Dashboard", style={"margin": 0}),
                html.Div(
                    build_nav_links(),
                    style={
                        "display": "flex",
                        "gap": "0.55rem",
                        "flexWrap": "wrap",
                        "marginTop": "0.6rem",
                    },
                ),
            ],
            style={
                "maxWidth": "1150px",
                "margin": "0 auto",
                "padding": "1rem 1.2rem 0.7rem 1.2rem",
                "borderBottom": "1px solid #e5e7eb",
                "fontFamily": "Arial, sans-serif",
            },
        ),
        page_container,
    ]
)


if __name__ == "__main__":
    app.run(debug=True)
