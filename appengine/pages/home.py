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

highlight_box_style = {
    "backgroundColor": "#eff6ff",
    "border": "1px solid #bfdbfe",
    "borderRadius": "8px",
    "padding": "0.8rem 1rem",
    "marginBottom": "0.8rem",
}

layout = html.Div(
    [
        html.H1("ED Bottleneck Analysis Project", style={"marginBottom": "0.4rem"}),
        html.P(
            "Identifying operational bottlenecks that drive emergency department wait times — "
            "so hospitals can better target staffing and resource allocation.",
            style={"color": "#4b5563", "marginTop": 0},
        ),
        html.Hr(),

        # Key stats banner
        html.Div(
            [
                html.Div([html.P("91,811", style=stat_number_style), html.P("ED Visits Analyzed", style=stat_label_style)], style=stat_box_style),
                html.Div([html.P("~728M", style=stat_number_style), html.P("Weighted National Visits", style=stat_label_style)], style=stat_box_style),
                html.Div([html.P("6 Years", style=stat_number_style), html.P("2015–2022 (NHAMCS)", style=stat_label_style)], style=stat_box_style),
                html.Div([html.P("0.581", style=stat_number_style), html.P("Classifier AUC-ROC", style=stat_label_style)], style=stat_box_style),
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
                html.H3("What this project does"),
                html.P(
                    "We use CDC NHAMCS emergency department survey data (2015–2022) to identify "
                    "which operational conditions — boarding, observation units, imaging workload, "
                    "bed management — are most associated with elevated patient wait times. "
                    "The 91,811 cleaned visit records carry PATWT survey weights, so all estimates "
                    "represent the full national ED population (~728 million weighted visits)."
                ),
                html.P(
                    "The primary goal is not to predict any individual patient's wait time — "
                    "that is not achievable from retrospective survey data without real-time "
                    "operational context. Instead, the goal is to rank bottlenecks by their "
                    "population-level impact, enabling hospital administrators to prioritize "
                    "interventions with the highest expected payoff."
                ),
            ],
            style=card_style,
        ),
        html.Div(
            [
                html.H3("Core objectives"),
                html.Ul(
                    [
                        html.Li("Rank operational bottlenecks (boarding, obs units, bed management, imaging) by their weighted impact on wait time."),
                        html.Li("Compare bottleneck severity across US census regions to surface geographic variation."),
                        html.Li("Build a PATWT-weighted risk classifier to flag visits likely to wait >30 minutes based on arrival-time information."),
                        html.Li("Validate that temporal patterns (peak hours, day-of-week) are the strongest learnable signal in this dataset."),
                        html.Li("Produce actionable staffing recommendations grounded in nationally representative population estimates."),
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
                            "Boarding is the single largest binary bottleneck: visits where patients are "
                            "held pending inpatient admission wait +7.7 minutes longer on average than non-boarded visits."
                        ),
                        html.Li(
                            "Bed czar programs are associated with +6.8 min longer waits — counter-intuitive "
                            "because these programs appear at the most congested facilities, not because "
                            "the programs cause delays."
                        ),
                        html.Li(
                            "Observation unit placement adds +5.0 min, suggesting these patients consume "
                            "ED capacity that affects throughput for all subsequent arrivals."
                        ),
                        html.Li(
                            "Fast-track is the top SHAP feature (|SHAP| 1.03): its presence strongly "
                            "predicts reduced wait times, confirming that parallel triage pathways work."
                        ),
                        html.Li(
                            "A PATWT-weighted gradient boosting classifier predicts wait >30 min with "
                            "AUC-ROC 0.581 and average precision 0.376 — useful for triage support but "
                            "not a substitute for real-time operational monitoring."
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
                    "turns nationally representative ED data into prioritized, evidence-based "
                    "operational recommendations."
                ),
            ],
            style=card_style,
        ),
        html.Div(
            [
                html.H3("Data source"),
                html.P(
                    "CDC National Hospital Ambulatory Medical Care Survey (NHAMCS), Emergency "
                    "Department component. Survey years 2015–2018, 2021, 2022 (2019–2020 not "
                    "publicly available). 91,811 records after sentinel cleaning and deduplication. "
                    "PATWT survey weights applied throughout all analyses per CDC documentation requirements."
                ),
            ],
            style=card_style,
        ),
    ],
    style=container_style,
)
