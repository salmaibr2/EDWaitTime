import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os
from io import StringIO
from google.cloud import storage

dash.register_page(__name__)

# ── styles ──
container_style = {
    "maxWidth": "1100px",
    "margin": "0 auto",
    "padding": "2rem 1.2rem 3rem 1.2rem",
    "fontFamily": "Arial, sans-serif",
    "lineHeight": "1.65",
}

card_style = {
    "backgroundColor": "#f8f9fb",
    "border": "1px solid #e6e8ef",
    "borderRadius": "10px",
    "padding": "1.1rem 1.2rem",
    "marginBottom": "1rem",
}

section_heading_style = {
    "borderLeft": "4px solid #2563eb",
    "paddingLeft": "0.7rem",
    "marginTop": "2rem",
    "marginBottom": "0.7rem",
}

fig_caption_style = {
    "fontSize": "0.85rem",
    "color": "#6b7280",
    "fontStyle": "italic",
    "textAlign": "center",
    "marginTop": "0.3rem",
    "marginBottom": "1.5rem",
}

analysis_text_style = {
    "fontSize": "0.95rem",
    "color": "#374151",
    "marginBottom": "0.8rem",
}

stat_row_style = {
    "display": "flex",
    "gap": "0.8rem",
    "flexWrap": "wrap",
    "marginBottom": "1.2rem",
}

stat_box_style = {
    "textAlign": "center",
    "padding": "0.8rem 0.6rem",
    "backgroundColor": "#ffffff",
    "border": "1px solid #e6e8ef",
    "borderRadius": "10px",
    "flex": "1",
    "minWidth": "130px",
}

stat_number = {
    "fontSize": "1.6rem",
    "fontWeight": "700",
    "color": "#2563eb",
    "margin": "0",
}

stat_label = {
    "fontSize": "0.78rem",
    "color": "#6b7280",
    "margin": "0.15rem 0 0 0",
}

highlight_box_style = {
    "backgroundColor": "#eff6ff",
    "border": "1px solid #bfdbfe",
    "borderRadius": "8px",
    "padding": "0.8rem 1rem",
    "marginBottom": "0.8rem",
}

model_table_header = {
    "padding": "0.6rem 0.8rem",
    "borderBottom": "2px solid #1e293b",
    "textAlign": "left",
    "fontSize": "0.9rem",
    "fontWeight": "700",
    "backgroundColor": "#f1f5f9",
}

model_table_cell = {
    "padding": "0.5rem 0.8rem",
    "borderBottom": "1px solid #e2e8f0",
    "fontSize": "0.9rem",
}

model_table_cell_center = {
    **model_table_cell,
    "textAlign": "center",
}

best_cell = {
    **model_table_cell_center,
    "fontWeight": "700",
    "color": "#16a34a",
}


# layout
layout = html.Div(
    [
        # Header
        html.H1("Analytics & Results", style={"marginBottom": "0.3rem"}),
        html.P(
            "EDA findings, visualizations, and model performance from 121,026 ED visits (NHAMCS 2015\u20132021).",
            style={"color": "#4b5563", "marginTop": 0, "marginBottom": "0.5rem"},
        ),
        html.Hr(),

        # Dataset at a glance
        html.Div(
            [
                html.Div([html.P("121,026", style=stat_number), html.P("ED Visits", style=stat_label)], style=stat_box_style),
                html.Div([html.P("36", style=stat_number), html.P("Features", style=stat_label)], style=stat_box_style),
                html.Div([html.P("33.3 min", style=stat_number), html.P("Mean Wait", style=stat_label)], style=stat_box_style),
                html.Div([html.P("15.0 min", style=stat_number), html.P("Median Wait", style=stat_label)], style=stat_box_style),
                html.Div([html.P("50.4 min", style=stat_number), html.P("Std Dev", style=stat_label)], style=stat_box_style),
                html.Div([html.P("477 min", style=stat_number), html.P("Max Wait", style=stat_label)], style=stat_box_style),
            ],
            style=stat_row_style,
        ),

       
        # SECTION 1:Wait Time Distribution
        html.H2("1. Wait Time Distribution", style=section_heading_style),

        html.Img(
            src="/assets/waittime_distribution.png",
            style={"width": "100%", "maxWidth": "800px", "display": "block", "margin": "0 auto"},
        ),
        html.P("Figure 1: Distribution of ED wait times capped at the 99th percentile.", style=fig_caption_style),

        html.Div(
            [
                html.P(
                    "The wait time distribution is heavily right-skewed. The tallest bar sits "
                    "near 0\u201310 minutes, with roughly 30,000 visits falling in the shortest bin. "
                    "The KDE curve confirms a sharp peak followed by a long tail that stretches "
                    "past 250 minutes.",
                    style=analysis_text_style,
                ),
                html.P(
                    "The mean (33.3 min) is more than double the median (15.0 min), a classic "
                    "indicator of right skew. In practical terms, half of all patients are seen "
                    "within 15 minutes, but a minority experience very long delays that pull the "
                    "average upward. This skew is a key challenge for predictive modeling because "
                    "models optimized for mean error tend to underpredict the long-tail cases "
                    "that represent the most operationally concerning visits.",
                    style=analysis_text_style,
                ),
            ],
            style=card_style,
        ),

    
        # SECTION 2:  Wait Time by Arrival Hour
        html.H2("2. Wait Time by Arrival Hour", style=section_heading_style),

        html.Img(
            src="/assets/waittime_by_hour.png",
            style={"width": "100%", "maxWidth": "850px", "display": "block", "margin": "0 auto"},
        ),
        html.P("Figure 2: Box plot of wait times across 24 arrival hours.", style=fig_caption_style),

        html.Div(
            [
                html.P(
                    "Arrival hour has a clear, non-linear relationship with wait time. Patients "
                    "arriving between 3\u20138 AM experience the shortest waits, with hourly means "
                    "of 23\u201327 minutes. Wait times rise steadily through the morning and plateau "
                    "during the afternoon and evening (1\u20138 PM), where averages reach 35\u201338 minutes. "
                    "The 6 PM hour has the single highest average at 37.6 minutes.",
                    style=analysis_text_style,
                ),
                html.P(
                    "The box plots also show that outlier density (dots above the whiskers) increases "
                    "substantially during peak hours, meaning not only are typical waits longer, "
                    "but extreme waits become more frequent. Late-night hours (10 PM\u20131 AM) maintain "
                    "moderately elevated waits despite lower volume, likely reflecting overnight "
                    "staffing reductions.",
                    style=analysis_text_style,
                ),
            ],
            style=card_style,
        ),

        html.Div(
            [
                html.P(
                    "\u26a1 Peak congestion window: Arrivals between 1 PM and 8 PM face "
                    "~59% longer waits than early morning arrivals.",
                    style={"fontWeight": "600", "margin": "0"},
                ),
            ],
            style=highlight_box_style,
        ),

        
        # SECTION 3: Wait Time by Triage Level
        html.H2("3. Wait Time by Triage Level (IMMEDR)", style=section_heading_style),

        html.Img(
            src="/assets/waittime_by_triage.png",
            style={"width": "100%", "maxWidth": "750px", "display": "block", "margin": "0 auto"},
        ),
        html.P("Figure 3: Wait time distribution by triage immediacy level.", style=fig_caption_style),

        html.Div(
            [
                html.P(
                    "IMMEDR encodes triage urgency: 1 = Immediate, 2 = Emergent, 3 = Urgent, "
                    "4 = Semi-urgent, 5 = Non-urgent. Values -9 and -8 represent unknown or "
                    "not-recorded triage levels, and 0 and 7 are other coded categories.",
                    style=analysis_text_style,
                ),
                html.P(
                    "Level 1 (Immediate) patients have the lowest median wait and the tightest "
                    "distribution, confirming that true emergencies are prioritized effectively. "
                    "Level 3 (Urgent) patients show the widest spread and some of the longest outliers, "
                    "which makes sense since this is the largest volume category and these patients "
                    "are sick enough to need prompt care but may get queued behind higher-acuity cases.",
                    style=analysis_text_style,
                ),
                html.P(
                    "Interestingly, the unknown triage categories (-9, -8) show wait distributions "
                    "comparable to levels 3\u20134, suggesting that missing triage data does not "
                    "correspond to a distinct patient population in terms of wait experience.",
                    style=analysis_text_style,
                ),
            ],
            style=card_style,
        ),

        
        # SECTION 4: Wait Time by Day of Week

        html.H2("4. Wait Time by Day of Week", style=section_heading_style),

        html.Img(
            src="/assets/waittime_by_day.png",
            style={"width": "100%", "maxWidth": "700px", "display": "block", "margin": "0 auto"},
        ),
        html.P("Figure 4: Average wait time by day of week (1 = Sunday, 7 = Saturday).", style=fig_caption_style),

        html.Div(
            [
                html.P(
                    "Monday (VDAYR = 2) has the highest average wait time at 36.6 minutes and "
                    "the highest patient volume (19,551 visits). Tuesday and Wednesday follow "
                    "at 34.8 and 34.3 minutes respectively. Sunday (30.0 min) and Saturday "
                    "(29.8 min) have the shortest average waits, about 6\u20137 minutes below Monday.",
                    style=analysis_text_style,
                ),
                html.P(
                    "The weekday\u2013weekend gap is consistent across the multi-year dataset, "
                    "suggesting a structural pattern rather than random variation. This likely "
                    "reflects higher weekday volumes driven by patients who delay seeking care "
                    "over the weekend and present on Monday, combined with referral patterns "
                    "from primary care offices that are open on weekdays.",
                    style=analysis_text_style,
                ),
            ],
            style=card_style,
        ),

        
        # SECTION 5: Correlation Heatmap
    
        html.H2("5. Correlation Heatmap", style=section_heading_style),

        html.Img(
            src="/assets/correlation_heatmap.png",
            style={"width": "100%", "maxWidth": "750px", "display": "block", "margin": "0 auto"},
        ),
        html.P("Figure 5: Pearson correlation between numeric features and WAITTIME.", style=fig_caption_style),

        html.Div(
            [
                html.P(
                    "The top row shows the correlation of each variable with WAITTIME. Every "
                    "value is near zero: AGE (r = \u22120.01), PAINSCALE (r = 0.00), BPSYS "
                    "(r = 0.00), PULSE (r = \u22120.01), and even ARRIVAL_HOUR (r = 0.06). "
                    "No single patient-level feature explains meaningful variance in wait time.",
                    style=analysis_text_style,
                ),
                html.P(
                    "The heatmap does reveal strong intercorrelations among clinical variables: "
                    "BPSYS and BPDIAS (r = 0.81), TEMPF and RESPR (r = 0.29), PULSE and RESPR "
                    "(r = 0.38). These reflect normal physiological relationships but do not "
                    "translate into wait time predictive power.",
                    style=analysis_text_style,
                ),
                html.P(
                    "This is a critical finding: it confirms that ED wait times are driven by "
                    "system-level factors (patient volume, staffing, bed availability) rather "
                    "than by individual patient characteristics. Any predictive model relying "
                    "solely on patient-level features will face a fundamental ceiling on accuracy.",
                    style=analysis_text_style,
                ),
            ],
            style=card_style,
        ),

        html.Div(
            [
                html.P(
                    "\U0001f50d Key takeaway: Patient demographics and clinical variables have "
                    "near-zero correlation with wait time. Delays are system-driven, not patient-driven.",
                    style={"fontWeight": "600", "margin": "0"},
                ),
            ],
            style=highlight_box_style,
        ),

        
        # SECTION 6: Model Performance
        
        html.H2("6. Model Performance", style=section_heading_style),

        html.Div(
            [
                html.P(
                    "We evaluated six models across three modeling strategies on a held-out test set:",
                    style=analysis_text_style,
                ),
                html.Ul(
                    [
                        html.Li("Arrival-only with residual correction (Residual HGB, Hour-Median)"),
                        html.Li("Segmented by triage level (Segmented HGB by IMMEDR, Hour-Median)"),
                        html.Li("Retrospective with post-visit variables (Linear Regression, Hour-Median)"),
                    ],
                    style={"fontSize": "0.9rem", "marginBottom": "0.8rem"},
                ),
            ],
            style=card_style,
        ),

        html.Img(
            src="/assets/model_comparison.png",
            style={"width": "100%", "maxWidth": "850px", "display": "block", "margin": "0 auto"},
        ),
        html.P("Figure 6: Holdout MAE comparison across all model paths.", style=fig_caption_style),

        # Model results table
        html.Div(
            html.Table(
                [
                    html.Thead(html.Tr([
                        html.Th("Model", style=model_table_header),
                        html.Th("Strategy", style=model_table_header),
                        html.Th("MAE (min)", style={**model_table_header, "textAlign": "center"}),
                        html.Th("RMSE (min)", style={**model_table_header, "textAlign": "center"}),
                        html.Th("R\u00b2", style={**model_table_header, "textAlign": "center"}),
                    ])),
                    html.Tbody([
                        html.Tr([
                            html.Td("Residual HGB", style=model_table_cell),
                            html.Td("Arrival + Residual", style=model_table_cell),
                            html.Td("28.34", style=best_cell),
                            html.Td("55.91", style=model_table_cell_center),
                            html.Td("\u22120.097", style=model_table_cell_center),
                        ], style={"backgroundColor": "#f0fdf4"}),
                        html.Tr([
                            html.Td("Hour-Median (Trainfit)", style=model_table_cell),
                            html.Td("Arrival + Residual", style=model_table_cell),
                            html.Td("28.34", style=best_cell),
                            html.Td("56.00", style=model_table_cell_center),
                            html.Td("\u22120.100", style=model_table_cell_center),
                        ]),
                        html.Tr([
                            html.Td("Segmented HGB by IMMEDR", style=model_table_cell),
                            html.Td("Segmented", style=model_table_cell),
                            html.Td("28.36", style=best_cell),
                            html.Td("55.81", style=model_table_cell_center),
                            html.Td("\u22120.093", style=model_table_cell_center),
                        ], style={"backgroundColor": "#f0fdf4"}),
                        html.Tr([
                            html.Td("Hour-Median (Trainfit)", style=model_table_cell),
                            html.Td("Segmented", style=model_table_cell),
                            html.Td("28.34", style=best_cell),
                            html.Td("56.00", style=model_table_cell_center),
                            html.Td("\u22120.100", style=model_table_cell_center),
                        ]),
                        html.Tr([
                            html.Td("Hour-Median (Trainfit)", style=model_table_cell),
                            html.Td("Retrospective", style=model_table_cell),
                            html.Td("28.34", style=best_cell),
                            html.Td("56.00", style=model_table_cell_center),
                            html.Td("\u22120.100", style=model_table_cell_center),
                        ], style={"backgroundColor": "#f0fdf4"}),
                        html.Tr([
                            html.Td("Linear Regression", style=model_table_cell),
                            html.Td("Retrospective", style=model_table_cell),
                            html.Td("34.49", style=model_table_cell_center),
                            html.Td("53.48", style={**model_table_cell_center, "fontWeight": "700", "color": "#16a34a"}),
                            html.Td("\u22120.004", style={**model_table_cell_center, "fontWeight": "700", "color": "#16a34a"}),
                        ]),
                    ]),
                ],
                style={"width": "100%", "borderCollapse": "collapse"},
            ),
            style={**card_style, "overflowX": "auto"},
        ),

        html.Div(
            [
                html.P(
                    "The tree-based models (Residual HGB, Segmented HGB) and hour-median baseline "
                    "all achieve an MAE of ~28.3 minutes, meaning the average prediction is off by "
                    "about 28 minutes. Linear regression has a notably higher MAE of 34.5 minutes, "
                    "confirming that the relationship between features and wait time is non-linear.",
                    style=analysis_text_style,
                ),
                html.P(
                    "However, all models produce negative R\u00b2 values on the holdout set. A negative "
                    "R\u00b2 means the model\u2019s predictions are worse than simply predicting the mean "
                    "wait time for every patient. This is not a failure of the algorithms but rather "
                    "reflects the fundamental difficulty of the problem: wait time variance is driven "
                    "by real-time factors (current patient volume, staffing, bed occupancy) that are "
                    "not captured in retrospective survey data.",
                    style=analysis_text_style,
                ),
                html.P(
                    "An important finding is that the simple hour-median model (predicting the historical "
                    "median wait for each arrival hour) performs nearly identically to complex gradient "
                    "boosting models. This suggests that arrival hour captures most of the learnable "
                    "signal in the available features, and adding patient-level variables provides "
                    "minimal additional predictive power.",
                    style=analysis_text_style,
                ),
            ],
            style=card_style,
        ),

    
        # SECTION 7: Next Steps
        
        html.H2("7. Next Steps", style=section_heading_style),

        html.Div(
            [
                html.H4("For hospitals", style={"marginBottom": "0.3rem", "color": "#1e40af"}),
                html.Ul([
                    html.Li(
                        "Increase staffing coverage between 10 AM and 8 PM, particularly on Mondays, "
                        "when both volume and wait times peak."
                    ),
                    html.Li(
                        "Post historical median wait times by hour as patient-facing estimates. "
                        "Our analysis shows this simple approach is as accurate as complex ML models."
                    ),
                    html.Li(
                        "Investigate why Monday has the highest volume and wait time. Deferred weekend "
                        "care and primary care referral patterns are likely contributing factors."
                    ),
                ]),
            ],
            style=card_style,
        ),
        html.Div(
            [
                html.H4("For future research", style={"marginBottom": "0.3rem", "color": "#1e40af"}),
                html.Ul([
                    html.Li(
                        "Incorporate real-time operational data (current census, staffing ratios, "
                        "bed occupancy) to break through the accuracy ceiling of retrospective features."
                    ),
                    html.Li(
                        "Reframe as classification: predicting whether wait exceeds 30 or 60 minutes "
                        "may yield more actionable and accurate results than continuous regression."
                    ),
                    html.Li(
                        "Apply log transformation to the target variable to reduce the impact of "
                        "extreme outliers on model training."
                    ),
                    html.Li(
                        "Conduct facility-level analysis to test whether the national-level finding "
                        "of no demographic disparities holds at individual hospitals."
                    ),
                ]),
            ],
            style=card_style,
        ),
        html.Div(
            [
                html.H4("Equity considerations", style={"marginBottom": "0.3rem", "color": "#1e40af"}),
                html.P(
                    "The near-zero correlation between patient demographics and wait time is a "
                    "positive finding at the national level, suggesting that NHAMCS-sampled facilities "
                    "are not systematically delaying care based on age, sex, or other characteristics. "
                    "However, this does not rule out disparities at the individual hospital or regional "
                    "level, which warrants further investigation.",
                    style=analysis_text_style,
                ),
            ],
            style=card_style,
        ),
    ],
    style=container_style,
)