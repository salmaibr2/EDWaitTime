import dash
from dash import html

dash.register_page(__name__, name="Methods")

container_style = {
    "maxWidth": "980px",
    "margin": "0 auto",
    "padding": "2rem 1.2rem 3rem 1.2rem",
    "fontFamily": "Arial, sans-serif",
    "lineHeight": "1.7",
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

highlight_box_style = {
    "backgroundColor": "#eff6ff",
    "border": "1px solid #bfdbfe",
    "borderRadius": "8px",
    "padding": "0.8rem 1rem",
    "marginBottom": "1rem",
}

warning_box_style = {
    "backgroundColor": "#fef9c3",
    "border": "1px solid #fde68a",
    "borderRadius": "8px",
    "padding": "0.8rem 1rem",
    "marginBottom": "1rem",
}

text_style = {
    "fontSize": "0.95rem",
    "color": "#374151",
    "marginBottom": "0.8rem",
}

layout = html.Div(
    [
        html.H1("Methods", style={"marginBottom": "0.3rem"}),
        html.P(
            "Data source, survey weighting, bottleneck methodology, modeling approach, and limitations.",
            style={"color": "#4b5563", "marginTop": 0},
        ),
        html.Hr(),

        # 1. Data Source
        html.H2("1. Data Source", style=section_heading_style),
        html.Div(
            [
                html.P(
                    "This project uses the CDC National Hospital Ambulatory Medical Care Survey "
                    "(NHAMCS), Emergency Department component. NHAMCS is an annual probability "
                    "sample of patient visits to non-federal, non-institutional general and "
                    "short-stay hospitals in the United States.",
                    style=text_style,
                ),
                html.P(
                    "Six survey years are included: 2015, 2016, 2017, 2018, 2021, and 2022. "
                    "Files for 2019 and 2020 are not publicly available from the CDC. After "
                    "combining all six years and applying sentinel cleaning and deduplication, "
                    "the final dataset contains 91,811 ED visit records across 38 features.",
                    style=text_style,
                ),
                html.Ul([
                    html.Li("Source: CDC NHAMCS ED SAS public use files"),
                    html.Li("Years: 2015–2018, 2021, 2022 (2019–2020 unavailable)"),
                    html.Li("Raw combined shape: 109,760 rows × 1,061 columns"),
                    html.Li("After cleaning and deduplication: 91,811 rows × 38 columns"),
                    html.Li("WAITTIME filtered to 0–480 minutes"),
                ], style={"fontSize": "0.92rem"}),
            ],
            style=card_style,
        ),

        # 2. Survey Weights (PATWT)
        html.H2("2. Survey Weights (PATWT)", style=section_heading_style),
        html.Div(
            [
                html.P(
                    "NHAMCS is a stratified probability sample, not a census. Each visit record "
                    "carries a patient visit weight (PATWT) that represents the number of actual "
                    "ED visits nationwide that the sampled record estimates. For example, a record "
                    "with PATWT = 5,000 means that visit represents approximately 5,000 real visits "
                    "to similar EDs across the US.",
                    style=text_style,
                ),
                html.P(
                    "PATWT values in this dataset range from 40 to 57,926. The 91,811 sampled "
                    "records represent approximately 728 million weighted national ED visits across "
                    "the six survey years. Without applying PATWT, statistics would over-represent "
                    "large urban hospitals (which are sampled at higher rates) and produce biased "
                    "national estimates.",
                    style=text_style,
                ),
            ],
            style=card_style,
        ),
        html.Div(
            [
                html.P(
                    "PATWT is applied throughout all analyses: weighted means in EDA, "
                    "sample_weight in model training, and weighted metrics in model evaluation. "
                    "This is required by CDC documentation for any NHAMCS population estimate.",
                    style={"fontWeight": "600", "margin": "0"},
                ),
            ],
            style=highlight_box_style,
        ),

        # 3. Data Cleaning
        html.H2("3. Data Cleaning", style=section_heading_style),
        html.Div(
            [
                html.P(
                    "NHAMCS encodes missing and not-applicable responses as sentinel values rather "
                    "than true NaN. All sentinel cleaning is performed once in notebook 01_data_prep "
                    "and applies to 29 columns. Downstream notebooks do not repeat this step.",
                    style=text_style,
                ),
                html.Ul([
                    html.Li("Numeric unknowns: −9, −8, −7 → NaN"),
                    html.Li("Categorical not-answered: 8, 9, 98, 99, 998, 999 → NaN (column-specific)"),
                    html.Li(
                        "TEMPF encoding fix: NHAMCS stores temperature as integer×10 "
                        "(e.g., 986 = 98.6°F). Values above 120 are divided by 10. "
                        "Values outside 85–115°F after correction are set to NaN."
                    ),
                    html.Li("WAITTIME filtered to 0–480 minutes (physiological feasibility range)"),
                    html.Li("40 exact duplicate rows removed"),
                    html.Li("SETTYPE excluded — 100% of records are General ED (SETTYPE=3), zero variance"),
                ], style={"fontSize": "0.92rem"}),
            ],
            style=card_style,
        ),

        # 4. Why Individual Prediction Fails
        html.H2("4. Why Individual Wait Time Prediction Fails", style=section_heading_style),
        html.Div(
            [
                html.P(
                    "All regression models trained on this dataset produce negative R² on the "
                    "holdout year — meaning they perform worse than simply predicting the mean "
                    "wait time for every patient. This is not a failure of the algorithms. It "
                    "reflects a fundamental limitation of the data.",
                    style=text_style,
                ),
                html.P(
                    "Individual ED wait time is determined primarily by real-time operational "
                    "state: how many patients are currently in the waiting room, how many beds "
                    "are occupied, how many nurses are on shift right now. None of this "
                    "information exists in a retrospective survey collected weeks after the visit.",
                    style=text_style,
                ),
                html.P(
                    "Patient-level features (age, vitals, triage level, demographics) have "
                    "near-zero Spearman correlation with wait time. Arrival hour is the "
                    "strongest individual predictor — and a simple hour-of-day median baseline "
                    "matches complex gradient boosting on MAE (28.3 min). Adding more features "
                    "provides no additional predictive power.",
                    style=text_style,
                ),
            ],
            style=card_style,
        ),

        html.Div(
            [
                html.P(
                    "Demographics do not drive wait time — and that is a meaningful finding.",
                    style={"fontWeight": "700", "margin": "0 0 0.5rem 0", "fontSize": "1rem"},
                ),
                html.P(
                    "Our initial EDA found that age (r = −0.01), sex (r ≈ 0.00), race, and "
                    "ethnicity all have near-zero correlation with WAITTIME at the national level. "
                    "A patient's demographic profile carries essentially no information about "
                    "how long they will wait.",
                    style={"margin": "0 0 0.5rem 0", "fontSize": "0.93rem"},
                ),
                html.P(
                    "This is an important equity signal: NHAMCS-sampled facilities are not "
                    "systematically delaying care based on who the patient is. Delays are "
                    "system-driven — determined by boarding rates, bed availability, staffing "
                    "levels, and time of day — not by patient demographics. This finding "
                    "redirected the entire project from demographic-based prediction toward "
                    "operational bottleneck identification.",
                    style={"margin": "0", "fontSize": "0.93rem"},
                ),
            ],
            style=highlight_box_style,
        ),

        html.Div(
            [
                html.P(
                    "NHAMCS was designed for population-level estimation of healthcare utilization "
                    "trends, not for training individual-level predictive models. Reframing the "
                    "goal from prediction to bottleneck identification is the appropriate use of this dataset.",
                    style={"fontWeight": "600", "margin": "0"},
                ),
            ],
            style=warning_box_style,
        ),

        # 5. Bottleneck Methodology
        html.H2("5. Bottleneck Identification Methodology", style=section_heading_style),
        html.Div(
            [
                html.P(
                    "Eleven binary operational flags are analyzed as candidate bottlenecks:",
                    style=text_style,
                ),
                html.Ul([
                    html.Li("BOARD — patient held pending inpatient admission (boarding)"),
                    html.Li("OBSCLIN — patient placed in observation unit"),
                    html.Li("FASTTRAK — fast-track parallel triage pathway active"),
                    html.Li("BEDREG, BEDCZAR, IMBED — bed management programs"),
                    html.Li("ANYIMAGE, MRI, XRAY, CTCONTRAST — imaging workload flags"),
                    html.Li("ADMIT — patient admitted to inpatient at end of visit"),
                ], style={"fontSize": "0.92rem", "marginBottom": "0.8rem"}),
                html.P(
                    "For each flag, the PATWT-weighted mean wait time is computed separately "
                    "for flag-present and flag-absent visits. The delta (present minus absent) "
                    "quantifies the marginal delay associated with each condition at the national "
                    "population level. Flags with 1/2 coding are recoded to 0/1 before analysis.",
                    style=text_style,
                ),
                html.P(
                    "SHAP (SHapley Additive exPlanations) values from a PATWT-weighted "
                    "HistGradientBoosting model provide a model-based bottleneck ranking that "
                    "accounts for feature interactions, complementing the raw weighted deltas. "
                    "SHAP is computed using TreeExplainer on a 2,000-row subsample of the "
                    "holdout set, with mean |SHAP| weighted by PATWT.",
                    style=text_style,
                ),
            ],
            style=card_style,
        ),

        # 6. Modeling
        html.H2("6. Modeling Approach", style=section_heading_style),
        html.Div(
            [
                html.H4("Train / validation / holdout split", style={"marginBottom": "0.3rem", "color": "#1e40af"}),
                html.Ul([
                    html.Li("Train: 2015–2018"),
                    html.Li("Validation: 2021"),
                    html.Li("Holdout: 2022 (reported metrics)"),
                ], style={"fontSize": "0.92rem", "marginBottom": "0.8rem"}),
                html.P(
                    "A temporal split is used rather than random split to simulate real-world "
                    "deployment — the model is always evaluated on future data it has never seen.",
                    style=text_style,
                ),

                html.H4("Features (arrival-time only)", style={"marginBottom": "0.3rem", "color": "#1e40af"}),
                html.P(
                    "Only features available at the moment of patient arrival are used in the "
                    "classifier — triage level (IMMEDR), vitals (BPSYS, BPDIAS, TEMPF, PULSE, "
                    "RESPR), demographics (AGE, SEX, RACEUN, ETHUN), arrival hour, day of week, "
                    "month, region, and MSA type. Cyclical encoding (sin/cos) is applied to "
                    "arrival hour and month. IS_PEAK and IS_WEEKEND binary flags are added.",
                    style=text_style,
                ),

                html.H4("Algorithm", style={"marginBottom": "0.3rem", "color": "#1e40af"}),
                html.P(
                    "HistGradientBoostingClassifier (scikit-learn) with PATWT as sample_weight. "
                    "HGB natively handles missing values (NaN imputation is not required). "
                    "The classification threshold is wait > 30 minutes.",
                    style=text_style,
                ),

                html.H4("Feature importance", style={"marginBottom": "0.3rem", "color": "#1e40af"}),
                html.P(
                    "Permutation importance (n_repeats=5, scoring='roc_auc') on a 2,000-row "
                    "PATWT-weighted subsample of the holdout set. HGB does not expose a "
                    "feature_importances_ attribute, so permutation importance is used instead.",
                    style=text_style,
                ),
            ],
            style=card_style,
        ),

        # 7. Limitations
        html.H2("7. Limitations", style=section_heading_style),
        html.Div(
            [
                html.Ul([
                    html.Li(
                        "No hospital identifier: NHAMCS contains no facility-level ID. All models "
                        "learn national-average patterns. A hospital deploying these models would "
                        "need to recalibrate on its own data to account for facility-specific "
                        "capacity and patient mix."
                    ),
                    html.Li(
                        "No real-time operational data: current census, bed occupancy, and staffing "
                        "ratios are absent. These are the primary drivers of individual wait time "
                        "and cannot be recovered from retrospective survey responses."
                    ),
                    html.Li(
                        "Missing years: 2019 and 2020 SAS files are not publicly available. "
                        "The COVID-19 disruption years are therefore excluded from all trend analysis."
                    ),
                    html.Li(
                        "Bottleneck deltas are associative, not causal: facilities with boarding "
                        "or bed czar programs are the most congested facilities to begin with. "
                        "The delta reflects where these conditions appear, not a direct causal effect."
                    ),
                    html.Li(
                        "IMMEDR missing in 20.7% of records: triage level is the strongest "
                        "individual predictor, but missing in a substantial share of visits. "
                        "HGB handles this via NaN splits; results for non-triaged visits "
                        "should be interpreted cautiously."
                    ),
                    html.Li(
                        "Classifier AUC-ROC 0.581: the model outperforms random (0.50) but "
                        "is not precise enough for clinical decision-making without real-time "
                        "operational context."
                    ),
                ], style={"fontSize": "0.92rem"}),
            ],
            style=card_style,
        ),

        # 8. Pipeline
        html.H2("8. Notebook Pipeline", style=section_heading_style),
        html.Div(
            [
                html.Div([
                    html.Span("01_data_prep", style={"fontWeight": "700", "fontFamily": "monospace"}),
                    html.Span(" → Loads all 6 SAS files, applies sentinel cleaning, TEMPF fix, "
                              "deduplication, and saves eda_df.csv, model_A_arrival_dataset.csv, "
                              "model_B_retrospective_dataset.csv", style={"fontSize": "0.9rem"}),
                ], style={"marginBottom": "0.6rem"}),
                html.Div([
                    html.Span("02_weighted_eda", style={"fontWeight": "700", "fontFamily": "monospace"}),
                    html.Span(" → PATWT-weighted descriptive statistics, temporal patterns, "
                              "triage breakdown, operational feature prevalence. Saves EDA plots.",
                              style={"fontSize": "0.9rem"}),
                ], style={"marginBottom": "0.6rem"}),
                html.Div([
                    html.Span("03_bottleneck_analysis", style={"fontWeight": "700", "fontFamily": "monospace"}),
                    html.Span(" → Weighted delta analysis for 11 operational flags, SHAP-based "
                              "bottleneck ranking, regional breakdown. Saves bottleneck CSVs and plots.",
                              style={"fontSize": "0.9rem"}),
                ], style={"marginBottom": "0.6rem"}),
                html.Div([
                    html.Span("04_modeling", style={"fontWeight": "700", "fontFamily": "monospace"}),
                    html.Span(" → PATWT-weighted classifier and regressor, permutation importance, "
                              "risk profiles by triage/hour/region. Saves model eval CSV and plots.",
                              style={"fontSize": "0.9rem"}),
                ]),
            ],
            style=card_style,
        ),
    ],
    style=container_style,
)
