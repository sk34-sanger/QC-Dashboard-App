import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def read_length_distribution_plot(df):
    bins = ['% 0 ~ 50', '% 50 ~ 100', '% 100 ~ 150', '% 150 ~ 200', '% 200 ~ 250', '% 250 ~ 300']
    df_melted = df.melt(
        id_vars=['Sample'], 
        value_vars=bins, 
        var_name='Length Distribution', 
        value_name='Composition Percentage'
    )
    df_melted['Length Distribution'] = df_melted['Length Distribution'].str.replace('% ', '')

    fig = px.bar(
        df_melted, 
        x="Length Distribution", 
        y="Composition Percentage", 
        facet_col="Sample",  # Creates separate subplot for each sample
        facet_col_wrap=3,    # Number of columns in the grid
        title="Read Length Distribution (50nt Increments)",
        template="plotly_white",
        color_discrete_sequence=["#4591DC"]  # Single color since each sample is separate
    )
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="")
    fig.update_layout(
        yaxis=dict(
            range=[0, 100], 
            ticksuffix="%"
        ),
        xaxis_title="Length Distribution",
        yaxis_title="Composition Percentage",
        xaxis_title_font=dict(size=18),
        yaxis_title_font=dict(size=18),
        hovermode="x unified",
        height=800  # Adjust height for multiple subplots
    )

    # Update all y-axes to have consistent range
    fig.update_yaxes(range=[0, 100], ticksuffix="%")
    return fig


def sample_qc_stats_total_plot(df):
    # Create a stacked bar chart Total reads and Excluded Reads vs Sample
    df_long = df.melt(
        id_vars=["Sample"],
        value_vars=["Total Reads", "Excluded Reads"],
        var_name="Read Type",
        value_name="Read Counts",
    )
    fig = px.bar(
        df_long,
        x="Sample",
        y="Read Counts",
        color="Read Type",
        title="Total Reads vs Excluded Reads per Sample",
        template="plotly_white",
        labels={"Read Counts": "Read Counts", "Read Type": "Read Type"},
        color_discrete_sequence=["#4591DC", "#F26419"],  # Colors for Total reads and Excluded Reads
    )
    fig.update_layout(
        barmode='stack',
        xaxis_title="Sample",
        yaxis_title="Read Counts",
        xaxis_title_font=dict(size=18),
        yaxis_title_font=dict(size=18),
        hovermode="x unified",
        height=600
    )
    return fig

def sample_qc_stats_accepted_reads_plot(df, qc_stats_coverage_df):
    categories = ["% Library Reads", "% PAM Reads", "% Reference Reads", "% Unmapped Reads"]
    # Colorblind-friendly colors with 50% transparency (matching R's t_col with 0.5 alpha)
    colors = {
        "% Library Reads": "rgba(127, 205, 187, 0.5)",   # #7FCDBB with alpha
        "% PAM Reads": "rgba(246, 215, 122, 0.5)",       # #F6D77A with alpha
        "% Reference Reads": "rgba(155, 211, 240, 0.5)", # #9BD3F0 with alpha
        "% Unmapped Reads": "rgba(232, 174, 119, 0.5)",  # #E8AE77 with alpha
    }

    # Normalize to 100% (equivalent to R's position = "fill")
    percent_df = df[categories].div(df[categories].sum(axis=1), axis=0) * 100
    percent_df["Sample"] = df["Sample"]

    # Calculate y_scale for secondary axis (matching R's y_scale = max(library_cov) * 2)
    y_scale = qc_stats_coverage_df["Library Coverage"].max() * 2

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    for category in categories:
        fig.add_trace(
            go.Bar(
                x=percent_df["Sample"],
                y=percent_df[category],
                name=category,
                marker_color=colors[category],
                text=percent_df[category].round(1).astype(str) + "%",
                textposition="inside",
                insidetextanchor="middle",
                hovertemplate="%{x}<br>%{fullData.name}: %{y:.1f}%<extra></extra>",
            ),
            secondary_y=False,
        )

    fig.add_trace(
        go.Scatter(
            x=qc_stats_coverage_df["Sample"],
            y=qc_stats_coverage_df["Library Coverage"],
            name="Library Coverage",
            mode="lines+markers",
            marker=dict(color="#E31A1C", symbol="diamond", size=10),
            line=dict(color="#E31A1C", dash="dash"),
            hovertemplate="%{x}<br>Library Coverage: %{y}<extra></extra>",
        ),
        secondary_y=True,
    )

    fig.update_layout(
        barmode="stack",
        title=dict(text="Sample QC Stats", font=dict(size=24, family="sans-serif")),
        template="plotly_white",
        xaxis_title="Samples",
        yaxis_title="Percentage",
        yaxis_title_font=dict(size=18, family="sans-serif"),
        xaxis_title_font=dict(size=18, family="sans-serif"),
        hovermode="x unified",
        height=700,
        legend=dict(
            title_text="",
            font=dict(size=16),
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02
        ),
        plot_bgcolor="ivory",
    )
    fig.update_yaxes(range=[0, 100], ticksuffix="%", tickfont=dict(size=14), secondary_y=False)
    fig.update_yaxes(
        title_text="Library Coverage",
        range=[0, y_scale],
        tickfont=dict(size=14),
        secondary_y=True
    )
    fig.update_xaxes(tickangle=-90, tickfont=dict(size=14))
    return fig

def sample_qc_position_coverage_plot(df, sample_qc_cutoffs_df):
    """
    Create position coverage scatter plot for each sample
    
    Args:
        df: DataFrame with columns: sequence, position, count, sample, log2p1
        sample_qc_cutoffs_df: DataFrame with cutoff values including seq_low_count
    """
    import numpy as np
    import math
    
    # Get the threshold value for horizontal line: log2(seq_low_count + 1)
    seq_low_count = sample_qc_cutoffs_df['seq_low_count'].iloc[0]
    threshold = np.log2(seq_low_count + 1)
    
    # Get unique samples and calculate number of rows needed
    samples = df['sample'].unique()
    n_samples = len(samples)
    n_cols = 3
    n_rows = math.ceil(n_samples / n_cols)
    
    # Calculate y-axis max
    y_max = int(df['log2p1'].max()) + 1
    
    # Create subplots
    fig = make_subplots(
        rows=n_rows, 
        cols=n_cols,
        subplot_titles=[str(s) for s in samples],
        vertical_spacing=0.08,
        horizontal_spacing=0.06
    )
    
    # Add scatter plot for each sample
    for idx, sample in enumerate(samples):
        row = (idx // n_cols) + 1
        col = (idx % n_cols) + 1
        
        sample_df = df[df['sample'] == sample]
        
        # Get position range for this sample
        x_min = sample_df['position'].min()
        x_max = sample_df['position'].max()
        
        # Add scatter points
        fig.add_trace(
            go.Scatter(
                x=sample_df['position'],
                y=sample_df['log2p1'],
                mode='markers',
                marker=dict(
                    color='tomato',
                    size=2,
                    opacity=0.8
                ),
                name=sample,
                showlegend=False,
                hovertemplate="Position: %{x}<br>log2(count+1): %{y:.2f}<extra></extra>"
            ),
            row=row,
            col=col
        )
        
        # Add horizontal threshold line
        fig.add_trace(
            go.Scatter(
                x=[x_min, x_max],
                y=[threshold, threshold],
                mode='lines',
                line=dict(color='springgreen', dash='dash', width=1),
                showlegend=False,
                hoverinfo='skip'
            ),
            row=row,
            col=col
        )
        
        # Update x and y axes for each subplot with independent scales
        fig.update_xaxes(
            title_text="",
            tickfont=dict(size=8, weight=700),
            range=[x_min, x_max],
            tickvals=[x_min, x_max],
            tickformat=',d',
            row=row,
            col=col
        )
        fig.update_yaxes(
            range=[0, y_max],
            title_text="",
            tickfont=dict(size=8, weight=700),
            row=row,
            col=col
        )
    
    # Update overall layout
    fig.update_layout(
        title=dict(
            text="Sample QC Position Coverage",
            font=dict(size=12, family="Arial", weight=700)
        ),
        showlegend=False,
        plot_bgcolor='ivory',
        paper_bgcolor='white',
        height=400 * n_rows,
        hovermode='closest'
    )
    
    # Add common axis labels
    fig.add_annotation(
        text="Genomic Coordinate",
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.05,
        showarrow=False,
        font=dict(size=12, family="Arial", weight=700),
        xanchor='center'
    )
    
    fig.add_annotation(
        text="log2(count+1)",
        xref="paper",
        yref="paper",
        x=-0.02,
        y=0.5,
        showarrow=False,
        font=dict(size=12, family="Arial", weight=700),
        textangle=-90,
        yanchor='middle'
    )
    
    return fig