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

stat_box_style = {
    "textAlign": "center",
    "padding": "1rem",
    "backgroundColor": "#ffffff",
    "border": "1px solid #e6e8ef",
    "borderRadius": "10px",
    "flex": "1",
    "minWidth": "140px",
}

stat_number_style = {
    "fontSize": "2rem",
    "fontWeight": "700",
    "color": "#2563eb",
    "margin": "0",
}

stat_label_style = {
    "fontSize": "0.85rem",
    "color": "#6b7280",
    "margin": "0.2rem 0 0 0",
}

layout = html.Div(
    [
        html.H1("ED Wait Time Prediction Project", style={"marginBottom": "0.4rem"}),
        html.P(
            "A predictive analytics project focused on understanding and reducing emergency department delays.",
            style={"color": "#4b5563", "marginTop": 0},
        ),
        html.Hr(),

        # Key stats banner
        html.Div(
            [
                html.Div([html.P("121,026", style=stat_number_style), html.P("ED Visits Analyzed", style=stat_label_style)], style=stat_box_style),
                html.Div([html.P("33.3 min", style=stat_number_style), html.P("Mean Wait Time", style=stat_label_style)], style=stat_box_style),
                html.Div([html.P("15.0 min", style=stat_number_style), html.P("Median Wait Time", style=stat_label_style)], style=stat_box_style),
                html.Div([html.P("2015-2021", style=stat_number_style), html.P("Years Covered", style=stat_label_style)], style=stat_box_style),
            ],
            style={
                "display": "flex",
                "gap": "0.8rem",
                "flexWrap": "wrap",
                "marginBottom": "1.2rem",
            },
        ),

        html.Div(
            [
                html.H3("What this project entails"),
                html.P(
                    "We use CDC NHAMCS emergency department data (2015-2021) to analyze patterns "
                    "in patient wait time and total visit length, then build machine learning models "
                    "to predict delays at the point of arrival. The combined dataset contains 121,026 "
                    "visit records across 36 features spanning temporal, demographic, clinical, "
                    "resource, and operational categories."
                ),
                html.P(
                    "The goal is to support smarter staffing and resource allocation by identifying "
                    "when congestion is likely and which factors contribute most to delays."
                ),
            ],
            style=card_style,
        ),
        html.Div(
            [
                html.H3("Core objectives"),
                html.Ul(
                    [
                        html.Li("Predict ED wait time using arrival-time information (triage level, vitals, arrival hour, demographics)."),
                        html.Li("Identify time-based congestion patterns across hours and weekdays."),
                        html.Li("Measure how clinical complexity and diagnostics affect delays."),
                        html.Li("Evaluate demographic and operational factors associated with wait differences."),
                        html.Li("Compare multiple ML approaches: Gradient Boosting, segmented models, and linear regression."),
                    ]
                ),
            ],
            style=card_style,
        ),
        html.Div(
            [
                html.H3("Key findings"),
                html.Ul(
                    [
                        html.Li(
                            "Temporal patterns are strong: afternoon arrivals (1-8 PM) wait 35-38 minutes on "
                            "average vs. 24-27 minutes for early morning arrivals, a ~59% increase."
                        ),
                        html.Li(
                            "Monday has the highest average wait time (36.6 min) and volume (19,551 visits); "
                            "weekends average 6-7 minutes less."
                        ),
                        html.Li(
                            "Patient demographics and vitals show near-zero correlation with wait time, "
                            "suggesting delays are system-driven, not patient-driven."
                        ),
                        html.Li(
                            "Best models achieve MAE of ~28.3 minutes. Tree-based models outperform linear "
                            "regression on MAE (28.3 vs 34.5 min), but overall R-squared remains negative, "
                            "highlighting the challenge of predicting individual wait times without real-time data."
                        ),
                    ]
                ),
            ],
            style=card_style,
        ),
        html.Div(
            [
                html.H3("Why it matters"),
                html.P(
                    "Every year roughly 3 million patients leave the ED without being seen due to "
                    "long waits, increasing the risk of serious complications. Reducing avoidable "
                    "wait times can improve patient outcomes, reduce left-without-being-seen rates, "
                    "lower staff burnout (affecting over 50% of ED clinicians), and decrease the "
                    "hundreds of thousands of dollars hospitals spend per turnover. This project "
                    "turns ED data into practical decision support for hospital operations."
                ),
            ],
            style=card_style,
        ),
        html.Div(
            [
                html.H3("Data source"),
                html.P(
                    "CDC National Hospital Ambulatory Medical Care Survey (NHAMCS), Emergency "
                    "Department component. Multi-year data from 2015-2021 combined. 121,026 records, "
                    "36 features after preprocessing."
                ),
            ],
            style=card_style,
        ),
    ],
    style=container_style,
)