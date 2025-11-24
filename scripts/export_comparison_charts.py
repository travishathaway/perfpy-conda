#!/usr/bin/env python3
"""
Export conda vs rattler comparison charts to a single HTML file.

This script reads the performance data CSVs and creates an HTML report
with execution time and memory usage comparison charts.
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path


def get_profiled_agg(file):
    """Load and process profiled performance data."""
    # Load the CSV file
    df = pd.read_csv(file)

    # Convert time columns from nanoseconds to seconds for better readability
    df['total_time_sec'] = df['total_time'] / 1e9

    # Convert memory from bytes to MB
    df['max_memory_mb'] = df['max_memory_usage'] / (1024 * 1024)

    # Convert bytes to MB
    df['bytes_recv_mb'] = df['bytes_recv'] / (1024 * 1024)
    df['bytes_sent_mb'] = df['bytes_sent'] / (1024 * 1024)

    # Columns we need for report
    columns = [
        "name",
        "bytes_recv",
        "bytes_sent",
        "user_time",
        "cpu_time",
        "total_time",
        "max_memory_usage",
        "total_time_sec",
        "max_memory_mb",
        "bytes_recv_mb",
        "bytes_sent_mb"
    ]

    return df[columns]


def prepare_comparison_data(conda_csv, rattler_csv):
    """Load and prepare comparison data from both solvers."""
    # Load data
    profiled = get_profiled_agg(conda_csv)
    profiled_rattler = get_profiled_agg(rattler_csv)

    # Aggregate by name
    conda_agg = profiled.groupby("name").mean().reset_index()
    conda_agg['solver'] = 'conda'

    rattler_agg = profiled_rattler.groupby("name").mean().reset_index()
    rattler_agg['solver'] = 'rattler'

    # Combine both datasets
    comparison_df = pd.concat([conda_agg, rattler_agg], ignore_index=True)

    # Filter to only include conda_create commands (exclude clean, set_config)
    comparison_df = comparison_df[comparison_df['name'].str.startswith('conda_create')]

    # Create cleaner labels for the charts
    comparison_df['scenario'] = comparison_df['name'].str.replace('conda_create_', '', regex=False)
    comparison_df['scenario'] = comparison_df['scenario'].str.replace('_', ' ', regex=False).str.title()

    # Add is_sharded column
    comparison_df['is_sharded'] = comparison_df['scenario'].str.contains('Sharded')

    return comparison_df


def time_execution_chart(df, is_sharded: bool = False):
    df = df[df['is_sharded'] == is_sharded]
    title_extra = "(sharded)" if is_sharded else "(not sharded)"
    df['scenario_short'] = df['scenario'].str.replace("Conda Forge", "").str.replace("Sharded", "").str.title()

    fig_time_with_table = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        specs=[[{"type": "bar"}],
               [{"type": "table"}]],
        subplot_titles=(f'Execution Time Comparison: conda vs Rattler {title_extra}', 'Data Summary'),
        vertical_spacing=0.2
    )

    # Add bar chart traces
    conda_data = df[df['solver'] == 'conda']
    rattler_data = df[df['solver'] == 'rattler']

    fig_time_with_table.add_trace(
        go.Bar(name='conda', x=conda_data['scenario_short'], y=conda_data['total_time_sec'],
               marker_color='#43b02a'),
        row=1, col=1
    )

    fig_time_with_table.add_trace(
        go.Bar(name='Rattler', x=rattler_data['scenario_short'], y=rattler_data['total_time_sec'],
               marker_color='#f9c405'),
        row=1, col=1
    )
    # Prepare table data
    table_data = df.pivot(index='scenario_short', columns='solver', values='total_time_sec').reset_index()
    table_data['improvement_%'] = (
                (table_data['rattler'] - table_data['conda']) / table_data['conda'] * 100).round(1)

    # Add table
    fig_time_with_table.add_trace(
        go.Table(
            header=dict(
                values=['<b>Scenario</b>', '<b>conda (sec)</b>', '<b>Rattler (sec)</b>', '<b>Improvement (%)</b>'],
                fill_color='#f0f0f0',
                align='left',
                font=dict(size=12)
            ),
            cells=dict(
                values=[
                    table_data['scenario_short'],
                    table_data['conda'].round(4),
                    table_data['rattler'].round(4),
                    table_data['improvement_%']
                ],
                fill_color='white',
                align='left',
                font=dict(size=11)
            )
        ),
        row=2, col=1
    )

    # Update layout
    fig_time_with_table.update_layout(
        height=800,
        template='plotly_white',
        showlegend=True,
        barmode='group'
    )

    fig_time_with_table.update_xaxes(tickangle=-45, row=1, col=1)
    fig_time_with_table.update_yaxes(title_text="Total Time (seconds)", row=1, col=1)

    return fig_time_with_table


def memory_usage_chart(df, is_sharded: bool = False):
    df = df[df['is_sharded'] == is_sharded]
    title_extra = "(sharded)" if is_sharded else "(not sharded)"
    df['scenario_short'] = df['scenario'].str.replace("Conda Forge", "").str.replace("Sharded", "").str.title()

    fig_time_with_table = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        specs=[[{"type": "bar"}],
               [{"type": "table"}]],
        subplot_titles=(f'Max Memory Usage Comparison: conda vs Rattler {title_extra}', 'Data Summary'),
        vertical_spacing=0.2
    )

    # Add bar chart traces
    conda_data = df[df['solver'] == 'conda']
    rattler_data = df[df['solver'] == 'rattler']

    fig_time_with_table.add_trace(
        go.Bar(name='conda', x=conda_data['scenario_short'], y=conda_data['max_memory_mb'],
               marker_color='#43b02a'),
        row=1, col=1
    )

    fig_time_with_table.add_trace(
        go.Bar(name='Rattler', x=rattler_data['scenario_short'], y=rattler_data['max_memory_mb'],
               marker_color='#f9c405'),
        row=1, col=1
    )
    # Prepare table data
    table_data = df.pivot(index='scenario_short', columns='solver', values='max_memory_mb').reset_index()
    table_data['improvement_%'] = (
                (table_data['rattler'] - table_data['conda']) / table_data['conda'] * 100).round(1)

    # Add table
    fig_time_with_table.add_trace(
        go.Table(
            header=dict(
                values=['<b>Scenario</b>', '<b>conda (MB)</b>', '<b>Rattler (MB)</b>', '<b>Improvement (%)</b>'],
                fill_color='#f0f0f0',
                align='left',
                font=dict(size=12)
            ),
            cells=dict(
                values=[
                    table_data['scenario_short'],
                    table_data['conda'].round(4),
                    table_data['rattler'].round(4),
                    table_data['improvement_%']
                ],
                fill_color='white',
                align='left',
                font=dict(size=11)
            )
        ),
        row=2, col=1
    )

    fig_time_with_table.add_annotation(
        text=(
            "<b>Test Scenarios Explained:</b><br>"
            "• <b>Datascience:</b>fetching repodata for the packages 'pandas', 'plotly' and 'scipy'<br>"
            "• <b>Python:</b>fetching repodata for the 'python' package<br>"
            "• <b>Warm</b> cache is fully loaded with no network requests necessary"
            "• <b>Cold</b> cache is empty requiring network requests"
        ),
        xref="paper", yref="paper",
        x=0.5, y=-3.35,  # Position below the table (negative y for below)
        xanchor="center", yanchor="top",
        showarrow=False,
        align="left",
        font=dict(size=11, color="#000"),
        bgcolor="#f8f9fa",
        bordercolor="#dee2e6",
        borderwidth=1,
        borderpad=10
    )

    # Update layout
    fig_time_with_table.update_layout(
        height=800,
        template='plotly_white',
        showlegend=True,
        barmode='group',
    )

    fig_time_with_table.update_xaxes(tickangle=-45, row=1, col=1)
    fig_time_with_table.update_yaxes(title_text="Max Memory Usage (MBs)", row=1, col=1)

    return fig_time_with_table


def main():
    """Main execution function."""
    # Define paths
    base_dir = Path(__file__).parent.parent
    conda_csv = base_dir / 'data' / 'sharded_repodata_performance_2025-11-24.csv'
    rattler_csv = base_dir / 'data' / 'sharded_repodata_performance_rattler_2025-11-24.csv'
    output_html = base_dir / 'exports' / 'comparison_report.html'

    # Create exports directory if it doesn't exist
    output_html.parent.mkdir(exist_ok=True)

    print(f"Loading data from:")
    print(f"  - {conda_csv}")
    print(f"  - {rattler_csv}")

    # Prepare data
    comparison_df = prepare_comparison_data(conda_csv, rattler_csv)
    print(f"\nProcessed {len(comparison_df)} rows")

    # Create combined chart
    print("Creating charts...")
    fig_1 = time_execution_chart(comparison_df, is_sharded=False)
    fig_2 = time_execution_chart(comparison_df, is_sharded=True)
    fig_3 = memory_usage_chart(comparison_df, is_sharded=True)
    fig_4 = memory_usage_chart(comparison_df, is_sharded=False)

    # Export to HTML
    print(f"\nExporting to {output_html}")

    # Create combined HTML with all four charts
    config = {
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
    }

    # Get HTML for each chart
    html_1 = fig_1.to_html(
        config=config,
        include_plotlyjs='cdn',
        full_html=False
    )
    html_2 = fig_2.to_html(
        config=config,
        include_plotlyjs=False,
        full_html=False
    )
    html_3 = fig_3.to_html(
        config=config,
        include_plotlyjs=False,
        full_html=False
    )
    html_4 = fig_4.to_html(
        config=config,
        include_plotlyjs=False,
        full_html=False
    )

    # Combine into single HTML document
    combined_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Conda Performance Comparison: conda vs Rattler</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1080px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #43b02a;
            padding-bottom: 10px;
        }}
        .chart-section {{
            margin: 40px 0;
            padding: 20px 0;
            border-bottom: 1px solid #e0e0e0;
        }}
        .chart-section:last-child {{
            border-bottom: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Conda Performance Comparison: Conda vs Rattler</h1>
        <p>
            This report compares the performance of conda and rattler repodata fetching across different scenarios.
            We also compare the differences between shared repodata fetching and not sharded repodata fetching.
        </p>
        
        <p>Test scenarios explained:</p>
        <ul> 
            <li>
                <b>Datascience:</b> fetching repodata for the packages "pandas", "plotly" and "scipy"
            </li>
            <li>
                <b>Python:</b> fetching repodata for the "python" package
            </li>
            <li>
                <b>Warm:</b> cache is fully loaded with no network requests necessary
            </li>
            <li>
                <b>Cold:</b> cache is empty requiring network requests
            </li>
        </ul>

        <div class="chart-section">
            {html_1}
        </div>

        <div class="chart-section">
            {html_2}
        </div>

        <div class="chart-section">
            {html_3}
        </div>

        <div class="chart-section">
            {html_4}
        </div>
    </div>
</body>
</html>
"""

    # Write combined HTML to file
    with open(output_html, 'w') as f:
        f.write(combined_html)

    print(f"\n✓ Report successfully created at: {output_html}")
    print(f"  Open it in your browser to view the interactive charts.")


if __name__ == '__main__':
    main()
