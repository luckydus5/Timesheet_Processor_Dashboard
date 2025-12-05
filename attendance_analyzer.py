#!/usr/bin/env python3
"""
📊 ATTENDANCE ANALYZER - TOP 10 STATISTICS
Analyzes attendance data for overtime, weekend, and daily attendance

Features:
- Processes fingerprint attendance data
- Calculates overtime hours
- Identifies weekend work
- Generates top 10 statistics
- Creates comparison charts

Author: Olivier
Created: December 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st


def load_attendance_file(file_path, file_type="fingerprint"):
    """
    Load attendance file with proper header handling

    Args:
        file_path: Path to Excel file
        file_type: "fingerprint" or "peat" for different file formats

    Returns:
        DataFrame with properly named columns
    """
    try:
        # Read with header at row 2 (0-indexed)
        df = pd.read_excel(file_path, header=2)

        # Clean column names
        df.columns = df.columns.str.strip()

        # Rename columns if needed
        column_mapping = {
            "Date/Time": "DateTime",
            "Comment ": "Comment",
            "VerifyCode": "VerifyCode",
        }
        df.rename(columns=column_mapping, inplace=True)

        # Remove empty rows
        df = df.dropna(subset=["Name", "DateTime"], how="all")

        # Parse DateTime
        df["DateTime"] = pd.to_datetime(df["DateTime"], format="mixed", dayfirst=False)
        df["Date"] = df["DateTime"].dt.date
        df["Time"] = df["DateTime"].dt.time
        df["Year"] = df["DateTime"].dt.year
        df["Month"] = df["DateTime"].dt.month
        df["MonthName"] = df["DateTime"].dt.strftime("%B")
        df["Weekday"] = df["DateTime"].dt.day_name()
        df["IsWeekend"] = df["DateTime"].dt.dayofweek >= 5  # Saturday=5, Sunday=6

        return df

    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None


def calculate_daily_attendance(df):
    """
    Calculate daily attendance metrics per employee

    Returns:
        DataFrame with attendance statistics
    """
    # Group by employee and date
    daily_stats = (
        df.groupby(["Name", "Date"])
        .agg({"DateTime": "count", "Status": lambda x: list(x), "IsWeekend": "first"})
        .reset_index()
    )

    daily_stats.rename(columns={"DateTime": "RecordCount"}, inplace=True)

    # Count attendance days per employee
    attendance_summary = (
        daily_stats.groupby("Name")
        .agg({"Date": "count", "IsWeekend": "sum", "RecordCount": "sum"})
        .reset_index()
    )

    attendance_summary.rename(
        columns={
            "Date": "TotalDaysAttended",
            "IsWeekend": "WeekendDaysWorked",
            "RecordCount": "TotalRecords",
        },
        inplace=True,
    )

    return attendance_summary


def calculate_overtime_hours(df):
    """
    Calculate overtime hours per employee based on check-in/check-out times

    Returns:
        DataFrame with overtime statistics
    """
    # Filter overtime entries
    overtime_entries = df[
        df["Status"].str.contains("OverTime|Overtime", case=False, na=False)
    ]

    # Group by employee and date to calculate daily overtime
    overtime_by_day = []

    for name in overtime_entries["Name"].unique():
        emp_data = overtime_entries[overtime_entries["Name"] == name]

        for date in emp_data["Date"].unique():
            day_data = emp_data[emp_data["Date"] == date].sort_values("DateTime")

            # Find overtime in/out pairs
            ot_in = day_data[day_data["Status"].str.contains("In", case=False)]
            ot_out = day_data[day_data["Status"].str.contains("Out", case=False)]

            # Calculate hours if we have pairs
            total_ot_hours = 0
            for i in range(min(len(ot_in), len(ot_out))):
                time_in = ot_in.iloc[i]["DateTime"]
                time_out = ot_out.iloc[i]["DateTime"]

                if time_out > time_in:
                    hours = (time_out - time_in).total_seconds() / 3600
                    total_ot_hours += hours

            if total_ot_hours > 0:
                overtime_by_day.append(
                    {"Name": name, "Date": date, "OvertimeHours": total_ot_hours}
                )

    if overtime_by_day:
        ot_df = pd.DataFrame(overtime_by_day)

        # Aggregate by employee
        ot_summary = (
            ot_df.groupby("Name")
            .agg({"OvertimeHours": "sum", "Date": "count"})
            .reset_index()
        )

        ot_summary.rename(
            columns={"Date": "OvertimeDays", "OvertimeHours": "TotalOvertimeHours"},
            inplace=True,
        )

        return ot_summary
    else:
        return pd.DataFrame(columns=["Name", "TotalOvertimeHours", "OvertimeDays"])


def calculate_all_metrics(df):
    """
    Calculate all attendance metrics and merge them

    Returns:
        Complete DataFrame with all metrics
    """
    # Get daily attendance metrics
    attendance = calculate_daily_attendance(df)

    # Get overtime metrics
    overtime = calculate_overtime_hours(df)

    # Merge metrics
    if not overtime.empty:
        metrics = attendance.merge(overtime, on="Name", how="left")
    else:
        metrics = attendance.copy()
        metrics["TotalOvertimeHours"] = 0
        metrics["OvertimeDays"] = 0

    # Fill NaN values
    metrics["TotalOvertimeHours"] = metrics["TotalOvertimeHours"].fillna(0)
    metrics["OvertimeDays"] = metrics["OvertimeDays"].fillna(0)

    # Calculate weekday attendance
    metrics["WeekdayDaysWorked"] = (
        metrics["TotalDaysAttended"] - metrics["WeekendDaysWorked"]
    )

    # Sort by total days attended
    metrics = metrics.sort_values("TotalDaysAttended", ascending=False)

    return metrics


def get_top_10_metrics(metrics_df):
    """
    Get top 10 employees for each category

    Returns:
        Dictionary with top 10 DataFrames for each metric
    """
    top_10 = {
        "overtime_hours": metrics_df.nlargest(10, "TotalOvertimeHours")[
            ["Name", "TotalOvertimeHours", "OvertimeDays"]
        ],
        "weekend_work": metrics_df.nlargest(10, "WeekendDaysWorked")[
            ["Name", "WeekendDaysWorked", "TotalDaysAttended"]
        ],
        "daily_attendance": metrics_df.nlargest(10, "TotalDaysAttended")[
            ["Name", "TotalDaysAttended", "TotalRecords"]
        ],
        "total_records": metrics_df.nlargest(10, "TotalRecords")[
            ["Name", "TotalRecords", "TotalDaysAttended"]
        ],
    }

    return top_10


def create_comparison_chart(top_10_dict):
    """
    Create interactive comparison charts for top 10 metrics

    Returns:
        Plotly figure with subplots
    """
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "🏆 Top 10 Overtime Hours",
            "🌅 Top 10 Weekend Workers",
            "📅 Top 10 Daily Attendance",
            "📊 Top 10 Total Records",
        ),
        specs=[[{"type": "bar"}, {"type": "bar"}], [{"type": "bar"}, {"type": "bar"}]],
    )

    # Overtime Hours
    df_ot = top_10_dict["overtime_hours"]
    fig.add_trace(
        go.Bar(
            x=df_ot["Name"],
            y=df_ot["TotalOvertimeHours"],
            name="Overtime Hours",
            marker_color="#FF6B6B",
            text=df_ot["TotalOvertimeHours"].round(1),
            textposition="outside",
        ),
        row=1,
        col=1,
    )

    # Weekend Work
    df_weekend = top_10_dict["weekend_work"]
    fig.add_trace(
        go.Bar(
            x=df_weekend["Name"],
            y=df_weekend["WeekendDaysWorked"],
            name="Weekend Days",
            marker_color="#4ECDC4",
            text=df_weekend["WeekendDaysWorked"],
            textposition="outside",
        ),
        row=1,
        col=2,
    )

    # Daily Attendance
    df_attendance = top_10_dict["daily_attendance"]
    fig.add_trace(
        go.Bar(
            x=df_attendance["Name"],
            y=df_attendance["TotalDaysAttended"],
            name="Days Attended",
            marker_color="#95E1D3",
            text=df_attendance["TotalDaysAttended"],
            textposition="outside",
        ),
        row=2,
        col=1,
    )

    # Total Records
    df_records = top_10_dict["total_records"]
    fig.add_trace(
        go.Bar(
            x=df_records["Name"],
            y=df_records["TotalRecords"],
            name="Total Records",
            marker_color="#F38181",
            text=df_records["TotalRecords"],
            textposition="outside",
        ),
        row=2,
        col=2,
    )

    # Update layout
    fig.update_xaxes(tickangle=-45, row=1, col=1)
    fig.update_xaxes(tickangle=-45, row=1, col=2)
    fig.update_xaxes(tickangle=-45, row=2, col=1)
    fig.update_xaxes(tickangle=-45, row=2, col=2)

    fig.update_layout(
        height=800,
        showlegend=False,
        title_text="📊 Attendance Analysis - Top 10 Performers",
        title_font_size=20,
    )

    return fig


def create_individual_metric_chart(df, metric_name, metric_col, title, color):
    """
    Create individual chart for a specific metric

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["Name"],
            y=df[metric_col],
            text=(
                df[metric_col].round(1)
                if df[metric_col].dtype == "float"
                else df[metric_col]
            ),
            textposition="outside",
            marker_color=color,
            hovertemplate="<b>%{x}</b><br>" + metric_name + ": %{y}<extra></extra>",
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="Employee Name",
        yaxis_title=metric_name,
        xaxis_tickangle=-45,
        height=500,
        showlegend=False,
    )

    return fig


def export_to_excel(metrics_df, top_10_dict, output_file):
    """
    Export all statistics to Excel file with multiple sheets

    Args:
        metrics_df: Complete metrics DataFrame
        top_10_dict: Dictionary of top 10 DataFrames
        output_file: Output file path
    """
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        # Full metrics
        metrics_df.to_excel(writer, sheet_name="All Employees", index=False)

        # Top 10 sheets
        top_10_dict["overtime_hours"].to_excel(
            writer, sheet_name="Top 10 Overtime", index=False
        )
        top_10_dict["weekend_work"].to_excel(
            writer, sheet_name="Top 10 Weekend", index=False
        )
        top_10_dict["daily_attendance"].to_excel(
            writer, sheet_name="Top 10 Attendance", index=False
        )
        top_10_dict["total_records"].to_excel(
            writer, sheet_name="Top 10 Records", index=False
        )


if __name__ == "__main__":
    # Test with command line usage
    import sys

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"Processing {file_path}...")

        df = load_attendance_file(file_path)
        if df is not None:
            print(f"✅ Loaded {len(df)} records")

            metrics = calculate_all_metrics(df)
            print(f"\n📊 Calculated metrics for {len(metrics)} employees")

            top_10 = get_top_10_metrics(metrics)

            print("\n🏆 TOP 10 OVERTIME HOURS:")
            print(top_10["overtime_hours"].to_string(index=False))

            print("\n🌅 TOP 10 WEEKEND WORKERS:")
            print(top_10["weekend_work"].to_string(index=False))

            print("\n📅 TOP 10 DAILY ATTENDANCE:")
            print(top_10["daily_attendance"].to_string(index=False))
    else:
        print("Usage: python attendance_analyzer.py <attendance_file.xlsx>")
