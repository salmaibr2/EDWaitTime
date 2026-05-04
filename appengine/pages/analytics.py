import dash
from dash import html

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

warning_box_style = {
    "backgroundColor": "#fef9c3",
    "border": "1px solid #fde68a",
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


# ── layout ──
layout = html.Div(
    [
        # Header
        html.H1("Analytics & Results", style={"marginBottom": "0.3rem"}),
        html.P(
            "PATWT-weighted EDA, bottleneck analysis, and model performance — "
            "91,811 ED visits from NHAMCS 2015–2018, 2021–2022 representing ~728M national visits. "
            "2019–2020 are excluded from the analysis due to data quality concerns during the COVID-19 pandemic.",
            style={"color": "#4b5563", "marginTop": 0, "marginBottom": "0.5rem"},
        ),
        html.Hr(),

        # Dataset at a glance
        html.Div(
            [
                html.Div([html.P("91,811", style=stat_number), html.P("ED Visits", style=stat_label)], style=stat_box_style),
                html.Div([html.P("~728M", style=stat_number), html.P("Weighted National Visits", style=stat_label)], style=stat_box_style),
                html.Div([html.P("6 Years", style=stat_number), html.P("2015–18, 2021–22*", style=stat_label)], style=stat_box_style),
                html.Div([html.P("37", style=stat_number), html.P("Features", style=stat_label)], style=stat_box_style),
                html.Div([html.P("0–480 min", style=stat_number), html.P("Wait Time Range", style=stat_label)], style=stat_box_style),
                html.Div([html.P("PATWT", style=stat_number), html.P("Survey Weights Applied", style=stat_label)], style=stat_box_style),
            ],
            style=stat_row_style,
        ),

        # SECTION 1: Wait Time Distribution
        html.H2("1. Wait Time Distribution (Weighted)", style=section_heading_style),

        html.Img(
            src="/assets/waittime_distribution_weighted.png",
            style={"width": "100%", "maxWidth": "800px", "display": "block", "margin": "0 auto"},
        ),
        html.P(
            "Figure 1: PATWT-weighted distribution of ED wait times. Each bin is scaled "
            "by the survey weights so counts reflect national visit volumes.",
            style=fig_caption_style,
        ),

        html.Div(
            [
                html.P(
                    "The PATWT-weighted distribution confirms that the right-skewed shape holds "
                    "at the national population level, not just in the raw sample. The peak sits "
                    "near 0–10 minutes, and the weighted mean is pulled well above the weighted "
                    "median by a long tail of visits exceeding 90 minutes.",
                    style=analysis_text_style,
                ),
                html.P(
                    "Because each NHAMCS record represents thousands of actual visits nationwide "
                    "(PATWT range 40–57,926), unweighted statistics would over-represent large "
                    "urban hospitals sampled at higher rates. All subsequent analyses in this "
                    "dashboard use PATWT-weighted estimates.",
                    style=analysis_text_style,
                ),
            ],
            style=card_style,
        ),

        # SECTION 2: Temporal Patterns
        html.H2("2. Temporal Patterns", style=section_heading_style),

        html.Img(
            src="/assets/waittime_temporal_weighted.png",
            style={"width": "100%", "maxWidth": "900px", "display": "block", "margin": "0 auto"},
        ),
        html.P(
            "Figure 2: PATWT-weighted mean wait time by arrival hour (left) and day of week (right).",
            style=fig_caption_style,
        ),

        html.Div(
            [
                html.P(
                    "Arrival hour is the strongest temporal signal. Weighted mean wait times trough "
                    "in the early morning hours (3–6 AM) and peak in the afternoon and early evening "
                    "(1–8 PM), a pattern that is stable across all six survey years.",
                    style=analysis_text_style,
                ),
                html.P(
                    "Day-of-week effects are smaller but consistent: Monday carries the highest "
                    "weighted mean wait, with weekend days averaging several minutes less. This "
                    "aligns with deferred weekend care presenting on Monday and weekday primary "
                    "care referral patterns.",
                    style=analysis_text_style,
                ),
            ],
            style=card_style,
        ),

        html.Div(
            [
                html.P(
                    "Arrival hour is the single most learnable signal in this dataset. "
                    "A simple hour-median baseline matches complex gradient boosting on MAE.",
                    style={"fontWeight": "600", "margin": "0"},
                ),
            ],
            style=highlight_box_style,
        ),

        # SECTION 3: Triage Breakdown
        html.H2("3. Wait Time by Triage Level (Weighted)", style=section_heading_style),

        html.Img(
            src="/assets/waittime_by_triage_weighted.png",
            style={"width": "100%", "maxWidth": "750px", "display": "block", "margin": "0 auto"},
        ),
        html.P(
            "Figure 3: PATWT-weighted mean wait time and visit share by IMMEDR triage category.",
            style=fig_caption_style,
        ),

        html.Div(
            [
                html.P(
                    "IMMEDR encodes triage urgency: 1 = Immediate, 2 = Emergent, 3 = Urgent, "
                    "4 = Semi-urgent, 5 = Non-urgent. Level 1 (Immediate) patients are seen fastest, "
                    "confirming that priority triage protocols are functioning at the national level.",
                    style=analysis_text_style,
                ),
                html.P(
                    "Level 3 (Urgent) accounts for the largest weighted visit share and shows the "
                    "widest wait time spread. These patients are sick enough to need prompt care but "
                    "are routinely queued behind higher-acuity cases, making them the group most "
                    "sensitive to operational bottlenecks like boarding and bed shortages.",
                    style=analysis_text_style,
                ),
            ],
            style=card_style,
        ),

        # SECTION 4: Bottleneck Analysis
        html.H2("4. Operational Bottleneck Analysis", style=section_heading_style),

        html.Div(
            [
                html.P(
                    "Eleven binary operational flags were tested: BOARD (inpatient boarding), "
                    "OBSCLIN (observation unit placement), ANYIMAGE / MRI / XRAY / CTCONTRAST "
                    "(imaging workload), BEDREG / BEDCZAR / IMBED (bed management programs), "
                    "FASTTRAK (fast-track pathway), and ADMIT (admitted to inpatient).",
                    style=analysis_text_style,
                ),
                html.P(
                    "For each flag, the PATWT-weighted mean wait time is computed separately "
                    "for flag-present and flag-absent visits. The delta (present minus absent) "
                    "estimates the marginal delay associated with each condition at the "
                    "national population level.",
                    style=analysis_text_style,
                ),
            ],
            style=card_style,
        ),

        html.Img(
            src="/assets/bottleneck_delta.png",
            style={"width": "100%", "maxWidth": "800px", "display": "block", "margin": "0 auto"},
        ),
        html.P(
            "Figure 4: PATWT-weighted mean wait delta (flag present minus flag absent, in minutes). "
            "Positive bars indicate conditions associated with longer waits.",
            style=fig_caption_style,
        ),

        html.Div(
            [
                html.Div([
                    html.P("Boarding (BOARD)", style={"fontWeight": "700", "margin": "0 0 0.2rem 0", "color": "#dc2626"}),
                    html.P("+7.7 min weighted delta — largest binary bottleneck. Inpatient-admitted patients "
                           "held in ED beds block capacity for incoming patients, creating a cascade effect "
                           "on all subsequent wait times.", style={"margin": 0, "fontSize": "0.92rem"}),
                ], style={**card_style, "borderLeft": "4px solid #dc2626"}),
                html.Div([
                    html.P("Bed Czar (BEDCZAR)", style={"fontWeight": "700", "margin": "0 0 0.2rem 0", "color": "#ea580c"}),
                    html.P("+6.8 min — bed management coordinators appear at the most congested facilities. "
                           "The association reflects where the program is deployed, not a causal effect of "
                           "the program itself.", style={"margin": 0, "fontSize": "0.92rem"}),
                ], style={**card_style, "borderLeft": "4px solid #ea580c"}),
                html.Div([
                    html.P("Observation Unit (OBSCLIN)", style={"fontWeight": "700", "margin": "0 0 0.2rem 0", "color": "#d97706"}),
                    html.P("+5.0 min — patients placed in observation status consume ED capacity that affects "
                           "throughput for all subsequent arrivals.", style={"margin": 0, "fontSize": "0.92rem"}),
                ], style={**card_style, "borderLeft": "4px solid #d97706"}),
            ],
        ),

        html.Img(
            src="/assets/bottleneck_shap.png",
            style={"width": "100%", "maxWidth": "800px", "display": "block", "margin": "0 auto"},
        ),
        html.P(
            "Figure 5: PATWT-weighted mean |SHAP value| for each operational feature from a "
            "HistGradientBoosting model trained on 2015–2018 and tested on 2022 holdout.",
            style=fig_caption_style,
        ),

        html.Div(
            [
                html.P(
                    "SHAP values from a PATWT-weighted gradient boosting model confirm the "
                    "bottleneck ranking from the raw deltas, while also accounting for feature "
                    "interactions. Fast-track (FASTTRAK) is the highest-impact feature by SHAP "
                    "(mean |SHAP| 1.03), reflecting that its presence strongly predicts reduced "
                    "wait times — evidence that parallel triage pathways are highly effective.",
                    style=analysis_text_style,
                ),
                html.P(
                    "Observation unit (OBSCLIN, 0.95) and bed czar (BEDCZAR, 0.65) rank next, "
                    "followed by boarding (BOARD, 0.56). Imaging flags (ANYIMAGE, MRI, CTCONTRAST) "
                    "have lower SHAP values, suggesting their impact on wait time is mediated "
                    "through other operational conditions rather than being a direct cause.",
                    style=analysis_text_style,
                ),
                html.P(
                    "Note on TOTPROC: the total procedures count has the highest raw SHAP value "
                    "among operational features (1.42 min) — higher than any binary bottleneck flag. "
                    "However, it is excluded from the bottleneck ranking because it is a proxy for "
                    "visit complexity, not an actionable operational lever. More procedures reflect "
                    "sicker patients requiring more care; a hospital cannot reduce procedures to shorten "
                    "waits. Its high SHAP value confirms that visit complexity is a major driver of "
                    "wait time variance, but the levers for improvement lie in the process flags above.",
                    style={**analysis_text_style, "color": "#6b7280", "fontStyle": "italic"},
                ),
            ],
            style=card_style,
        ),

        html.Div(
            [
                html.P(
                    "Fast-track programs have the largest SHAP impact and the only negative delta — "
                    "hospitals with fast-track report shorter waits. Boarding has the largest "
                    "positive delta (+7.7 min). These two interventions should be the primary "
                    "targets for operational improvement.",
                    style={"fontWeight": "600", "margin": "0"},
                ),
            ],
            style=highlight_box_style,
        ),

        # SECTION 5: Operational Features Overview
        html.H2("5. Operational Feature Prevalence & Impact", style=section_heading_style),

        html.Img(
            src="/assets/operational_features_weighted.png",
            style={"width": "100%", "maxWidth": "900px", "display": "block", "margin": "0 auto"},
        ),
        html.P(
            "Figure 6: For each operational flag — PATWT-weighted prevalence (% of visits where "
            "flag = present) and the weighted mean wait split (present vs. absent).",
            style=fig_caption_style,
        ),

        html.Div(
            [
                html.P(
                    "Prevalence matters for prioritization: a bottleneck that adds 10 minutes "
                    "but occurs in only 2% of visits has less total population impact than one "
                    "that adds 5 minutes across 30% of visits. The combined view of prevalence "
                    "and delta identifies which conditions to address first for the greatest "
                    "reduction in national ED wait burden.",
                    style=analysis_text_style,
                ),
            ],
            style=card_style,
        ),

        # SECTION 6: Regional Breakdown
        html.H2("6. Regional Breakdown", style=section_heading_style),

        html.Img(
            src="/assets/waittime_by_region_weighted.png",
            style={"width": "100%", "maxWidth": "800px", "display": "block", "margin": "0 auto"},
        ),
        html.P(
            "Figure 7: PATWT-weighted mean wait time by US census region.",
            style=fig_caption_style,
        ),

        html.Img(
            src="/assets/bottleneck_by_region.png",
            style={"width": "100%", "maxWidth": "900px", "display": "block", "margin": "0 auto"},
        ),
        html.P(
            "Figure 8: Bottleneck delta (minutes) by US census region for each operational flag.",
            style=fig_caption_style,
        ),

        html.Div(
            [
                html.P(
                    "Regional stratification reveals that bottleneck severity is not uniform "
                    "across the US. The Northeast and West show generally higher wait times "
                    "and stronger bottleneck deltas, consistent with higher urban density, "
                    "larger hospital volumes, and greater bed pressure in those regions.",
                    style=analysis_text_style,
                ),
                html.P(
                    "The South has the highest weighted visit share (largest regional population "
                    "in the NHAMCS sample) but a more moderate bottleneck profile. The Midwest "
                    "shows the smallest regional deltas for most flags, suggesting relatively "
                    "better throughput conditions in the sampled facilities.",
                    style=analysis_text_style,
                ),
            ],
            style=card_style,
        ),

        # SECTION 7: Model Results
        html.H2("7. Model Results", style=section_heading_style),

        html.Div(
            [
                html.P(
                    "We trained a PATWT-weighted HistGradientBoosting classifier on arrival-time "
                    "features (triage level, vitals, arrival hour, demographics, region) to predict "
                    "whether a patient will wait more than 30 minutes. Train: 2015–2018. "
                    "Validation: 2021. Holdout: 2022. "
                    "2019–2020 are excluded from the analysis due to data quality concerns during the COVID-19 pandemic.",
                    style=analysis_text_style,
                ),
            ],
            style=card_style,
        ),

        html.Img(
            src="/assets/model_classifier_eval.png",
            style={"width": "100%", "maxWidth": "850px", "display": "block", "margin": "0 auto"},
        ),
        html.P(
            "Figure 9: ROC curve and precision-recall curve on the 2022 holdout set.",
            style=fig_caption_style,
        ),

        # Model results table
        html.Div(
            html.Table(
                [
                    html.Thead(html.Tr([
                        html.Th("Task", style=model_table_header),
                        html.Th("Model", style=model_table_header),
                        html.Th("Metric", style={**model_table_header, "textAlign": "center"}),
                        html.Th("Value", style={**model_table_header, "textAlign": "center"}),
                        html.Th("Holdout Year", style={**model_table_header, "textAlign": "center"}),
                    ])),
                    html.Tbody([
                        html.Tr([
                            html.Td("Classification (wait >30 min)", style=model_table_cell),
                            html.Td("Weighted HGB Classifier", style=model_table_cell),
                            html.Td("AUC-ROC", style=model_table_cell_center),
                            html.Td("0.581", style=best_cell),
                            html.Td("2022", style=model_table_cell_center),
                        ], style={"backgroundColor": "#f0fdf4"}),
                        html.Tr([
                            html.Td("Classification (wait >30 min)", style=model_table_cell),
                            html.Td("Weighted HGB Classifier", style=model_table_cell),
                            html.Td("Avg Precision", style=model_table_cell_center),
                            html.Td("0.376", style=model_table_cell_center),
                            html.Td("2022", style=model_table_cell_center),
                        ]),
                        html.Tr([
                            html.Td("Regression (wait time, min)", style=model_table_cell),
                            html.Td("Weighted HGB Regressor (log1p)", style=model_table_cell),
                            html.Td("Weighted MAE", style=model_table_cell_center),
                            html.Td("29.6 min", style=model_table_cell_center),
                            html.Td("2022", style=model_table_cell_center),
                        ], style={"backgroundColor": "#f0fdf4"}),
                        html.Tr([
                            html.Td("Regression (wait time, min)", style=model_table_cell),
                            html.Td("Weighted HGB Regressor (log1p)", style=model_table_cell),
                            html.Td("Weighted R²", style=model_table_cell_center),
                            html.Td("−0.12", style=model_table_cell_center),
                            html.Td("2022", style=model_table_cell_center),
                        ]),
                        html.Tr([
                            html.Td("Baseline", style=model_table_cell),
                            html.Td("Hour-median (arrival hour only)", style=model_table_cell),
                            html.Td("Weighted MAE", style=model_table_cell_center),
                            html.Td("28.3 min", style=model_table_cell_center),
                            html.Td("2022", style=model_table_cell_center),
                        ], style={"backgroundColor": "#f0fdf4"}),
                    ]),
                ],
                style={"width": "100%", "borderCollapse": "collapse"},
            ),
            style={**card_style, "overflowX": "auto"},
        ),

        html.Div(
            [
                html.P(
                    "The negative R² on regression is expected, not a modeling failure. "
                    "Individual wait time is driven by real-time hospital state (bed occupancy, "
                    "staffing ratios, current census) that is absent from retrospective survey data. "
                    "The hour-median baseline matches complex gradient boosting on MAE because "
                    "arrival hour captures nearly all learnable signal in the available features.",
                    style=analysis_text_style,
                ),
                html.P(
                    "The AUC-ROC of 0.581 for the >30 min classifier is modest but meaningful: "
                    "it outperforms random assignment (0.50) and provides actionable risk stratification "
                    "for triage support when combined with arrival-time triage scores.",
                    style=analysis_text_style,
                ),
            ],
            style=card_style,
        ),

        html.Div(
            [
                html.P(
                    "Key limitation: NHAMCS contains no hospital identifier. All models learn "
                    "national-level patterns. A hospital deploying these models would need to "
                    "recalibrate on its own historical data to account for facility-specific "
                    "capacity and patient mix.",
                    style={"fontWeight": "600", "margin": "0"},
                ),
            ],
            style=warning_box_style,
        ),

        html.Img(
            src="/assets/model_feature_importance.png",
            style={"width": "100%", "maxWidth": "800px", "display": "block", "margin": "0 auto"},
        ),
        html.P(
            "Figure 10: PATWT-weighted permutation importance (mean decrease in AUC-ROC) "
            "for the arrival-time classifier on the 2022 holdout.",
            style=fig_caption_style,
        ),

        html.Img(
            src="/assets/model_risk_profiles.png",
            style={"width": "100%", "maxWidth": "900px", "display": "block", "margin": "0 auto"},
        ),
        html.P(
            "Figure 11: Predicted probability of wait >30 min by triage level (left), "
            "arrival hour (center), and US census region (right).",
            style=fig_caption_style,
        ),

        html.Div(
            [
                html.P(
                    "Risk profiles confirm the operational story: Immediate (level 1) triage "
                    "has the lowest predicted probability of a long wait. Afternoon/evening "
                    "arrivals face the highest risk across all triage levels. Regional risk "
                    "variation aligns with the bottleneck severity differences observed in "
                    "the regional bottleneck analysis.",
                    style=analysis_text_style,
                ),
            ],
            style=card_style,
        ),

        # SECTION 8: Recommendations
        html.H2("8. Operational Recommendations", style=section_heading_style),

        html.Div(
            [
                html.H4("Highest-impact interventions", style={"marginBottom": "0.3rem", "color": "#1e40af"}),
                html.Ul([
                    html.Li(
                        "Expand fast-track capacity: fast-track is the strongest protective factor "
                        "(SHAP 1.03). Parallel pathways for lower-acuity patients directly reduce "
                        "congestion for higher-acuity queues."
                    ),
                    html.Li(
                        "Reduce inpatient boarding: boarding adds +7.7 min per affected visit. "
                        "Surge protocols that pull admitted patients to hallway inpatient beds "
                        "within 2 hours of admission order have shown effectiveness in prior research."
                    ),
                    html.Li(
                        "Accelerate observation unit throughput: the +5.0 min obs unit delta "
                        "reflects capacity consumed by long-stay obs patients. Daily discharge "
                        "rounds before 10 AM can release beds before afternoon peak volume."
                    ),
                    html.Li(
                        "Increase afternoon/evening staffing: 1–8 PM is consistently the highest-wait "
                        "window across all years and regions. Shift overlap during this window "
                        "provides the highest marginal return on staffing investment."
                    ),
                ]),
            ],
            style=card_style,
        ),
        html.Div(
            [
                html.H4("For future analysis", style={"marginBottom": "0.3rem", "color": "#1e40af"}),
                html.Ul([
                    html.Li(
                        "Integrate real-time ED census data (current boarding count, occupied beds, "
                        "patients in waiting room) to cross the accuracy ceiling that retrospective "
                        "survey data cannot overcome."
                    ),
                    html.Li(
                        "Apply facility-level random effects to account for between-hospital variance "
                        "that is currently absorbed into noise."
                    ),
                    html.Li(
                        "Conduct sub-group bottleneck analysis by triage level to identify whether "
                        "boarding disproportionately affects urgent vs. non-urgent patients."
                    ),
                ]),
            ],
            style=card_style,
        ),
    ],
    style=container_style,
)
