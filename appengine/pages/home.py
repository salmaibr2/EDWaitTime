import dash
from dash import html

dash.register_page(__name__, path='/')

container_style = {
    "maxWidth": "980px",
    "margin": "0 auto",
    "padding": "2rem 1.2rem 3rem 1.2rem",
    "fontFamily": "Arial, sans-serif",
    "lineHeight": "1.6",
}

card_style = {
    "backgroundColor": "#f8f9fb",
    "border": "1px solid #e6e8ef",
    "borderRadius": "10px",
    "padding": "1rem 1.1rem",
    "marginBottom": "0.9rem",
}

layout = html.Div(
    [
        html.H1("ED Wait Time Prediction Project", style={"marginBottom": "0.4rem"}),
        html.P(
            "A predictive analytics project focused on understanding and reducing emergency department delays.",
            style={"color": "#4b5563", "marginTop": 0},
        ),
        html.Hr(),
        html.Div(
            [
                html.H3("What this project entails"),
                html.P(
                    "We use CDC NHAMCS emergency department data to analyze patterns in patient wait time and total visit length, then build machine learning models to predict delays at the point of arrival."
                ),
                html.P(
                    "The goal is to support smarter staffing and resource allocation by identifying when congestion is likely and which factors contribute most to delays."
                ),
            ],
            style=card_style,
        ),
        html.Div(
            [
                html.H3("Core objectives"),
                html.Ul(
                    [
                        html.Li("Predict ED wait time and length of stay using arrival-time information."),
                        html.Li("Identify time-based congestion patterns across hours and weekdays."),
                        html.Li("Measure how clinical complexity and diagnostics affect delays."),
                        html.Li("Evaluate demographic and operational factors associated with wait differences."),
                    ]
                ),
            ],
            style=card_style,
        ),
        html.Div(
            [
                html.H3("Why it matters"),
                html.P(
                    "Reducing avoidable wait times can improve patient outcomes, reduce left-without-being-seen risk, and lower pressure on ED staff. This project aims to turn ED data into practical decision support for hospital operations."
                ),
            ],
            style=card_style,
        ),
    ],
    style=container_style,
)