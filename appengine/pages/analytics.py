import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
from pathlib import Path
import os
from io import StringIO
from google.cloud import storage

dash.register_page(__name__)

container_style = {
    "maxWidth": "1150px",
    "margin": "0 auto",
    "padding": "2rem 1.2rem 3rem 1.2rem",
    "fontFamily": "Arial, sans-serif",
}

card_style = {
    "backgroundColor": "#f8f9fb",
    "border": "1px solid #e6e8ef",
    "borderRadius": "10px",
    "padding": "1rem 1.1rem",
    "marginBottom": "0.9rem",
}


def _load_eda_dataframe():
    needed_cols = ["WAITTIME", "ARRTIME", "VDAYR", "AGE", "SEX", "IMMEDR"]

    bucket_name = os.environ.get("BUCKET_NAME")
    csv_blob = os.environ.get("EDA_CSV_BLOB", "processed/eda_df.csv")

    if bucket_name:
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(csv_blob)
            csv_text = blob.download_as_text()
            df = pd.read_csv(StringIO(csv_text))
            df.columns = [str(c).upper() for c in df.columns]
            existing_cols = [col for col in needed_cols if col in df.columns]
            if not existing_cols:
                return pd.DataFrame(), "CSV loaded from GCS but missing required columns for EDA visuals."
            return df[existing_cols].copy(), f"Loaded from gs://{bucket_name}/{csv_blob}"
        except Exception as exc:
            gcs_error = f"Could not load CSV from gs://{bucket_name}/{csv_blob} ({exc})."
        else:
            gcs_error = None
    else:
        gcs_error = "BUCKET_NAME not set."

    local_csv = Path(__file__).resolve().parents[2] / "data" / "eda_df.csv"
    if local_csv.exists():
        try:
            df = pd.read_csv(local_csv)
            df.columns = [str(c).upper() for c in df.columns]
            existing_cols = [col for col in needed_cols if col in df.columns]
            if not existing_cols:
                return pd.DataFrame(), "Local CSV found but missing required columns for EDA visuals."
            return df[existing_cols].copy(), f"Loaded from local file: {local_csv}"
        except Exception as exc:
            return pd.DataFrame(), f"Found local CSV but could not read it ({exc})."

    return pd.DataFrame(), f"{gcs_error} Local fallback not found at {local_csv}."


def _build_figures(df):
    if df.empty:
        return []

    figures = []

    if "WAITTIME" in df.columns:
        wait_df = df.copy()
        wait_df["WAITTIME"] = pd.to_numeric(wait_df["WAITTIME"], errors="coerce")
        wait_df = wait_df[(wait_df["WAITTIME"].notna()) & (wait_df["WAITTIME"] >= 0) & (wait_df["WAITTIME"] <= 480)]
        if not wait_df.empty:
            fig_wait = px.histogram(
                wait_df,
                x="WAITTIME",
                nbins=40,
                title="Distribution of ED Wait Time (minutes)",
                labels={"WAITTIME": "Wait Time (min)"},
            )
            figures.append(fig_wait)

    if "ARRTIME" in df.columns and "WAITTIME" in df.columns:
        hour_df = df.copy()
        hour_df["ARRTIME"] = pd.to_numeric(hour_df["ARRTIME"], errors="coerce")
        hour_df["WAITTIME"] = pd.to_numeric(hour_df["WAITTIME"], errors="coerce")
        hour_df = hour_df[(hour_df["ARRTIME"].notna()) & (hour_df["WAITTIME"].notna())]
        if not hour_df.empty:
            hour_df["ARR_HOUR"] = (hour_df["ARRTIME"] // 100).astype(int)
            hour_df = hour_df[(hour_df["ARR_HOUR"] >= 0) & (hour_df["ARR_HOUR"] <= 23)]
            by_hour = hour_df.groupby("ARR_HOUR", as_index=False)["WAITTIME"].mean()
            if not by_hour.empty:
                fig_hour = px.line(
                    by_hour,
                    x="ARR_HOUR",
                    y="WAITTIME",
                    markers=True,
                    title="Average Wait Time by Arrival Hour",
                    labels={"ARR_HOUR": "Hour of Day", "WAITTIME": "Avg Wait (min)"},
                )
                figures.append(fig_hour)

    if "VDAYR" in df.columns and "WAITTIME" in df.columns:
        day_df = df.copy()
        day_df["VDAYR"] = pd.to_numeric(day_df["VDAYR"], errors="coerce")
        day_df["WAITTIME"] = pd.to_numeric(day_df["WAITTIME"], errors="coerce")
        day_df = day_df[(day_df["VDAYR"].between(1, 7)) & (day_df["WAITTIME"].notna())]
        if not day_df.empty:
            weekday_map = {
                1: "Sunday",
                2: "Monday",
                3: "Tuesday",
                4: "Wednesday",
                5: "Thursday",
                6: "Friday",
                7: "Saturday",
            }
            day_df["WEEKDAY"] = day_df["VDAYR"].astype(int).map(weekday_map)
            order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
            by_day = day_df.groupby("WEEKDAY", as_index=False)["WAITTIME"].mean()
            by_day["WEEKDAY"] = pd.Categorical(by_day["WEEKDAY"], categories=order, ordered=True)
            by_day = by_day.sort_values("WEEKDAY")
            fig_day = px.bar(
                by_day,
                x="WEEKDAY",
                y="WAITTIME",
                title="Average Wait Time by Day of Week",
                labels={"WEEKDAY": "Day", "WAITTIME": "Avg Wait (min)"},
            )
            figures.append(fig_day)

    return figures[:3]


eda_df, data_note = _load_eda_dataframe()
eda_figures = _build_figures(eda_df)

layout = html.Div(
    [
        html.H1("Analytics Overview", style={"marginBottom": "0.4rem"}),
        html.P(
            "Summary of planned model features, data categories, and selected visuals from EDA.",
            style={"color": "#4b5563", "marginTop": 0},
        ),
        html.Hr(),
        html.Div(
            [
                html.H3("Features we will use"),
                html.Ul(
                    [
                        html.Li("Temporal context: arrival hour, weekday, and seasonality indicators."),
                        html.Li("Patient factors: age, sex, race/ethnicity, and insurance-related fields."),
                        html.Li("Triage and acuity: immediacy level, pain score, and vital sign proxies."),
                        html.Li("Resource demand markers: labs, imaging, procedures, and medication indicators."),
                        html.Li("Operational indicators: boarding, admission pathway, and ED process variables."),
                    ]
                ),
            ],
            style=card_style,
        ),
        html.Div(
            [
                html.H3("Five categories of data"),
                html.Ul(
                    [
                        html.Li("Temporal data (arrival time, wait time, length-of-visit, day/time patterns)"),
                        html.Li("Patient demographics (age, sex, race, ethnicity, insurance/payor profile)"),
                        html.Li("Clinical data (triage urgency, vitals, pain, diagnoses, injury context)"),
                        html.Li("Resource utilization (labs, imaging, medications, and procedures)"),
                        html.Li("Hospital operations (boarding, fast-track/observation, triage workflow)"),
                    ]
                ),
            ],
            style=card_style,
        ),
        html.Div(
            [
                html.H3("EDA visuals"),
                html.P(
                    "The charts below are generated from your exported EDA CSV (GCS first, local fallback second).",
                    style={"marginTop": "0.3rem"},
                ),
                html.P(data_note, style={"color": "#b45309"}) if data_note else html.Div(),
            ],
            style=card_style,
        ),
        html.Div(
            [
                dcc.Graph(figure=fig, style={"marginBottom": "1rem"})
                for fig in eda_figures
            ]
            if eda_figures
            else [
                html.Div(
                    "No EDA charts are currently available. Ensure eda_df.csv exists in GCS (EDA_CSV_BLOB) or at data/eda_df.csv.",
                    style={"padding": "0.5rem 0.2rem", "color": "#6b7280"},
                )
            ]
        ),
    ],
    style=container_style,
)