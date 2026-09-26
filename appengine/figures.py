"""
Plotly figure builders for the analytics dashboard.

Place this file at appengine/figures.py, alongside app4.py (not
inside pages/). Each function takes the full dataframe and returns
a ready-to-use plotly Figure. All weighting logic matches the
notebooks (02_weighted_eda.ipynb).
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

REGION_LABELS = {1: "Northeast", 2: "Midwest", 3: "South", 4: "West"}
MSA_LABELS = {1: "Urban (MSA)", 2: "Rural (non-MSA)"}
IMMEDR_LABELS = {
    0: "Not recorded",
    1: "Immediate",
    2: "Emergent",
    3: "Urgent",
    4: "Semi-urgent",
    5: "Non-urgent",
    7: "No triage",
}
VDAYR_LABELS = {1: "Sun", 2: "Mon", 3: "Tue", 4: "Wed", 5: "Thu", 6: "Fri", 7: "Sat"}

OPERATIONAL_FLAGS = [
    ("FASTTRAK", "Fast-track / urgent care ESA"),
    ("OBSCLIN", "Observation / clinical decision unit"),
    ("BOARD", "Patient boarded in ED"),
    ("BEDREG", "Bed request required (bed czar/registry)"),
    ("IMBED", "Immediate bedding used"),
    ("BEDCZAR", "Bed czar / bed management present"),
    ("ANYIMAGE", "Any imaging ordered"),
    ("MRI", "MRI ordered"),
    ("XRAY", "X-ray ordered"),
    ("CTCONTRAST", "CT with contrast ordered"),
]


def wmean(values, weights):
    mask = values.notna() & weights.notna()
    return np.average(values[mask], weights=weights[mask])


def weighted_group_stats(df, groupby_col, value_col="WAITTIME", weight_col="PATWT", label_map=None):
    rows = []
    total_w = df[weight_col].sum()
    for grp, sub in df.groupby(groupby_col, dropna=True):
        v = sub[value_col].dropna()
        w = sub.loc[v.index, weight_col]
        if len(v) < 10:
            continue
        rows.append(
            {
                groupby_col: grp,
                "label": label_map.get(grp, str(grp)) if label_map else str(grp),
                "n_records": len(sub),
                "weighted_share_pct": sub[weight_col].sum() / total_w * 100,
                "weighted_mean_wait": np.average(v, weights=w),
            }
        )
    return pd.DataFrame(rows)


def build_wait_time_distribution(df):
    overall_wmean = wmean(df["WAITTIME"], df["PATWT"])

    bins = np.arange(0, 241, 10)
    unweighted_counts, _ = np.histogram(df["WAITTIME"], bins=bins, density=True)
    weighted_counts, _ = np.histogram(df["WAITTIME"], bins=bins, weights=df["PATWT"], density=True)

    sorted_idx = df["WAITTIME"].argsort()
    vals_sorted = df["WAITTIME"].iloc[sorted_idx].values
    wts_sorted = df["PATWT"].iloc[sorted_idx].values
    cum_wt = np.cumsum(wts_sorted) / wts_sorted.sum()
    pcts = [25, 50, 75, 90, 95]
    pct_vals = [vals_sorted[np.searchsorted(cum_wt, p / 100)] for p in pcts]

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Wait Time Distribution", "Weighted Percentiles"),
        column_widths=[0.6, 0.4],
    )

    fig.add_trace(
        go.Bar(
            x=bins[:-1],
            y=unweighted_counts,
            name="Unweighted",
            marker_color="steelblue",
            opacity=0.6,
            hovertemplate="Wait time: %{x}-%{customdata} min<br>Density: %{y:.4f}<extra>Unweighted</extra>",
            customdata=bins[1:],
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Bar(
            x=bins[:-1],
            y=weighted_counts,
            name="PATWT-weighted",
            marker_color="darkorange",
            opacity=0.6,
            hovertemplate="Wait time: %{x}-%{customdata} min<br>Density: %{y:.4f}<extra>PATWT-weighted</extra>",
            customdata=bins[1:],
        ),
        row=1,
        col=1,
    )
    fig.add_vline(
        x=overall_wmean,
        line_dash="dash",
        line_color="darkorange",
        line_width=1.5,
        annotation_text=f"Weighted mean ({overall_wmean:.0f} min)",
        annotation_position="top right",
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Bar(
            x=pct_vals,
            y=[f"P{p}" for p in pcts],
            orientation="h",
            marker_color="#3b6fa0",
            text=[f"{v:.0f} min" for v in pct_vals],
            textposition="outside",
            hovertemplate="%{y}: %{x:.0f} min<extra></extra>",
            showlegend=False,
        ),
        row=1,
        col=2,
    )

    fig.update_xaxes(range=[bins[0] - 5, bins[-1] + 15], row=1, col=1)
    fig.update_xaxes(range=[0, max(pct_vals) * 1.15], row=1, col=2)
    fig.update_xaxes(title_text="Wait time (minutes)", row=1, col=1)
    fig.update_yaxes(title_text="Density", row=1, col=1)
    fig.update_xaxes(title_text="Wait time (minutes)", row=1, col=2)

    fig.update_layout(
        barmode="overlay",
        title_text="National ED Wait Time, PATWT-Weighted (2015-2022)",
        title_x=0.5,
        title_y=0.97,
        legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="center", x=0.5),
        height=460,
        margin=dict(t=110, b=60, l=60, r=60),
        template="plotly_white",
    )
    return fig


def build_temporal_patterns(df):
    overall_wmean = wmean(df["WAITTIME"], df["PATWT"])

    fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=("By Arrival Hour", "By Day of Week", "By Month"),
    )

    hour_stats = weighted_group_stats(df, "ARRIVAL_HOUR").sort_values("ARRIVAL_HOUR")
    fig.add_trace(
        go.Scatter(
            x=hour_stats["ARRIVAL_HOUR"],
            y=[overall_wmean] * len(hour_stats),
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=hour_stats["ARRIVAL_HOUR"],
            y=hour_stats["weighted_mean_wait"],
            mode="lines+markers",
            name="Weighted mean wait",
            line=dict(color="steelblue", width=2),
            marker=dict(size=6),
            fill="tonexty",
            fillcolor="rgba(70,130,180,0.15)",
            showlegend=False,
            hovertemplate="Hour %{x}: %{y:.1f} min<extra></extra>",
        ),
        row=1,
        col=1,
    )
    fig.add_hline(
        y=overall_wmean,
        line_dash="dash",
        line_color="red",
        opacity=0.6,
        annotation_text="Overall mean",
        annotation_position="top left",
        row=1,
        col=1,
    )

    day_stats = weighted_group_stats(df, "VDAYR", label_map=VDAYR_LABELS).sort_values("VDAYR")
    day_colors = ["#e74c3c" if d in [1, 7] else "steelblue" for d in day_stats["VDAYR"]]
    fig.add_trace(
        go.Bar(
            x=day_stats["label"],
            y=day_stats["weighted_mean_wait"],
            marker_color=day_colors,
            showlegend=False,
            hovertemplate="%{x}: %{y:.1f} min<extra></extra>",
        ),
        row=1,
        col=2,
    )
    fig.add_hline(y=overall_wmean, line_dash="dash", line_color="red", opacity=0.6, row=1, col=2)

    month_stats = weighted_group_stats(df, "VMONTH").sort_values("VMONTH")
    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    fig.add_trace(
        go.Bar(
            x=month_labels[: len(month_stats)],
            y=month_stats["weighted_mean_wait"],
            marker_color="steelblue",
            opacity=0.85,
            showlegend=False,
            hovertemplate="%{x}: %{y:.1f} min<extra></extra>",
        ),
        row=1,
        col=3,
    )
    fig.add_hline(y=overall_wmean, line_dash="dash", line_color="red", opacity=0.6, row=1, col=3)

    fig.update_xaxes(title_text="Arrival Hour", row=1, col=1)
    fig.update_yaxes(title_text="Weighted Mean Wait (min)", row=1, col=1)
    fig.update_xaxes(title_text="Day of Week", row=1, col=2)
    fig.update_xaxes(title_text="Month", row=1, col=3)

    fig.update_layout(
        title_text="Weighted Mean Wait Time by Time Period",
        title_x=0.5,
        title_y=0.97,
        showlegend=False,
        height=440,
        margin=dict(t=90, b=60, l=60, r=40),
        template="plotly_white",
    )
    return fig


def build_triage_level(df):
    overall_wmean = wmean(df["WAITTIME"], df["PATWT"])
    triage_stats = weighted_group_stats(df, "IMMEDR", label_map=IMMEDR_LABELS).sort_values("IMMEDR")

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Mean Wait by Triage Level", "Visit Volume by Triage Level"),
    )

    fig.add_trace(
        go.Bar(
            x=triage_stats["weighted_mean_wait"],
            y=triage_stats["label"],
            orientation="h",
            marker_color="#c0392b",
            text=[f"{v:.1f}" for v in triage_stats["weighted_mean_wait"]],
            textposition="outside",
            showlegend=False,
            hovertemplate="%{y}: %{x:.1f} min<extra></extra>",
        ),
        row=1,
        col=1,
    )
    fig.add_vline(
        x=overall_wmean,
        line_dash="dash",
        line_color="black",
        opacity=0.5,
        annotation_text="Overall mean",
        annotation_position="top right",
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Bar(
            x=triage_stats["weighted_share_pct"],
            y=triage_stats["label"],
            orientation="h",
            marker_color="#2980b9",
            opacity=0.85,
            text=[f"{v:.1f}%" for v in triage_stats["weighted_share_pct"]],
            textposition="outside",
            showlegend=False,
            hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
        ),
        row=1,
        col=2,
    )

    fig.update_xaxes(
        title_text="Weighted Mean Wait (min)",
        range=[0, triage_stats["weighted_mean_wait"].max() * 1.2],
        row=1,
        col=1,
    )
    fig.update_xaxes(
        title_text="Share of Weighted Visits (%)",
        range=[0, triage_stats["weighted_share_pct"].max() * 1.2],
        row=1,
        col=2,
    )

    fig.update_layout(
        title_text="Triage Urgency (IMMEDR), Weighted",
        title_x=0.5,
        height=440,
        margin=dict(t=90, b=60, l=90, r=60),
        template="plotly_white",
    )
    return fig


def build_regional_breakdown(df):
    overall_wmean = wmean(df["WAITTIME"], df["PATWT"])
    region_stats = weighted_group_stats(df, "REGION", label_map=REGION_LABELS)
    msa_stats = weighted_group_stats(df, "MSA", label_map=MSA_LABELS)

    fig = make_subplots(rows=1, cols=2, subplot_titles=("By US Region", "Urban vs Rural (MSA)"))

    region_colors = ["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3"]
    fig.add_trace(
        go.Bar(
            x=region_stats["label"],
            y=region_stats["weighted_mean_wait"],
            marker_color=region_colors[: len(region_stats)],
            text=[f"{v:.1f}" for v in region_stats["weighted_mean_wait"]],
            textposition="outside",
            showlegend=False,
            hovertemplate="%{x}: %{y:.1f} min<extra></extra>",
        ),
        row=1,
        col=1,
    )
    fig.add_hline(
        y=overall_wmean,
        line_dash="dash",
        line_color="red",
        opacity=0.7,
        annotation_text="Overall mean",
        annotation_position="top left",
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Bar(
            x=msa_stats["label"],
            y=msa_stats["weighted_mean_wait"],
            marker_color=["#2980b9", "#e67e22"][: len(msa_stats)],
            text=[f"{v:.1f}" for v in msa_stats["weighted_mean_wait"]],
            textposition="outside",
            showlegend=False,
            hovertemplate="%{x}: %{y:.1f} min<extra></extra>",
        ),
        row=1,
        col=2,
    )
    fig.add_hline(y=overall_wmean, line_dash="dash", line_color="red", opacity=0.7, row=1, col=2)

    y_max = max(region_stats["weighted_mean_wait"].max(), msa_stats["weighted_mean_wait"].max()) * 1.2
    fig.update_yaxes(title_text="Weighted Mean Wait (min)", range=[0, y_max], row=1, col=1)
    fig.update_yaxes(range=[0, y_max], row=1, col=2)

    fig.update_layout(
        title_text="Wait Time by Geography, PATWT-Weighted",
        title_x=0.5,
        height=440,
        margin=dict(t=90, b=60, l=60, r=40),
        template="plotly_white",
    )
    return fig


def build_operational_features(df):
    total_w = df["PATWT"].sum()
    summary_rows = []

    for col, label in OPERATIONAL_FLAGS:
        if col not in df.columns:
            continue
        vals = df[col].dropna().unique()
        if set(vals).issubset({0, 1, 0.0, 1.0}):
            present = df[col] == 1
            absent = df[col] == 0
        else:
            present = df[col] == 1
            absent = df[col] == 2

        pres_sub = df[present]
        abs_sub = df[absent]
        if len(pres_sub) < 10 or len(abs_sub) < 10:
            continue

        pres_wmean = wmean(pres_sub["WAITTIME"], pres_sub["PATWT"])
        abs_wmean = wmean(abs_sub["WAITTIME"], abs_sub["PATWT"])
        pres_share = pres_sub["PATWT"].sum() / total_w * 100

        summary_rows.append(
            {
                "Feature": label,
                "Present_Share_%": round(pres_share, 1),
                "Delta_min": round(pres_wmean - abs_wmean, 1),
            }
        )

    ops_df = pd.DataFrame(summary_rows)
    colors = ["#e74c3c" if d > 0 else "#2ecc71" for d in ops_df["Delta_min"]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=ops_df["Present_Share_%"],
            y=ops_df["Delta_min"],
            mode="markers+text",
            marker=dict(size=14, color=colors, line=dict(width=1, color="white")),
            text=ops_df["Feature"],
            textposition="top center",
            textfont=dict(size=10),
            hovertemplate=(
                "%{text}<br>Present in %{x:.1f}% of visits<br>Delta: %{y:+.1f} min<extra></extra>"
            ),
        )
    )
    fig.add_hline(y=0, line_color="black", line_width=1)
    fig.update_xaxes(title_text="Share of Weighted Visits (%)")
    fig.update_yaxes(title_text="Extra Wait Minutes When Feature Is Present")
    fig.update_layout(
        title_text="Operational Features, Wait Time Impact and Prevalence",
        title_x=0.5,
        height=480,
        margin=dict(t=90, b=60, l=60, r=40),
        template="plotly_white",
    )
    return fig